# MoBIE specification

The MoBIE specification describes a valid configuration for the MoBIE viewer. The specification defines four different concepts:
- A `project`, which groups data, for example from the same publication, that can be opened by the MoBIE viewer. It consists of multiple `datasets`.
- A `dataset`, which contains data that can be opened *jointly* by the MoBIE viewer.
- A `source`, which corresponds to a single image data source as well as associated metadata and viewer state.
- A `view`, which describes the viewer state.

The specification is defined via [jsonschema](https://json-schema.org/) and the schema files are located [here](https://github.com/mobie/mobie.github.io/tree/master/schema).
It is versioned, following [the semantic versioning convention](https://semver.org/). The current version is `0.2.0`.

**Using jsonschema:**

The jsonschema files can be used in the following ways:
- Static validation against the schema: using e.g. [jsonschema-python](https://python-jsonschema.readthedocs.io/en/stable/) `jsonschema -i my-dataset-schema.json schema/dataset.schema.json`. See also the [full project validation script](https://github.com/mobie/mobie.github.io/blob/master/scripts/validate_project.py).
- Generate example data from the schema with [fake-schema-cli](https://github.com/atomsfat/fake-schema-cli): `fake-schema schema/dataset.schema.json`

## <a name="project"></a>Project 

The `project` and its associated `datasets` are stored in a directory structure with the project corresponding to the root directory.
This directory must contain the file `project.json`, which must contain a valid [project schema](https://github.com/mobie/mobie.github.io/tree/master/schema/project.schema.json)
See an example project structure, slightly adapted from the [zebrafish-lm project](https://github.com/mobie/zebrafish-lm-datasets):
```
zebrafish-lm/
├── project.json
├── actin
├── cisgolgi
├── lysosomes
├── membrane
├── nuclei
└── trans_golgi
```

### <a name="project-metadata"></a>Project Metadata

The project metadata, stored in `project.json`, has the following structure:
- `datasets`: List of the available datasets. The dataset directory names must match the names in the list. It must contain at least one dataset.
- `defaultDataset`: The dataset that will be opened when the MoBIE viewer is started for this project.
- `description`: Description of this project.
- `references`: List of references for this project.
- `specVersion`: The MoBIE specification version of this project.

For the zebrafish-lm project the `project.json` looks like this:
```json
{
  "datasets": [
    "actin",
    "cisgolgi",
    "lysosomes",
    "membrane",
    "nuclei",
    "trans_golgi"
  ],
  "defaultDataset": "membrane",
  "description": "A quantitative atlas of the cellular architecture for the zebrafish posterior lateral line primoridum.",
  "references": ["https://doi.org/10.7554/eLife.55913"],
  "specVersion": "0.2.0"
}
```

### <a name="project-storage"></a>Local & Remote Projects

Projects can be either stored locally or hosted on a remote object store.
In addition, the `image data`, i.e. the image data in one of the [supported data formats](#data) and `metadata`, corresponding to the json files for this project and [tables](#tables) 
can be accessed from different storage locations for one project.

In more detail, MoBIE currently supports the following storage options:
- filesystem: can store `image data` and `metadata`.
- s3 object store: can store `image data` and `metadata`; public and private buckets are supported.
- github: can only store `metadata`, `image data` must be loaded from object store.

This enables different combinations of hosting a project, see also this [figure](fig-storage):
<ol type="a">
<li>only on filesystem: project is only available locally; this is the best mode for development.</li>
<li>only on s3 object store: project is self-contained in object store and can be shared with collaborators privately (using a privat bucket) or shared publicly (using a public bucket).</li>
<li>on github and s3 object store: the metadata is stored on github, which also serves as entrypoint for the viewer. The image sources are stored on the s3 bucket. This set-up has the advantage that metadata is under version control.</li>
</ol>

![fig-storage](../assets/hosting.png)

## <a name="dataset"></a>Dataset

A `dataset` consists of a root directory, which must contain the file `dataset.json` with a valid [dataset schema](https://github.com/mobie/mobie.github.io/tree/master/schema/project.schema.json).
It should contain the subdirectories `images`, containing the image data, `tables`, containing the table data and may contain the directory `misc`, containing additional data associated with this dataset.
Note that the location of image and table data is determined in `dataset.json` and it is thus possible to choose a different directory structure than `images/` and `tables/` to store them,
but the layout using `images/` and `tables/` is recommended for consistency with other MoBIE projects and assumed throughout this document.

The `images` directory contains the xml files describing the image data, see [data specification](#data) for details.
It may contain additional subdirectories to organise these files; by convention the files for local and remote image sources are separated into `images/local` and `images/remote`.

The `tables` directory contains all tabular data assoicated with segmentations or grid views (see [data specification](#data) and [view specification](#view) for details)
All tables associated with one segmentation or view, must be located in the same subdirectory, which must contain a table `default.tsv` and may contain additional tables. 
See the [table data specification](#tables) for details on how tables are stored.

The `misc` directory may contain the subdirectory `bookmarks` with additional views stored in json files according to the [bookmarks spec](https://github.com/mobie/mobie.github.io/tree/master/schema/bookmarks.schema.json).
It may also contain the file `leveling.json`, which specifies the "natural" orientation of the dataset and other subdirectories and other files that are associated with this dataset.


See an example dataset directory structure and `dataset.json` (left incomplete for brevity) for one of the zebrafish-lm project's dataset below.
```
actin/
├── sources.json
├── images
│   ├── local
│   └── remote
├── misc
│   └── bookmarks
│   └── leveling.json
└── tables
    ├── segmentation_sample1
    └── segmentation_sample2
```

### <a name="dataset-metadata"></a>Dataset Metadata

The dataset metadata, stored in `dataset.json`, has the following structure:
- `description`: Description of this dataset.
- `is2d`: Are all images in this dataset two dimensional?
- `sources`: Mapping source names to their [specification](#source-metadata).
- `views`: Mapping of view names for to their [specification](#view-metadata). Must contain the `default` view.

For the zebrafish-lm dataset the `dataset.json` looks like this (source and view metadata omitted for brevity):
```json
{
    "description": "Zebrafish primordium with actin staining.",
    "is2d": False,
    "sources": {
        "membrane_sample1": {"..."},
        "membrane_sample2": {"..."},
        "segmentation_sample1": {"..."}
        "segmentation_sample2": {"..."}
    },
    "views": {
        "default": {"..."}
    }
}
```

## <a name="source"></a>Source

A `source` consists of an image (volume) and associated metadata like viewer state or tables. 
Two different types of sources are supported:
- `image`: intensity images corresponding to the "primary" data, e.g. electron microscopy or light microscopy images.
- `segmentation`: label masks corresponding to segmented objects labeled by integer ids, e.g. cell or ultrastructure segmentations.

### <a name="data"></a>Image Data

The data is stored in a multi-dimensional, chunked format.
MoBIE primarily supports the [n5](https://github.com/saalfeldlab/n5) data format, using the [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) to represent timepoints and multi-scale image pyramids.
In addition, it supports [HDF5](https://www.hdfgroup.org/solutions/hdf5/), again using the [bdv hdf5 format](https://imagej.net/BigDataViewer.html#About_the_BigDataViewer_data_format); however this format can only be read locally and **does not** support remote access from an object store.
The `name` saved in the bdv.xml must agree with the name in the [source metadata](#source-metadata).
There is also experimental support for the emerging [ome ngff](https://ngff.openmicroscopy.org/latest/).

### <a name="table"></a>Table Data

MoBIE supports tables associated with segmentations, where each row corresponds to some properties of an object in the segmentation.
The tables should be stored as tab separated values `.tsv` files; they may also be stored as comma separated values `.csv`.

The default segmentation table (which is stored in `default.tsv`, see also [dataset specification](#dataset)) must contain the columns `label_id`, `anchor_x`, `anchor_y`, `anchor_z`,
`bb_min_x`, `bb_min_y`, `bb_min_z` and `bb_min_x`, `bb_min_y`, `bb_min_z`. The `anchor` columns specify a reference point for the object corresponding to this row. It will be centered
when the corresponding obejct is selected. The `bb_min` and `bb_max` columns specify the start and stop of the bounding box for the object. Both anchor and bounding box coordinates must
be given in phyisical units. It may contain additional columns.

Additional segmentation tables must contain the column `label_id` and may contain arbitraty additional columns.
The label id `0` is reserved for background and should not be listed in any of the tables.

See an example segmentation default table for 8 objects with additional column `n_pixels` giving the number of pixels of the object.
```tsv
label_id    anchor_x    anchor_y    anchor_z    bb_min_x    bb_min_y    bb_min_z    bb_max_x    bb_max_y    bb_max_z    n_pixels
1.0 49.78   41.25   8.7 45.23   37.20386467793656   3.36    56.053  44.24   17.73   127867.0
2.0 42.79   40.06   9.0 38.29   36.31097192566608   3.81    48.513  43.55   15.26   112529.0
3.0 52.79   44.33   9.9 48.41   40.477804769594975  3.81    56.946  47.02   17.96   111520.0
4.0 57.90   42.95   7.8 53.77   39.18807079409317   3.59    62.204  45.63   16.61   102318.0
5.0 47.19   45.17   9.8 43.45   42.26359027413593   4.49    51.490  47.91   17.06   95659.0
6.0 40.31   41.75   9.9 37.00   35.31886886758777   4.71    46.430  44.84   15.94   98376.0
7.0 64.68   43.91   8.4 60.12   39.98175324055582   4.71    70.439  46.72   15.71   104657.0
8.0 35.57   43.39   10. 30.55   40.676225381210635  4.93    40.676  46.03   16.16   104961.0
```

The color scheme used to display the segmentation can also be loaded from a table, see `colorByColumn` in the [source metadata](#source-metadta). In order to set an explicit color map, the field `color` may be set to `argbColumn`. In this case, the values in the column must follow the format `alpha-red-green-blue`, e.g. `255-0-0-255`.

### <a name="source-metadata"></a>Source Metadata

The metadata for the sources of a dataset is specified in the field `sources` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`sources` contains a mapping of source names to [source metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/source.schema.json).
The metadata entries have the following structure (see below for an example json file):
- `image`: An image source. The source name (=key for this source entry) must be teh same as the setup name in the bdv.xml. The fields `imageDataLocations` and `view` are required.
	- `description`: Description of this image source.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory.
		- `fileSystem`: Location of the bdv.xml for reading the source image data from the local filesystem.
		- `s3store`: Location of the bdv.xml for reading the source image data from an s3 object store.
	- `view`: Contains a [view](#view-metadata).
- `segmentation`: A segmentation source. The source name (=key for this source entry) must be teh same as the setup name in the bdv.xml. The field `imageDataLocations` is required.
	- `description`: Description of this segmentation source.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory.
		- `fileSystem`: Location of the bdv.xml for reading the source image data from the local filesystem.
		- `s3store`: Location of the bdv.xml for reading the source image data from an s3 object store.
	- `tableDataLocation`: Location of the table directory for this segmentation source, relative to the dataset root directory.
	- `view`: Contains a [view](#view-metadata).

```json
{
  "image": {
    "imageDataLocations": {
      "fileSystem": "YT.xml"
    },
    "view": {
      "isExclusive": false,
      "uiSelectionGroup": "=vZG*5",
      "sourceDisplays": [
        {
          "segmentationDisplay": {
            "opacity": 0.6339031658952454,
            "lut": "glasbeyZeroTransparent",
            "name": "GQZ",
            "sources": [
              "\"{",
              ",N*dZu34gt",
              "a|G-ba#^L",
              "QAq?><u$fI&"
            ],
            "showSelectedSegmentsIn3d": true,
            "selectedSegmentIds": [
              "Jd;782684640;69637"
            ],
            "colorByColumn": "[00zqg?p&",
            "resolution3dView": [
              74349873.45393723,
              43592822.621136844,
              91462179.813303
            ]
          }
        },
        {
          "segmentationDisplay": {
            "opacity": 0.3433189239960328,
            "lut": "glasbeyZeroTransparent",
            "name": "H1",
            "sources": [
              "?qBBk$",
              "!aIy~n)",
              "SA",
              "0?y6B==fO0",
              "n`>I"
            ],
            "showScatterPlot": true,
            "valueLimits": [
              -13519223.647686034,
              -60129278.78701437
            ],
            "colorByColumn": "M:Sl}C"
          }
        },
        {
          "segmentationDisplay": {
            "opacity": 0.4169635212560101,
            "lut": "glasbeyZeroTransparent",
            "name": "G.VME#oa'|",
            "sources": [
              "=1,&mZ#fi",
              "MT`",
              "23(6*1}s{V",
              "'"
            ],
            "valueLimits": [
              17272986.85358569,
              -32144685.90146771
            ],
            "colorByColumn": "9<B26my>c",
            "showSelectedSegmentsIn3d": true
          }
        },
        {
          "segmentationDisplay": {
            "opacity": 0.9938733316947221,
            "lut": "argbColumn",
            "name": "m!S",
            "sources": [
              "$",
              "B4a!gywwu4",
              "6?yB"
            ],
            "colorByColumn": "$=3Pbv",
            "valueLimits": [
              46349990.3327634,
              57888023.8890855
            ],
            "showScatterPlot": false,
            "selectedSegmentIds": [
              "J]c(%YI;4341612;9947764226",
              "|;41;2182636200",
              "CxMNn+r8#d;64875082;3236",
              "6BMUSo?faqE;52246;5417402816",
              "9;4760410;8776032"
            ],
            "scatterPlotAxes": [
              "7FWR~doT;O-xy",
              "x^R9H;>"
            ],
            "resolution3dView": [
              -6784753.32146959,
              -5612693.342588544,
              72514751.77515164
            ],
            "tables": [
              "$$",
              "Zmh~Ys)&",
              "5$",
              "[&f6\\hv6%Kv",
              "=z_g2$"
            ],
            "showSelectedSegmentsIn3d": true
          }
        },
        {
          "segmentationDisplay": {
            "opacity": 0.17517965901085808,
            "lut": "glasbeyZeroTransparent",
            "name": "n",
            "sources": [
              "mL6B#_a!"
            ],
            "scatterPlotAxes": [
              "5;#tE9,M>u",
              ">;R$ahyznS6"
            ],
            "showScatterPlot": true,
            "resolution3dView": [
              -68421024.18938816,
              -25474981.62035589,
              -29335425.12952511
            ],
            "tables": [
              "yP!XoAy",
              "VeE24^",
              "^+lB"
            ],
            "selectedSegmentIds": [
              "*m;3;84178438251"
            ],
            "showSelectedSegmentsIn3d": true,
            "valueLimits": [
              -26897123.859693646,
              30890341.76944843
            ],
            "colorByColumn": "^ll$j"
          }
        }
      ],
      "viewerTransform": {
        "timepoint": 36177778
      },
      "sourceTransforms": [
        {
          "affine": {
            "parameters": [
              -58030196.68331508,
              -53611002.45928054,
              10155044.635174006,
              82864392.05019015,
              -31446290.123716563,
              58716145.500630915,
              -91771303.36743647,
              77429675.26631227,
              -63741742.32945218,
              1226120.5043121725,
              -90573423.6913684,
              -61235133.31891264
            ],
            "sources": [
              "~9P"
            ],
            "timepoints": [
              42928883,
              96593048
            ]
          }
        },
        {
          "grid": {
            "sources": [
              [
                "\\PwbHPca",
                "Q"
              ],
              [
                "kuD4s!",
                "^DUaj*",
                "e"
              ],
              [
                "(<C}~J",
                "cF_oHO6",
                "U>]5rS-7",
                "#Q5MN'",
                "`gyc"
              ],
              [
                "$5<NYVQr+ab"
              ],
              [
                "ZuK\\Yy",
                "{jQBQSL4us",
                "q10C3mWQ>h",
                "`s|_M"
              ]
            ],
            "tableDataLocation": "yoK)wxU:#",
            "timepoints": [
              -76144786,
              -59968250,
              -86665083,
              86977793,
              68683435
            ]
          }
        },
        {
          "grid": {
            "sources": [
              [
                "j4Wk9D",
                "w406"
              ],
              [
                "s+Z`?",
                "_DJq{~]",
                "S",
                "%Bt",
                "ayrz"
              ],
              [
                "%M8%",
                "{^=;a",
                "FJ"
              ]
            ],
            "tableDataLocation": "XJEQ",
            "positions": [
              [
                -95703134,
                80728017,
                -50439009
              ]
            ],
            "timepoints": [
              -73068886,
              20727092
            ]
          }
        }
      ]
    },
    "description": "qui cupidatat aliqua anim id"
  }
}
```

## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce a MoBIE viewer state.

### <a name="view-grid"></a>Grid Views

Grid views can be used to arrange sources in a grid automatically. They must have an associated table that is
used for navigation in the viewer, and can also store additional properties for individual grid positions.
The table specification is the same as for the [segmentation tables](#tables), except for a different layout required in the default table,
which must contain the column `grid_id` and may contain additional arbitrary columns.
The `grid_id` column indexes the 2d grid position with row major convention.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
grid_id mitochondria    vesicles    golgi   er
0   1   0   1   0
1   1   0   1   1
2   0   0   0   1
3   0   1   0   1
```

### <a name="view-metadata"></a>View Metadata

The metadata for the views of a dataset is specified in the field `views` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`views` contains a mapping of view names to [view metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/view.schema.json).

Additional views can be stored as json files with the field `bookmarks` mapping view names to metadata in the folder `misc/bookmarks`

The metadata entries have the following structure (see below for an example json file):
- `isExclusive`: Does this view replace the current viewer state (exclusive) or is it added to it (additive)?.
- `sourceDisplays`: The display groups of this view. Contains a list with items:
	- `imageDisplay`: Viewer state for a group of image sources. The fields `color`, `contrastLimits`, `opacity`, `name` and `sources` are required.
		- `blendingMode`: The mode for blending multiple image sources.
		- `color`: The color map.
		- `contrastLimits`: The contrast limits. Contains a tuple of [number, number].
		- `name`: 
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `resolution3dView`: The resolution used for the 3d viewer, in physical units. Only relevant if 'showImageIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `showImagesIn3d`: Whether to show the images in the 3d viewer.
		- `sources`: The image sources that are part of this display group. Contains a list of strings.
	- `segmentationDisplay`:  The fields `opacity`, `lut`, `name` and `sources` are required.
		- `colorByColumn`: 
		- `lut`: The segmentation look-up-table for the segmentation coloring.
		- `name`: 
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `resolution3dView`: Resolution used for the 3d viewer, in physical units. Only relevant if 'showSelectedSegmentsIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedSegmentIds`: List of selected segment ids. Contains a list of strings.
		- `showScatterPlot`: Whether to show the scatter plot.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer.
		- `sources`: The segmentation sources that are part of this display group. Contains a list of strings.
		- `tables`: Additional tables to load. If present, the default table will always be loaded and should not be specified here. Contains a list of strings.
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
- `sourceTransforms`: The source transformations of this view. The transformations must be defined in the physical coordinate space and are applied in addition to the transformations given in the bdv.xml. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources. The fields `parameters` and `sources` are required.
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention. Contains a list of numbers.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `grid`: Arrange multiple sources in a grid by offseting sources with a grid spacing. The fields `sources` and `tableDataLocation` are required.
		- `positions`: Grid positions for the sources. If not specified, the sources will be arranged in a square grid. If given, must have the same length as `sources`. Contains a list of arrays.
		- `sources`: The sources for the grid. The outer list specifies the grid posititions, the inner list the sources per grid position. Contains a list of arrays.
		- `tableDataLocation`: Location of the table directory for this grid view, relative to the dataset root directory.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
- `uiSelectionGroup`: 
- `viewerTransform`: The viewer transformation of this view.Must contain exactly one of the following items:
	- 
		- `timepoint`: The initial timepoint shown in the viewer.
	- 
		- `affine`: Affine transformation applied by the viewer. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer.
	- 
		- `normalizedAffine`: Normalized affine transformation applied by the viewer. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer.
	- 
		- `position`: Position that will be centered in the viewer. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer.

```json
{
  "isExclusive": false,
  "uiSelectionGroup": "EEP?",
  "sourceDisplays": [
    {
      "imageDisplay": {
        "color": "red",
        "contrastLimits": [
          44698.932470764856,
          25870.10895789962
        ],
        "opacity": 0.7346415498281704,
        "name": ">225[M",
        "sources": [
          "#"
        ],
        "blendingMode": "sumOccluding",
        "resolution3dView": [
          -97427643.3343464,
          -64524331.64069049,
          98504326.85914984
        ],
        "showImagesIn3d": false
      }
    },
    {
      "imageDisplay": {
        "color": "magenta",
        "contrastLimits": [
          48094.89283560391,
          24008.792045012553
        ],
        "opacity": 0.5153851613350793,
        "name": "!sSN@zh)]",
        "sources": [
          "#zS:Nte|X~"
        ],
        "blendingMode": "sumOccluding"
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.39709112454022555,
        "lut": "glasbeyZeroTransparent",
        "name": "x-=l",
        "sources": [
          "Q#8\\3",
          "TBRG-r",
          "<}BiBpA2uG",
          "e(~TvY6ZT"
        ],
        "selectedSegmentIds": [
          "fcFALQOvi~Q;1566;58424",
          "+B7;0040473401;72010148",
          "PN#mMsj%;088;6",
          "=~+`('`#;556272;9155462"
        ],
        "valueLimits": [
          8915448.244127646,
          -93489342.55482386
        ],
        "tables": [
          "]~",
          "?GCX8-7J",
          "+~$_u2M7cFh",
          "3[jYAZx",
          "h1C'W2#,Y`:"
        ],
        "scatterPlotAxes": [
          "_~lzOu(N;zJ%?wF6oZ",
          "0,;7drjkgom"
        ],
        "showSelectedSegmentsIn3d": false
      }
    }
  ],
  "viewerTransform": {
    "normalizedAffine": [
      -38825602.67937434,
      60941710.21978161,
      49358801.94249135,
      -70724346.11695999,
      -2117273.871589735,
      68449891.16090307,
      -30771589.277686313,
      -75465020.85257503,
      -13524780.181047589,
      -98006184.417063,
      27488396.427337453,
      -74177587.39227426
    ]
  },
  "sourceTransforms": [
    {
      "grid": {
        "sources": [
          [
            "^klMv\"{I",
            "LOJrUw91O~",
            "_FyrzR1cW}",
            "g%8r+Ms:P<Q",
            "yCt$><"
          ],
          [
            "DO)V",
            "L",
            "g'1>^~e",
            "D("
          ],
          [
            "dlj}",
            "iMG\\#!kS#",
            "=",
            "e:}",
            "\"(4[i.^h"
          ]
        ],
        "tableDataLocation": "%'Y]fxa",
        "positions": [
          [
            87297406,
            54954990,
            -84522313,
            82814894,
            26990981
          ],
          [
            -18831660,
            3950742,
            -96767613,
            30498216,
            -66871298
          ],
          [
            40492741,
            -38979512
          ]
        ],
        "timepoints": [
          -63188596,
          19637655,
          -83601894
        ]
      }
    },
    {
      "affine": {
        "parameters": [
          -60294453.75044107,
          -28017813.459113583,
          -44248326.8324466,
          2062692.97983855,
          40091837.65733954,
          -64320706.22863249,
          -46679537.46018449,
          57262022.72809759,
          66369943.09025702,
          4653655.494518414,
          -9214395.51079373,
          73664788.66876641
        ],
        "sources": [
          "i",
          "Y%",
          "G+7v"
        ]
      }
    },
    {
      "grid": {
        "sources": [
          [
            "1vq)Uipg3*U",
            "-p)(7:'}",
            "++",
            "^",
            "WhR$!cG"
          ],
          [
            "]H"
          ]
        ],
        "tableDataLocation": "%gvJ",
        "timepoints": [
          23645041
        ],
        "positions": [
          [
            -46740643
          ]
        ]
      }
    },
    {
      "affine": {
        "parameters": [
          -94846594.04708174,
          7845075.218047276,
          59791605.83655828,
          -17339507.653189883,
          96120974.49444005,
          9655385.62119171,
          38335773.51335871,
          66146390.31299916,
          48522769.15636581,
          -1101997.1868268251,
          66692349.94684428,
          9635951.210210443
        ],
        "sources": [
          "GmG}vP",
          "\\UU",
          "85}P5[A0x6S",
          "+!G+QW",
          "~x+9-)"
        ],
        "timepoints": [
          7949008,
          69010024,
          25911313,
          861293,
          11942322
        ]
      }
    },
    {
      "affine": {
        "parameters": [
          82398445.3450951,
          -14685288.813732728,
          5896974.187448874,
          -66328813.66512491,
          44260336.423409134,
          -59885169.656030305,
          -87142684.06676413,
          -38183845.70617828,
          -2668792.2002323717,
          41121398.70868465,
          90176459.84641156,
          68907937.57678297
        ],
        "sources": [
          "R",
          "Qx$,MFX"
        ],
        "timepoints": [
          96844966
        ]
      }
    }
  ]
}
```

