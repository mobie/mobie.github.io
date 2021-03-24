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
- `image`: An image source. The fields `imageDataLocations` and `view` are required.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory. The field `local` is required.
		- `local`: Location of the bdv.xml file for reading the source image data from the local filesystem.
		- `remote`: Location of the bdv.xml file for reading the source image data from an object store.
	- `view`: Contains a [view](#view-metadata).
- `segmentation`: A segmentation source. The fields `imageDataLocations` and `view` are required.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory. The field `local` is required.
		- `local`: Location of the bdv.xml file for reading the source image data from the local filesystem.
		- `remote`: Location of the bdv.xml file for reading the source image data from an object store.
	- `tableDataLocation`: Location of the table directory for this segmentation source, relative to the dataset root directory.
	- `view`: Contains a [view](#view-metadata).

```json
{
  "image": {
    "imageDataLocations": {
      "local": "2J|}yu2.xml",
      "remote": "0=g.xml"
    },
    "view": {
      "menuItem": "?cei/qkj>k}E_w",
      "sourceDisplays": [
        {
          "segmentationDisplay": {
            "alpha": 0.27005306919877925,
            "color": "glasbey",
            "name": "y=xAd_",
            "sources": [
              "Ki'f",
              "j"
            ],
            "resolution3dView": [
              28156246.09837179,
              26385687.894863978,
              -7766548.654950485
            ],
            "colorByColumn": "tempor Lorem dolor nulla",
            "selectedSegmentIds": [
              "(\\3e;01775226;9485619"
            ],
            "showSelectedSegmentsIn3d": false
          }
        },
        {
          "segmentationDisplay": {
            "alpha": 0.4692857036113911,
            "color": "blueWhiteRed",
            "name": "IK@",
            "sources": [
              "s?~&')8Ov",
              "cYEN|I\"2g|",
              "wt(Un_T",
              "X,B=x*"
            ],
            "showSelectedSegmentsIn3d": true,
            "selectedSegmentIds": [
              "z{N'L(E2$5;8586;263"
            ],
            "valueLimits": [
              -31541379.541055337,
              46646445.98664966
            ],
            "resolution3dView": [
              -71520391.9111307,
              59920196.198866814,
              -87957728.61205457
            ],
            "tables": [
              "!&v#sdvpE`",
              "JmAmurpj\\3"
            ],
            "colorByColumn": "cillum et non id"
          }
        },
        {
          "segmentationDisplay": {
            "alpha": 0.33280154042290055,
            "color": "argbColumn",
            "name": "m",
            "sources": [
              "HMCxoceP'_U"
            ],
            "resolution3dView": [
              32601926.384777218,
              16212278.371424153,
              -63594131.67138266
            ],
            "tables": [
              "Bi4a",
              "EK_PL4",
              "2{Q}rEJT",
              "gspn)",
              "M?4svm%}Ad<"
            ],
            "selectedSegmentIds": [
              "hF={Aw@E;3588848;47",
              "45;04265436;2083192",
              "@8%;91147984;85137",
              "5I5\\P_;4;7",
              "8@f;194615752;34172538139"
            ],
            "colorByColumn": "et sed deserunt non"
          }
        },
        {
          "imageDisplay": {
            "color": "r=21,g=58232,b=811975,a=67531771",
            "contrastLimits": [
              48650.95612807671,
              46828.41729963934
            ],
            "name": "!I",
            "sources": [
              "%cjZZ#\"",
              "*e",
              "U",
              ":",
              "Wx6I')&"
            ],
            "resolution3dView": [
              -5196656.331089988,
              1484966.0222498775,
              76403001.45874014
            ],
            "showImagesIn3d": false
          }
        }
      ],
      "sourceTransforms": [
        {
          "autoGrid": {
            "sources": [
              [
                "$]t[a{@@",
                ";*h4Y218$\\?",
                "uiigIp\\"
              ],
              [
                "We5"
              ]
            ],
            "tableDataLocation": "()I5^qV"
          }
        },
        {
          "affine": {
            "parameters": [
              -42361098.42301672,
              -63440871.46781563,
              -70221251.424837,
              94536853.0464274,
              98239962.0830737,
              39540227.43397787,
              -22130657.95634246,
              52956084.69991353,
              -38390658.34929709,
              -10598778.547171012,
              -19866282.146334946,
              -50898318.686544105
            ],
            "sources": [
              "p(",
              "O6\\e!rV8fSo",
              "7l(\"W{B~_5p"
            ],
            "timepoints": [
              61790329,
              40635249,
              92907508,
              80214617,
              75393452
            ]
          }
        },
        {
          "autoGrid": {
            "sources": [
              [
                "TV?EIM>"
              ],
              [
                "ko._%",
                "Lu]EbWr",
                "aUI<q&$R",
                "$|IIp#t|t",
                "Yl|"
              ],
              [
                "CX;+f0`\")cg"
              ],
              [
                "lkUhrmgY7#+",
                "Cz){3"
              ],
              [
                "bOK$8KwTkT",
                "Yu29b6SIV[f",
                "fmy{NAE3T",
                "n"
              ]
            ],
            "tableDataLocation": "nxHsa",
            "timepoints": [
              -79815722,
              -41214276,
              1340731,
              72954433,
              -25616998
            ]
          }
        }
      ],
      "viewerTransform": {
        "normalizedAffine": [
          -4250653.086052746,
          56330471.87869641,
          6549104.653937027,
          -26200547.426446125,
          81461809.56160536,
          31578185.91173251,
          -91136913.93817462,
          -27957702.461276352,
          -25029803.60898924,
          53700167.21095213,
          -14231290.842697322,
          -10655780.042264953
        ]
      }
    }
  }
}
```

## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce a MoBIE viewer state.

### <a name="view-grid"></a>Grid Views

Grid views can be used to arrange sources in a grid automatically. They must have an associated table, that is
used for navigation in the viewer, and can also store additional properties for individual grid positions.
The table specification is the same as for the [segmentation tables](#tables), except for a different layout required in the default table,
which must contain the column `grid_id` and may contain additional arbitrary columns.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
grid_id mitochondria    vesicles    golgi   er
0   1   0   1   0   0
0   1   0   1   1   0
0   2   0   0   1   1
0   3   1   0   1   1
```

### <a name="view-metadata"></a>View Metadata

The metadata for the views of a dataset is specified in the field `views` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`views` contains a mapping of view names to [view metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/view.schema.json).

Additional views can be stored as json files with the field `bookmarks` mapping view names to metadata in the folder `misc/bookmarks`

The metadata entries have the following structure (see below for an example json file):
- `sourceDisplays`: The display groups of this view. Contains a list with items:
	- `imageDisplay`: Viewer state for a group of image sources. The fields `color`, `contrastLimits`, `name` and `sources` are required.
		- `color`: The color map.
		- `contrastLimits`: The contrast limits. Contains a tuple of [number, number].
		- `name`: 
		- `resolution3dView`: The resolution used for the 3d viewer, in physical units. Only relevant if 'showImageIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `showImagesIn3d`: Whether to show the images in the 3d viewer.
		- `sources`: The image sources that are part of this display group. Contains a list of strings.
	- `segmentationDisplay`:  The fields `alpha`, `color`, `name` and `sources` are required.
		- `alpha`: The alpha value used for blending segmentation and image data in the viewer.
		- `colorByColumn`: 
		- `lut`: The segmentation look-up-table for the segmentation coloring.
		- `name`: 
		- `resolution3dView`: Resolution used for the 3d viewer, in physical units. Only relevant if 'showSelectedSegmentsIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedSegmentIds`: List of selected segment ids. Contains a list of strings.
		- `showScatterPlot`: Whether to show the scatter plot.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer.
		- `sources`: The segmentation sources that are part of this display group. Contains a list of strings.
		- `tables`: Additional tables to load. If present, the default table will always be loaded and should not be specified here. Contains a list of strings.
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
- `sourceTransforms`: The source transformations of this view. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources. The fields `parameters` and `sources` are required.
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention. Contains a list of numbers.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `autoGrid`: Arange a list of soures in grid. The fields `sources` and `tableDataLocation` are required.
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
  "uiSelectionGroup": "Q\"=N~GK+^",
  "viewerTransform": {
    "position": [
      44298289.45397805,
      97680567.0750037,
      46968746.73622109
    ]
  }
}
```

