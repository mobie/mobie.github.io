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

The `images` directory contains the metadata files describing the image data, see [data specification](#data) for details.
It may contain additional subdirectories to organise these files. By convention the files for different data formats are often separated into folders named accordingly, e.g. `images/bdv-n5` and `images/bdv-n5-s3`.

The `tables` directory contains all tabular data assoicated with segmentations or grid views (see [data specification](#data) and [view specification](#view) for details)
All tables associated with a segmentation or view, must be located in the same subdirectory. This subdirectory must contain a default table, which should be called `default.tsv`, and may contain additional tables. 
See the [table data specification](#tables) for details on how tables are stored.

The `misc` directory may contain the subdirectory `views` with additional views stored in json files according to the [views spec](https://github.com/mobie/mobie.github.io/tree/master/schema/views.schema.json).
It may also contain the file `leveling.json`, which specifies the "natural" orientation of the dataset and other subdirectories and other files that are associated with this dataset.


See an example dataset directory structure and `dataset.json` (left incomplete for brevity) for one of the zebrafish-lm project's dataset below.
```
actin/
├── sources.json
├── images
│   ├── bdv-n5
│   └── bdv-n5-s3
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

The data is stored in a chunked format for multi-dimensional data. Currently MoBIE supports the following data formats:
- `bdv.n5` and `bdv.n5.s3`: the data is stored in the [n5](https://github.com/saalfeldlab/n5) data format. The [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) is used to store additional metadata about timepoints, the multi-scale image pyramid and transformations. To support data stored on s3, we extend the xml by custom fields that describe the s3 storage. See an example
  [here](https://github.com/mobie/plankton-fibsem-project/blob/master/data/emiliania/images/bdv-n5-s3/raw.xml#L27).
- `bdv.hdf5`: the data is stored in the [HDF5](https://www.hdfgroup.org/solutions/hdf5/) data format, using the [bdv hdf5 format](https://imagej.net/BigDataViewer.html#About_the_BigDataViewer_data_format) to represent image metadata. This format can only be read locally and **does not** support remote access from an object store.
- `bdv.ome.zarr` and `bdv.ome.zarr.s3`: the data is stored in the [ome zarr file format](https://ngff.openmicroscopy.org/latest/) and uses the same xml format as in the [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md), but using `bdv.ome.zarr` as ImageLoader format. The custom xml fields for `bdv.ome.zarr.s3` are identical to `bdv.n5.s3`. The support for this file format is still experimental.
- `openOrganelle.s3`: the data is stored in the [open organelle data format](https://openorganelle.janelia.org/), which is based on [n5](https://github.com/saalfeldlab/n5). Currently, this data format can only be streamed from s3 and not opened locally. We have added it to support data made available throuhg the Open Organelle data platform and the support is still experimental.

For the data formats using a BigDataViewer xml, each xml must only contain a single setup id and the value of the field `name` must be the same as the name in the [source metadata](#source-metadata).

### <a name="table"></a>Table Data

MoBIE supports tables associated with segmentations, where each row corresponds to some properties of an object in the segmentation.
The tables should be stored as tab separated values `.tsv` files; they may also be stored as comma separated values `.csv`.

The default segmentation table (which should be stored in `default.tsv` in the corresponding table, see also [dataset specification](#dataset)) must contain the columns `label_id`, `anchor_x`, `anchor_y`, `anchor_z`,
`bb_min_x`, `bb_min_y`, `bb_min_z` and `bb_min_x`, `bb_min_y`, `bb_min_z`. The `anchor` columns specify a reference point for the object corresponding to this row. It will be centered
when the corresponding obejct is selected. The `bb_min` and `bb_max` columns specify the start and stop of the bounding box for the object. Both anchor and bounding box coordinates must
be given in phyisical units. It may contain additional columns.

Additional segmentation tables must contain the column `label_id` and may contain arbitraty additional columns.
The `label_id`s in the additional tables may be incomplete, but they must not contain ids not present in the default table.
For example, given `label_id`s `[1, 2, 3, 4, 5]` in the default table the `label_id`s `[1, 2, 3, 4, 5]` or `[1, 3, 4]` are valid but `[1, 3, 4, 7]` is invalid.
The label id `0` is reserved for the background and must not be listed in any of the tables.

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
		- `bdv.hdf5`: Data stored in the bdv.hdf5 format, i.e. hdf5 data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.n5`: Data stored in the bdv.n5 format, i.e. n5 data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.n5.s3`: Data stored in the bdv.n5.s3 format, i.e. n5 data that is stored on a s3 object store. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.ome.zarr`: Data stored in the bdv.ome.zarr format, i.e. ome.zarr data that is stored on the local fileystem with additional bdv xml metadata. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.ome.zarr.s3`: Data stored in the bdv.ome.zarr.s3 format, i.e. ome.zarr data that is stored on a s3 object store with additional bdv xml metadata. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `ome.zarr`: Data stored in the ome.zarr format, i.e. ome.zarr data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the ome.zarr file, relative to the dataset root location.
		- `ome.zarr.s3`: Data stored in the ome.zarr.s3 format, i.e. ome.zarr data that is stored on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
		- `openOrganelle.s3`: Data stored in the openOrganelle file format on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
- `segmentation`: A segmentation source. The source name (=key for this source entry) must be teh same as the setup name in the bdv.xml. The field `imageData` is required.
	- `description`: Description of this segmentation source.
	- `imageData`: Description of the image data for this source, including the file format and the location of the data.
		- `bdv.hdf5`: Data stored in the bdv.hdf5 format, i.e. hdf5 data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.n5`: Data stored in the bdv.n5 format, i.e. n5 data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.n5.s3`: Data stored in the bdv.n5.s3 format, i.e. n5 data that is stored on a s3 object store. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.ome.zarr`: Data stored in the bdv.ome.zarr format, i.e. ome.zarr data that is stored on the local fileystem with additional bdv xml metadata. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `bdv.ome.zarr.s3`: Data stored in the bdv.ome.zarr.s3 format, i.e. ome.zarr data that is stored on a s3 object store with additional bdv xml metadata. The field `relativePath` is required.
			- `relativePath`: The file path to the xml storing the bdv metadata, relative to the dataset root location.
		- `ome.zarr`: Data stored in the ome.zarr format, i.e. ome.zarr data that is stored on the local fileystem. The field `relativePath` is required.
			- `relativePath`: The file path to the ome.zarr file, relative to the dataset root location.
		- `ome.zarr.s3`: Data stored in the ome.zarr.s3 format, i.e. ome.zarr data that is stored on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
		- `openOrganelle.s3`: Data stored in the openOrganelle file format on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
	- `tableData`: Description of the table data for this source, including the format and the location of the table data. The field `tsv` is required.
		- `tsv`: Table data in tsv file format, specified as root location for the table data. The field `relativePath` is required.
			- `relativePath`: The relative path of the table data w.r.t the dataset root location.

```json
{
  "segmentation": {
    "imageData": {
      "bdv.hdf5": {
        "relativePath": "in quis laboris Lorem"
      },
      "openOrganelle.s3": {
        "s3Address": "Duis minim qui nisi"
      },
      "bdv.n5.s3": {
        "relativePath": "est aute sunt ea labore"
      },
      "ome.zarr.s3": {
        "s3Address": "culpa consequat"
      }
    },
    "tableData": {
      "tsv": {
        "relativePath": "mollit commodo aute sint qui"
      }
    },
    "description": "qui"
  }
}
```

## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce a MoBIE viewer state.

### <a name="view-source-annotations"></a>Source Annotations

Views can optionally contain source annotations, which are specified via a `sourceAnnotationDisplay` (see schema description below). Source annotations contain a table, which has rows that are associated with the sources in this view and can be used to navigate to the sources (by clicking on the row) and store additional source level annotations.
Source annotation tables should be stored as tab separated values, but may also be comma separated.
They must contain the column `annotation_id`, which is used for navigation in the viewer, and must contain at least one more column.
The values in the `annotation_id` must be strings and must correspond to the keys of the `sources` field in the `sourceAnnotationDisplay`.
A primary application of source annotations are tables for views containing a `grid` transform (see schema description below).

In this case the `annotation_id` column corresponds to the flat grid position, which is computed from the 2d grid position according to the row-major indexing convention.
The mapping of grid positions to sources is defined in the `sources` field.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
annotation_id    mitochondria    vesicles    golgi   er
source1   1   0   1   0
source2   1   0   1   1
source3   0   0   0   1
source4   0   1   0   1
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
		- `sources`: The image sources that are part of this display group. Multiple sources should be moved apart spatially with source transform(s), e.g. grid, otherwise they will not be correctly displayed in the viewer. Contains a list of strings.
	- `segmentationDisplay`:  The fields `opacity`, `lut`, `name` and `sources` are required.
		- `blendingMode`: The mode for blending multiple image sources.
		- `colorByColumn`: 
		- `lut`: The look-up-table for categorical coloring modes.
		- `name`: 
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `resolution3dView`: Resolution used for the 3d viewer, in physical units. Only relevant if 'showSelectedSegmentsIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedSegmentIds`: List of selected segment ids. Contains a list of strings.
		- `showScatterPlot`: Whether to show the scatter plot. The default is 'false', i.e. if this property is not present the scatter plot should not be shown.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer.
		- `sources`: The segmentation sources that are part of this display group. Multiple sources should be moved apart spatially with source transform(s), e.g. grid, otherwise they will not be correctly displayed in the viewer. Contains a list of strings.
		- `tables`: The tables to load for this display. Must include the default table as the first item. Contains a list with items:
			- ``: 
			- ``: 
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
	- `sourceAnnotationDisplay`:  The fields `sources`, `tableData`, `tables`, `opacity`, `lut` and `name` are required.
		- `colorByColumn`: 
		- `lut`: The look-up-table for categorical coloring modes.
		- `name`: 
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedAnnotationIds`: List of selected source annotation ids. Contains a list of strings.
		- `showScatterPlot`: Whether to show the scatter plot. The default is 'false', i.e. if this property is not present the scatter plot should not be shown.
		- `sources`: Contains array with items of type [None](#None-metadata)
		- `tableData`: Contains a [tableData](#tableData-metadata).
		- `tables`: The tables to load for this display. Must include the default table as the first item. Contains a list with items:
			- ``: 
			- ``: 
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
- `sourceTransforms`: The source transformations of this view. The transformations must be defined in the physical coordinate space and are applied in addition to the transformations given in the bdv.xml. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources. The fields `parameters` and `sources` are required.
		- `name`: 
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention. Contains a list of numbers.
		- `sourceNamesAfterTransform`: Names of the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `grid`: Arrange multiple sources in a grid by offseting sources with a grid spacing. The field `sources` is required.
		- `name`: 
		- `positions`: Grid positions for the sources. If not specified, the sources will be arranged in a square grid. If given, must have the same keys as `sources`, mapping to 2d grid positions.Contains array with items of type [None](#None-metadata)
		- `sourceNamesAfterTransform`: Contains array with items of type [None](#None-metadata)
		- `sources`: Contains array with items of type [None](#None-metadata)
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `crop`: Crop transformation applied to a list of sources. The fields `min`, `max` and `sources` are required.
		- `max`: Maximum coordinates for the crop. Contains a list of numbers.
		- `min`: Minimum coordinates for the crop. Contains a list of numbers.
		- `name`: 
		- `shiftToOrigin`: Whether to shift the source to the coordinate space origin after applying the crop. By default true.
		- `sourceNamesAfterTransform`: Names of the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
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
  "uiSelectionGroup": "~",
  "description": "id consectetur tempor in sed",
  "sourceDisplays": [
    {
      "segmentationDisplay": {
        "opacity": 0.3558171101635148,
        "lut": "viridis",
        "name": "Hh2R",
        "sources": [
          "|3<m"
        ],
        "tables": [
          ".2nvH3c$QAC.tsv",
          "M.tsv",
          "pq4s.csv"
        ],
        "scatterPlotAxes": [
          "c'O::",
          "lrxMC-f?"
        ],
        "blendingMode": "sum",
        "colorByColumn": "p\\hv",
        "showScatterPlot": true,
        "valueLimits": [
          -96127174.89251122,
          10592213.456028342
        ],
        "showSelectedSegmentsIn3d": true,
        "selectedSegmentIds": [
          "sF*`N(V4&xq;30;0299",
          "P0Q3yh)x;3118897;44912224",
          "m:mL`9,-ZJZ;621760164;10",
          "D^M4d4Zw\\;660;950112214"
        ],
        "resolution3dView": [
          -6351403.396917775,
          55201063.502655506,
          50285329.4329617
        ]
      }
    },
    {
      "sourceAnnotationDisplay": {
        "sources": {
          "deserunt9c": [
            "uY$:y].",
            "Sa\\vxh",
            "m\\]a~]l"
          ]
        },
        "tableData": {
          "tsv": {
            "relativePath": "eu"
          }
        },
        "tables": [
          "0O#V~-nV.tsv",
          "o@.tsv",
          "v\"K.tsv",
          "=,2WBK.tsv",
          "UsPNr)-8~.tsv"
        ],
        "opacity": 0.23130875953467767,
        "lut": "glasbey",
        "name": "{~",
        "valueLimits": [
          54941373.97505513,
          -93888085.9906278
        ],
        "colorByColumn": ")of^hV^",
        "showScatterPlot": false
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.21668963907827354,
        "lut": "viridis",
        "name": "Fxtr]kO",
        "sources": [
          "aKfV-Z*uV",
          "~?7{>JB",
          "O:*=!aI"
        ],
        "scatterPlotAxes": [
          "z_",
          "}j^!k"
        ],
        "tables": [
          "eq7baF:.tsv"
        ],
        "blendingMode": "sum",
        "resolution3dView": [
          53334130.28314,
          34492911.200997055,
          -60395806.05433388
        ],
        "showSelectedSegmentsIn3d": true,
        "valueLimits": [
          47524030.549262345,
          13321421.744171947
        ],
        "showScatterPlot": false,
        "colorByColumn": "],Z(\\,B47&J",
        "selectedSegmentIds": [
          "jqe2F|d;10;3015",
          "np;10;12817195501"
        ]
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.724606387654052,
        "lut": "glasbeyZeroTransparent",
        "name": "q3$mQ=1e`K",
        "sources": [
          "Nn&-q~_Y}",
          "hc=Zzh",
          "9\"[F@T",
          "S",
          "uYH"
        ],
        "showSelectedSegmentsIn3d": false,
        "selectedSegmentIds": [
          "hTuiq[w+>*m;970882;3"
        ],
        "scatterPlotAxes": [
          "HmFBq`y",
          ":?"
        ],
        "showScatterPlot": false,
        "resolution3dView": [
          -24834026.34798844,
          25605925.898883,
          32406052.29982543
        ],
        "tables": [
          "_.csv",
          "+@\\#rxW.tsv",
          "{w?.csv",
          "[.tsv"
        ],
        "colorByColumn": "$P)V6",
        "valueLimits": [
          -99612413.22152166,
          -68168005.60299207
        ],
        "blendingMode": "sumOccluding"
      }
    },
    {
      "segmentationDisplay": {
        "opacity": 0.459514946359483,
        "lut": "argbColumn",
        "name": "T",
        "sources": [
          "\"?w",
          "{FF\\[",
          "\"WM{,A7F,:s",
          "i7YlOFx<",
          "|FM$}bI[)FH"
        ]
      }
    }
  ]
}
```

