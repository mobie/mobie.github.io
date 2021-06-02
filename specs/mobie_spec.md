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

The `misc` directory may contain the subdirectory `views` with additional views stored in json files according to the [views spec](https://github.com/mobie/mobie.github.io/tree/master/schema/views.schema.json).
It may also contain the file `leveling.json`, which specifies the "natural" orientation of the dataset and other subdirectories and other files that are associated with this dataset.


See an example dataset directory structure and `dataset.json` (left incomplete for brevity) for one of the zebrafish-lm project's dataset below.
```
actin/
├── sources.json
├── images
│   ├── local
│   └── remote
├── misc
│   └── views
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
    "is2d": false,
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

A `source` consists of an image (volume) and associated metadata like tables. 
Two different types of sources are supported:
- `image`: intensity images corresponding to the "primary" data, e.g. electron microscopy or light microscopy images.
- `segmentation`: label masks corresponding to segmented objects labeled by integer ids, e.g. cell or ultrastructure segmentations.

### <a name="data"></a>Image Data

The data is stored in a multi-dimensional, chunked format.
MoBIE primarily supports the [n5](https://github.com/saalfeldlab/n5) data format, using the [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) to represent timepoints and multi-scale image pyramids.
In addition, it supports [HDF5](https://www.hdfgroup.org/solutions/hdf5/), again using the [bdv hdf5 format](https://imagej.net/BigDataViewer.html#About_the_BigDataViewer_data_format); however this format can only be read locally and **does not** support remote access from an object store.
The `name` saved in the bdv.xml must agree with the name in the [source metadata](#source-metadata).
There is also experimental support for the emerging [ome ngff](https://ngff.openmicroscopy.org/latest/) and the [open organelle data](https://openorganelle.janelia.org/).

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
- `image`: An image source. The source name (=key for this source entry) must be teh same as the setup name in the bdv.xml. The field `imageData` is required.
	- `description`: Description of this image source.
	- `imageData`: Description of the image data for this source, including the file format and the location of the data.
		- `fileSystem`: Source for the image data on the local filesystem. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, relative to the dataset location on the filesystem.
		- `gitHub`: Source for the image data on github. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, relative to the dataset location on github.
		- `s3Store`: Source for the image data on an s3 object store. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, full s3 address.
- `segmentation`: A segmentation source. The source name (=key for this source entry) must be teh same as the setup name in the bdv.xml. The field `imageData` is required.
	- `description`: Description of this segmentation source.
	- `imageData`: Description of the image data for this source, including the file format and the location of the data.
		- `fileSystem`: Source for the image data on the local filesystem. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, relative to the dataset location on the filesystem.
		- `gitHub`: Source for the image data on github. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, relative to the dataset location on github.
		- `s3Store`: Source for the image data on an s3 object store. The fields `format` and `source` are required.
			- `format`: The image data file format.
			- `source`: The location of the image data 'entry point', e.g. the xml file for bdv file formats, full s3 address.
	- `tableData`: Description of the table data for this source, including the format and the location of the table data.
		- `fileSystem`: Source for the table data on the local filesystem. The fields `format` and `source` are required.
			- `format`: The table data file format. Note that for the `tsv` format, the source must point to the root location with all table files.
			- `source`: The location of the table data, relative to the dataset location on the filesystem.
		- `gitHub`: Source for the table data on github. The fields `format` and `source` are required.
			- `format`: The table data file format. Note that for the `tsv` format, the source must point to the root location with all table files.
			- `source`: The location of the table data, relative to the dataset location on github.
		- `s3Store`: Source for the image data on an s3 object store. The fields `format` and `source` are required.
			- `format`: The table data file format. Note that for the `tsv` format, the source must point to the root location with all table files.
			- `source`: The location of the table data, full s3 address.

```json
{
  "segmentation": {
    "imageData": {
      "s3Store": {
        "format": "bdv.n5.s3",
        "source": "deserunt in in dolor consequat"
      },
      "fileSystem": {
        "format": "bdv.hdf5",
        "source": "occaecat incididunt et consectetur Duis"
      }
    },
    "tableData": {
      "gitHub": {
        "format": "tsv",
        "source": "Ut sed minim"
      },
      "s3Store": {
        "format": "tsv",
        "source": "culpa est reprehenderit"
      },
      "fileSystem": {
        "format": "tsv",
        "source": "pariatur labore consequat dolore quis"
      }
    },
    "description": "cupidatat pariatur Excepteur"
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

Additional views can be stored as json files with the field `views` mapping view names to metadata in the folder `misc/views`

The metadata entries have the following structure (see below for an example json file):
- `description`: Free text description of this view.
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
		- `showScatterPlot`: Whether to show the scatter plot. The default is 'false', i.e. if this property is not present the scatter plot should not be shown.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer.
		- `sources`: The segmentation sources that are part of this display group. Contains a list of strings.
		- `tables`: Additional tables to load. If present, the default table will always be loaded and should not be specified here. Contains a list with items:
			- ``: 
			- ``: 
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
- `sourceTransforms`: The source transformations of this view. The transformations must be defined in the physical coordinate space and are applied in addition to the transformations given in the bdv.xml. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources. The fields `parameters` and `sources` are required.
		- `names`: Optional names the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention. Contains a list of numbers.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `grid`: Arrange multiple sources in a grid by offseting sources with a grid spacing. The fields `sources` and `tableDataLocation` are required.
		- `names`: Optional names the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `positions`: Grid positions for the sources. If not specified, the sources will be arranged in a square grid. If given, must have the same length as `sources`. Contains a list of arrays.
		- `sources`: The sources for the grid. The outer list specifies the grid posititions, the inner list the sources per grid position. Contains a list of arrays.
		- `tableDataLocation`: Location of the table directory for this grid view, relative to the dataset root directory.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `crop`: Crop transformation applied to a list of sources. The fields `min`, `max` and `sources` are required.
		- `max`: Maximum coordinates for the crop. Contains a list of numbers.
		- `min`: Minimum coordinates for the crop. Contains a list of numbers.
		- `names`: Optional names the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `shiftToOrigin`: Whether to shift the source to the coordinate space origin after applying the crop. By default true.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
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
  "uiSelectionGroup": "3fySl",
  "description": "velit nisi ad",
  "sourceTransforms": [
    {
      "crop": {
        "min": [
          -4210089.588782132,
          -68220644.68709669,
          15318176.781018928
        ],
        "max": [
          62726327.88104254,
          -99366491.48345701,
          -28372768.83910729
        ],
        "sources": [
          "X"
        ],
        "names": [
          "lv"
        ],
        "shiftToOrigin": false,
        "timepoints": [
          61610873
        ]
      }
    },
    {
      "grid": {
        "sources": [
          [
            "YL;",
            "692>ZG7SA["
          ],
          [
            "mXATf",
            "`F",
            "b_cJi",
            "uH0N~ZLL",
            "M96"
          ],
          [
            "E$jC7HH2",
            "Uh%@#11",
            "XkUB#.0b+'j",
            "`:T;^>..wL2"
          ],
          [
            "rN0P\\n6l",
            "SWtze}="
          ],
          [
            "Qc}",
            ".r6{ec"
          ]
        ],
        "tableDataLocation": "Z<+",
        "timepoints": [
          14637906,
          -74016228,
          -6024317,
          -43655147,
          -4125987
        ],
        "names": [
          "c\"piAnK.N",
          "!9F$]lF",
          "63=Hezm"
        ],
        "positions": [
          [
            -37498921,
            -64189977,
            -37107315,
            90585203,
            -3492329
          ],
          [
            -71794970,
            -85322276,
            -17435768,
            38050421,
            -26379537
          ]
        ]
      }
    },
    {
      "grid": {
        "sources": [
          [
            "JR6;"
          ],
          [
            "RZC(R0v(n",
            "j[_W",
            ">#]y",
            "[)"
          ]
        ],
        "tableDataLocation": "P"
      }
    }
  ],
  "viewerTransform": {
    "affine": [
      75615926.7372503,
      30214491.024365976,
      -53909118.32299783,
      -55373935.897121385,
      68124737.7476958,
      -25685006.46915047,
      -60038857.681553945,
      -22409283.119013608,
      4190849.482084632,
      -95010277.09253523,
      -69431152.56408867,
      24246799.78746611
    ]
  },
  "sourceDisplays": [
    {
      "imageDisplay": {
        "color": "cyan",
        "contrastLimits": [
          26037.234081710958,
          34602.09382463078
        ],
        "opacity": 0.26292165157853864,
        "name": "{(|Y7]<q>",
        "sources": [
          "[;7BLr1Z"
        ],
        "showImagesIn3d": true,
        "blendingMode": "sumOccluding",
        "resolution3dView": [
          -11139479.231796965,
          56536172.20849815,
          -228472.27522318065
        ]
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.5433730534460282,
        "lut": "argbColumn",
        "name": "Ra-._zjG%",
        "sources": [
          "d>mBR'0pd:",
          "UAM~P#,"
        ],
        "tables": [
          "|T%V-I.csv",
          "cJxx&~1CYH.csv",
          "hKYJ3>WV).csv"
        ],
        "selectedSegmentIds": [
          "IV;84635842;4178684",
          "YG,(tx;2936991055;5500110329",
          "Jl;718300;782",
          "7Nb=Y8*>=;3;3151022"
        ]
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.4630427111209743,
        "lut": "argbColumn",
        "name": "KC(NreJ?MI",
        "sources": [
          "gy3\\[$s4"
        ],
        "showSelectedSegmentsIn3d": false,
        "valueLimits": [
          -53465381.89044803,
          40017829.78872445
        ],
        "resolution3dView": [
          82554584.17240384,
          29179696.737790868,
          7329434.746076301
        ],
        "colorByColumn": "wt",
        "tables": [
          "CB`2.csv",
          "P0j.tsv",
          "0.csv",
          "%.csv"
        ]
      }
    },
    {
      "imageDisplay": {
        "color": "gray",
        "contrastLimits": [
          17841.724260122897,
          40062.09745922233
        ],
        "opacity": 0.09325340443679697,
        "name": "HT&UgInu^",
        "sources": [
          "-&+$e"
        ],
        "blendingMode": "sum",
        "resolution3dView": [
          85041664.30147037,
          -64542402.64338784,
          -20125267.092780024
        ],
        "showImagesIn3d": false
      }
    },
    {
      "imageDisplay": {
        "color": "black",
        "contrastLimits": [
          32254.61807084258,
          23636.413433219997
        ],
        "opacity": 0.807409175647879,
        "name": ">ta}y",
        "sources": [
          "E)",
          "^Jz(m:EUEg",
          "`qyd3[&4.",
          "c;?$P{CE",
          "~zj+zO4j[.Y"
        ]
      }
    }
  ]
}
```

