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
- Generate example data from the schema with [fake-schema-cli](https://github.com/atomsfat/fake-schema-cli): `fake-schema schema/dataset.schema.json `

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
- `project`: Additional project metadata.
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
  "project": {
    "description": "A quantitative atlas of the cellular architecture for the zebrafish posterior lateral line primoridum.",
    "references": ["https://doi.org/10.7554/eLife.55913"]
  },
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
All tables associated with one segmentation or view, must be located in the same subdirectory, which must a table `default.tsv` and may contain additional tables. 
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
- `dataset`: Additional information for this dataset.
    - `description`: Description of this dataset.
    - `is2d`: Are all images in this dataset two dimensional?
- `sources`: Mapping source names to their [specification](#source-metadata).
- `views`: Mapping of view names for to their [specification](#view-metadata). Must contain the `default` view.

For the zebrafish-lm dataset the `dataset.json` looks like this (source and view metadata omitted for brevity):
```json
{
    "dataset": {
        "description": "Zebrafish primordium with actin staining.",
        "is2d": False
    },
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
- `image`: An image source.. The fields `imageDataLocations`, `menuItem` and `view` are required.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory.. The field `local` is required.
		- `local`: Location of the bdv.xml file for reading the source image data from the local filesystem..
		- `remote`: Location of the bdv.xml file for reading the source image data from an object store..
	- `menuItem`: Menu item created for this source in the viewer GUI. The value leading the / determines the menu name, the value trailing it the item name..
	- `view`: Contains a [view](#view-metadata).
- `segmentation`: A segmentation source. The fields `imageDataLocations`, `menuItem` and `view` are required.
	- `imageDataLocations`: Location of the bdv.xml files for this source, relative to the dataset root directory.. The field `local` is required.
		- `local`: Location of the bdv.xml file for reading the source image data from the local filesystem..
		- `remote`: Location of the bdv.xml file for reading the source image data from an object store..
	- `menuItem`: Menu item created for this source in the viewer GUI. The value leading the / determines the menu name, the value trailing it the item name..
	- `tableDataRootLocation`: Location of the table root directory for this segmentation source, relative to the dataset root directory..
	- `view`: Contains a [view](#view-metadata).

```json
{
  "segmentation": {
    "imageDataLocations": {
      "local": ",z.xml"
    },
    "menuItem": "!a<kkY/[2Z{bde",
    "view": {
      "sourceDisplays": [
        {
          "segmentationDisplays": {
            "alpha": 0.238404436099513,
            "color": "glasbey",
            "name": ",'dw)1nji\\f",
            "sources": [
              "sHOjJizQNg",
              "yO=Y|:E"
            ],
            "showSelectedSegmentsIn3d": true,
            "colorByColumn": "in",
            "valueLimits": [
              38106402.61704439,
              -53566203.45417617
            ],
            "resolution3dView": [
              10182736.97209318,
              -20493327.90620646,
              32522199.896690696
            ],
            "tables": [
              "-?\\1LlH0",
              "kx?xIX*VIr|",
              "V"
            ],
            "selectedSegmentIds": [
              "CXU.z-b;996;7",
              "at6^ap\\;607;516020628",
              "z)[Gz;20;02537451120",
              ".2;29164584983;112",
              "zG.U@3at;776;570113"
            ]
          }
        },
        {
          "imageDisplays": {
            "color": "r=5,g=95,b=576077,a=58786",
            "contrastLimits": [
              49081.455405724584,
              44961.86508519593
            ],
            "name": "g3Ya'",
            "sources": [
              "*y%J'xeD&",
              "]ngTv3de",
              "u<{\\c$L",
              "pFfTgP`x",
              "_"
            ],
            "resolution3dView": [
              -62034533.371665426,
              -42561102.63717616,
              26991069.874406606
            ],
            "showImagesIn3d": false
          }
        }
      ]
    },
    "tableDataRootLocation": "J_Dr-"
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
- `sourceDisplays`: The display groups of this view.. Contains a list with items:
	- `imageDisplays`: Viewer state for a group of image sources.. The fields `color`, `contrastLimits`, `name` and `sources` are required.
		- `color`: The color map..
		- `contrastLimits`: The contrast limits.. Contains a tuple of [number, number].
		- `name`: 
		- `resolution3dView`: The resolution used for the 3d viewer, in physical units. Only relevant if 'showImageIn3d' is true. Will be determined automatically if not specified.. Contains a list of numbers.
		- `showImagesIn3d`: Whether to show the images in the 3d viewer..
		- `sources`: The image sources that are part of this display group.. Contains a list of strings.
	- `segmentationDisplays`:  The fields `alpha`, `color`, `name` and `sources` are required.
		- `alpha`: The alpha value used for blending segmentation and image data in the viewer..
		- `color`: The segmentation color map..
		- `colorByColumn`: Name of table column that is used for coloring. By default the 'label_id' column is used..
		- `name`: 
		- `resolution3dView`: Resolution used for the 3d viewer, in physical units. Only relevant if 'showSelectedSegmentsIn3d' is true. Will be determined automatically if not specified.. Contains a list of numbers.
		- `selectedSegmentIds`: List of selected segment ids.. Contains a list of strings.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer..
		- `sources`: The segmentation sources that are part of this display group.. Contains a list of strings.
		- `tables`: Additional tables to load. If present, the default table will always be loaded and should not be specified here.. Contains a list of strings.
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'.. Contains a tuple of [number, number].
- `sourceTransforms`: The source transformations of this view.. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources.. The fields `name`, `parameters` and `sources` are required.
		- `name`: 
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention.. Contains a list of numbers.
		- `sources`: The sources this transformation is applied to.. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints.. Contains a list of integers.
	- `autoGrid`: Arange a list of soures in grid.. The fields `name`, `sources` and `tableDataRootLocation` are required.
		- `name`: 
		- `sources`: The sources for the grid. The outer list specifies the grid posititions, the inner list the sources per grid position.. Contains a list of arrays.
		- `tableDataRootLocation`: Location of the table root directory for this grid view, relative to the dataset root directory..
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints.. Contains a list of integers.
- `viewerTransform`: The viewer transformation of this view..Must contain exactly one of the following items:
	- 
		- `timepoint`: The initial timepoint shown in the viewer..
	- 
		- `affine`: Affine transformation applied by the viewer.. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer..
	- 
		- `normalizedAffine`: Normalized affine transformation applied by the viewer.. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer..
	- 
		- `position`: Position that will be centered in the viewer.. Contains a list of numbers.
		- `timepoint`: The initial timepoint shown in the viewer..

```json
{
  "sourceDisplays": [
    {
      "segmentationDisplays": {
        "alpha": 0.08421050053830847,
        "color": "viridis",
        "name": "d>I#V!",
        "sources": [
          "%7)2:\"7"
        ],
        "valueLimits": [
          -25958112.243235126,
          -47324558.97129233
        ],
        "showSelectedSegmentsIn3d": false,
        "resolution3dView": [
          9211455.885129377,
          19549785.14271462,
          -20173314.373023167
        ],
        "colorByColumn": "laborum adipisicing do ut nulla",
        "selectedSegmentIds": [
          "qE$A=)%}R;0092;94882733",
          "&~z[';4;1110595",
          "'3;4149880342;0",
          "Z83A!Y;3;796365256"
        ]
      }
    },
    {
      "imageDisplays": {
        "color": "glasbeyFromRandom",
        "contrastLimits": [
          23807.83338656263,
          13330.582834161185
        ],
        "name": "%>yW2+w?\\4~",
        "sources": [
          "S!}\"\\e$\\",
          "Y@FSeQ[",
          "?Eq",
          "(L"
        ],
        "resolution3dView": [
          -85581146.35301104,
          85984386.96246475,
          91362289.23954964
        ]
      }
    },
    {
      "imageDisplays": {
        "color": "magenta",
        "contrastLimits": [
          40006.100871378374,
          32158.583646508938
        ],
        "name": "+:8sKw3yk5-",
        "sources": [
          "R]0"
        ],
        "showImagesIn3d": true,
        "resolution3dView": [
          -60290584.329927064,
          -61394846.45059285,
          -82099198.37872341
        ]
      }
    },
    {
      "imageDisplays": {
        "color": "red",
        "contrastLimits": [
          10041.629458522459,
          19463.351072466226
        ],
        "name": "1*Dc\"'6v@p",
        "sources": [
          "DO@<)AyK<",
          "X#Gt#_73"
        ],
        "showImagesIn3d": false
      }
    }
  ],
  "sourceTransforms": [
    {
      "autoGrid": {
        "name": "d{",
        "sources": [
          [
            "w",
            "jCW]03TS27",
            "3",
            "u@lBf.r"
          ],
          [
            "8jk",
            "yK\"",
            "$2LoQ{'W",
            "O_c3:p_9_)Z"
          ],
          [
            "bmKm"
          ],
          [
            "NYC1)|Ep$GO",
            "UVFyN5fj",
            "nC8h)",
            ";G`g<cs1=",
            "A"
          ],
          [
            "IAt)-]",
            "Yx=0#P\"&J)",
            "|zx"
          ]
        ],
        "tableDataRootLocation": "r=w+AJJ`f|N",
        "timepoints": [
          3359705,
          -26840367,
          -82248924,
          -55359996
        ]
      }
    },
    {
      "autoGrid": {
        "name": "emKEyz`dh",
        "sources": [
          [
            "!2PS3aP7<9A",
            "p:.7nPvI",
            "h]:U_'&}A8t",
            "wNB6<^",
            "TbeSPu;YH"
          ],
          [
            "i9S8g~AS)*w",
            "q9`PECF3",
            "TZb"
          ]
        ],
        "tableDataRootLocation": "rc=ou4",
        "timepoints": [
          16755729,
          31579057,
          45090143
        ]
      }
    },
    {
      "autoGrid": {
        "name": "vf",
        "sources": [
          [
            "[A:A'Z",
            "UV",
            ")!7(<'",
            "q]l5"
          ],
          [
            "zSj#fyH",
            "$Si;=eO+s{|",
            "sx"
          ],
          [
            "lUe"
          ],
          [
            "|M:kK",
            "KeoiA",
            "3B",
            "<NZ"
          ]
        ],
        "tableDataRootLocation": "1zavO=I",
        "timepoints": [
          -52365993,
          -59581333
        ]
      }
    },
    {
      "affine": {
        "name": "]bl&HwIi#v",
        "parameters": [
          -54820097.03256581,
          60881937.94397706,
          -70312130.19502576,
          86858691.75094637,
          33196231.781764045,
          -7405621.09580867,
          -81793869.94297709,
          -51515837.7802551,
          48215851.54651809,
          -81018748.48851845,
          56892190.50988892,
          -73508678.79698883
        ],
        "sources": [
          "c"
        ]
      }
    }
  ],
  "viewerTransform": {
    "position": [
      59767528.45476001,
      73750180.12645009,
      92633292.23736124
    ]
  }
}
```
