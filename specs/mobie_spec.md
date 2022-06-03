# MoBIE specification

MoBIE projects follow the specification described here; it is based on four key concepts:
- A `project`, which groups data, for example from the same publication, that can be opened by the MoBIE viewer. It consists of multiple `datasets`.
- A `dataset`, which contains data that can be opened in the same MoBIE viewer instance.
- A `source`, which corresponds to the data for a single image (also volume, timeseries) or segmentation image. For segmentation images it may also contain the associated tabular data.
- A `view`, which describes the full viewer state.

The specification is defined via [jsonschema](https://json-schema.org/). The schema files are located [here](https://github.com/mobie/mobie.github.io/tree/master/schema).
It is versioned, following [the semantic versioning convention](https://semver.org/). The current version is `0.2.0`.

**Using jsonschema:**

The jsonschema files can be used in the following ways:
- Static validation against the schema: using e.g. [jsonschema-python](https://python-jsonschema.readthedocs.io/en/stable/) `jsonschema -i my-dataset-schema.json schema/dataset.schema.json`. See also the [full project validation script](https://github.com/mobie/mobie.github.io/blob/master/scripts/validate_project.py).
- Generate example data from the schema with [fake-schema-cli](https://github.com/atomsfat/fake-schema-cli): `fake-schema schema/dataset.schema.json`

## <a name="project"></a>Project 

The `project` and its associated `datasets` are stored in a directory structure, with the project corresponding to the root directory.
This directory must contain the file `project.json`, which must contain a valid [project schema](https://github.com/mobie/mobie.github.io/tree/master/schema/project.schema.json).
See an example project structure, slightly adapted from the [clem project](https://github.com/mobie/clem-example-project):
```
clem/
├── project.json
├── hela
└── yeast
```

### <a name="project-metadata"></a>Project Metadata

The project metadata, stored in `project.json`, has the following structure:
- `datasets`: List of the available datasets. The dataset directory names must match the names in this list. It must contain at least one dataset.
- `defaultDataset`: The dataset that will be opened when the MoBIE viewer is started for this project.
- `imageDataFormats`: The image data formats present in this project, see [supported data formats](#data) for details.
- `description`: Description of this project.
- `references`: List of references for this project.
- `specVersion`: The MoBIE specification version of this project.

For the clem project the `project.json` looks like this:
```yaml
{
  "datasets": ["hela", "yeast"],
  "defaultDataset": "hela",
  "description": "Correlative electron microscopy data from the Schwab Lab at EMBL Heidelberg.",
  "imageDataFormats": ["ome.zarr", "ome.zarr.s3"]
  "references": ["https://doi.org/10.1083/jcb.201009037", "https://doi.org/10.1038/nmeth.1486"],
  "specVersion": "0.2.0"
}
```

### <a name="project-storage"></a>Local & Remote Projects

Projects can be stored locally or hosted remotely and  the `image data`, i.e. the images in one of the [supported data formats](#data) and `metadata`, i.e. the json files describing the project and [tabular data](#tables) can be accessed from different storage locations for one project.

In more detail, MoBIE currently supports the following three storage options:
- filesystem: can store `image data` and `metadata`.
- s3 object storage: can store `image data` and `metadata`; public and private buckets are supported.
- github: can only store `metadata`, `image data` must be loaded from object storarge.

This enables different combinations of hosting a project, see also [this figure](fig-storage):
<ol type="a">
<li>only on filesystem: project is only available locally.</li>
<li>only on s3 object storage: project is self-contained in object storage and can be shared with collaborators privately (using a privat bucket) or shared publicly (using a public bucket).</li>
<li>on github and s3 object storage: the metadata is stored on github, which also serves as entrypoint for the viewer. The image data is stored on the s3 bucket. This set-up has the advantage that the metadata is under version control.</li>
</ol>

![fig-storage](../assets/hosting.png)

## <a name="dataset"></a>Dataset

A `dataset` consists of a root directory, which must contain the file `dataset.json` with a valid [dataset schema](https://github.com/mobie/mobie.github.io/tree/master/schema/dataset.schema.json).
It should contain the subdirectories `images`, containing the image data, `tables`, containing the table data and may contain the directory `misc`, containing additional data associated with this dataset.
Note that the location of image and table data is determined in `dataset.json` and it is thus possible to choose a different directory structure than `images/` and `tables/` to store them,
but the layout using `images/` and `tables/` is recommended for consistency with other MoBIE projects and assumed throughout this document.

The `images` directory contains the metadata files describing the image data, see [data specification](#data) for details.
It may contain additional subdirectories to organise these files. By convention the files for different data formats are often separated into folders named accordingly, e.g. `images/bdv-n5` and `images/bdv-n5-s3`.

The `tables` directory contains all tabular data assoicated with segmentations or region displays (see [data specification](#data) and [view specification](#view) for details)
The tables associated with a segmentation or view, must all be located in the same subdirectory. This subdirectory must contain a default table, which should be called `default.tsv`, and may contain additional tables. 
See the [table data specification](#tables) for details on how tables are stored.

The `misc` directory may contain the subdirectory `views` with additional views stored in json files according to the [views spec](https://github.com/mobie/mobie.github.io/tree/master/schema/views.schema.json).

See an example dataset directory structure and `dataset.json` (left incomplete for brevity) for one of the zebrafish-lm project's dataset below.
```
hela/
├── dataset.json
├── images
│   ├── bdv-n5
│   └── bdv-n5-s3
├── misc
│   └── views
└── tables
    ├── em-crop
    └── lm-tomogram-table
```

### <a name="dataset-metadata"></a>Dataset Metadata

The dataset metadata, stored in `dataset.json`, has the following structure:
- `defaultLocation`: Default location used to initialize the `location` GUI element of the MoBIE menu.
- `description`: Description of this dataset.
- `is2d`: Are all images in this dataset two dimensional?
- `sources`: Mapping source names to their [specification](#source-metadata).
- `views`: Mapping of view names for to their [specification](#view-metadata). Must contain the `default` view.

For example, the `dataset.json` file for the `hela` dataset looks like this (source and view metadata omitted for brevity):
```yaml
{
    "defaultLocation": {...}
    "description": "A correlative electron microscopy sample of a HeLa cell.",
    "is2d": false,
    "sources": {
        "em-detail-a1-A": {...},
        "em-detail-a2-A": {...},
        ...
    },
    "views": {
        "default": {...},
        ...
    }
}
```

## <a name="source"></a>Source

A `source` consists of an image (volume, timeseries) and optionally associated tabular data. 
Two different types of sources are supported:
- `image`: intensity images corresponding to the "primary" data, e.g. electron microscopy or light microscopy images.
- `segmentation`: label masks corresponding to segmented objects labeled by integer ids, e.g. cell or ultrastructure segmentations.

### <a name="data"></a>Image Data

The data is stored in a chunked format for multi-dimensional data. Currently MoBIE supports the following data formats:
- `bdv.n5` and `bdv.n5.s3`: the data is stored in the [n5](https://github.com/saalfeldlab/n5) data format. The [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) is used to store additional metadata about timepoints, the multi-scale image pyramid and transformations. To support data stored on s3, we extend the xml by custom fields that describe the s3 storage. See an example
  [here](https://github.com/mobie/plankton-fibsem-project/blob/master/data/emiliania/images/bdv-n5-s3/raw.xml#L27).
- `bdv.hdf5`: the data is stored in the [HDF5](https://www.hdfgroup.org/solutions/hdf5/) data format, using the [bdv hdf5 format](https://imagej.net/BigDataViewer.html#About_the_BigDataViewer_data_format) to represent image metadata. This format can only be read locally and **does not** support remote access from an object store.
- `ome.zarr` and `ome.zarr.s3`: the data is stored in the [ome zarr file format](https://ngff.openmicroscopy.org/latest/), which contains all relevant metadata about transformations and the multi-scale image pyramid in the zarr file directly.
- `openOrganelle.s3`: the data is stored in the [open organelle data format](https://openorganelle.janelia.org/), which is based on [n5](https://github.com/saalfeldlab/n5). Currently, this data format can only be streamed from s3 and cannnot be opened locally. We have added it to support data made available throuhg the Open Organelle data platform and the support is still experimental.

For the data formats using a BigDataViewer xml file, each xml file must only contain a single setup id and the value of the field `name` must be the same as the name in the [source metadata](#source-metadata).
Similarly, data stored in `ome.zarr` must only contain a single channel, and the value of the `name` field in the image metadata must correspond to the name of the source.

### <a name="table"></a>Table Data

MoBIE supports tables associated with segmentations, where each row corresponds to properties of an object in the segmentation.
The tables should be stored as tab separated values `.tsv` files; they may also be stored as comma separated values `.csv`.

The default segmentation table (which should be stored in `default.tsv` in the corresponding table folder, see also [dataset specification](#dataset)) must contain the columns `label_id`, `anchor_x`, `anchor_y`, `anchor_z`,
`bb_min_x`, `bb_min_y`, `bb_min_z` and `bb_min_x`, `bb_min_y`, `bb_min_z`. The `anchor` columns specify a reference point for the object corresponding to this row. It will be centered
when the corresponding obejct is selected. The `bb_min` and `bb_max` columns specify the start and stop of the bounding box for the object. Both anchor and bounding box coordinates must
be given in phyisical units. The table may contain additional columns.

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

The color scheme used to display the segmentation can also be loaded from a table, see `colorByColumn` in the [view metadata](#view-metadata). In order to set an explicit color map, the field `color` may be set to `argbColumn`. In this case, the values in the column must follow the format `alpha-red-green-blue`, e.g. `255-0-0-255`.

### <a name="source-metadata"></a>Source Metadata

The metadata for the sources of a dataset is specified in the field `sources` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`sources` contains a mapping of source names to [source metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/source.schema.json).
The source metadata has the following elements (see below for an example json):
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
			- `signingRegion`: The signing region for aws, e.g. us-east-1.
		- `openOrganelle.s3`: Data stored in the openOrganelle file format on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
			- `signingRegion`: The signing region for aws, e.g. us-east-1.
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
			- `signingRegion`: The signing region for aws, e.g. us-east-1.
		- `openOrganelle.s3`: Data stored in the openOrganelle file format on a s3 object store. The field `s3Address` is required.
			- `s3Address`: The s3 address for this image data.
			- `signingRegion`: The signing region for aws, e.g. us-east-1.
	- `tableData`: Description of the table data for this source, including the format and the location of the table data. The field `tsv` is required.
		- `tsv`: Table data in tsv file format, specified as root location for the table data. The field `relativePath` is required.
			- `relativePath`: The relative path of the table data w.r.t the dataset root location.

**Examples:**
```yaml
{
  "em-detail-a1-A": {
    "image": {
      "imageData": {
        "bdv.n5": {
          "relativePath": "images/bdv-n5/em-detail-a1-A.xml"
        },
        "bdv.n5.s3": {
          "relativePath": "images/bdv-n5-s3/em-detail-a1-A.xml"
        }
      }
    }
  }
}
```
```yaml
{
  "em-segmentation": {
    "segmentation": {
      "imageData": {
        "bdv.n5": {
          "relativePath": "images/local/em-segmentation.xml"
        },
        "bdv.n5.s3": {
          "relativePath": "images/remote/em-segmentation.xml"
        }
      },
      "tableData": {
        "tsv": {
          "relativePath": "tables/em-segmentation"
        }
      }
    }
  }
}
```
## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce the MoBIE viewer state.

### <a name="view-source-annotations"></a>Region Displays

Views may contain region displays, specified by a `regionDisplay` (see schema description below), which describe the physical locations of images or collection of images in the global coordinate system.
Region displays must contain a table with rows associated with the sources of the display. This table can be used in the viewer to navigate to the corresponding sources (by clicking on the row) and it may store additional annotations or measurements for the correspoding image(s).
The tables should be stored as tab separated values, but may also be comma separated.
They must contain the column `region_id` and must contain at least one more column.
The values in the `region_id` column must be strings and must correspond to the keys of the `sources` field in the `regionDisplay`.

A primary application of region displays are tables for views with a `grid` transform (see schema description below).
In this case the `region_id` column corresponds to the flattened grid position, which is computed from the 2d grid position according to the row-major indexing convention.
The mapping of grid positions to sources is defined in the `sources` field.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
region_id    mitochondria    vesicles    golgi   er
source1   1   0   1   0
source2   1   0   1   1
source3   0   0   0   1
source4   0   1   0   1
```

### <a name="view-metadata"></a>View Metadata

The metadata for the views of a dataset is specified in the field `views` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`views` contains a mapping of view names to [view metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/view.schema.json).

Additional views can be stored as json files with the field `views` mapping view names to metadata in the folder `misc/views`

The view metadata has the following elements (see below for an example json file):
- `description`: Free text description of this view.
- `isExclusive`: Does this view replace the current viewer state (exclusive) or is it added to it (additive)?.
- `sourceDisplays`: The display groups of this view. Contains a list with items:
	- `imageDisplay`: Viewer state for a group of image sources. The fields `color`, `contrastLimits`, `opacity`, `name` and `sources` are required.
		- `blendingMode`: The mode for blending multiple image sources.
		- `color`: The color map.
		- `contrastLimits`: The contrast limits. Contains a tuple of [number, number].
		- `name`: Name for this field.
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `resolution3dView`: The resolution used for the 3d viewer, in physical units. Only relevant if 'showImageIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `showImagesIn3d`: Whether to show the images in the 3d viewer.
		- `sources`: The image sources that are part of this display group. Multiple sources should be moved apart spatially with source transform(s), e.g. grid, otherwise they will not be correctly displayed in the viewer. Contains a list of strings.
		- `visible`: Are the sources of this display visible? Default is true.
	- `segmentationDisplay`:  The fields `opacity`, `lut`, `name` and `sources` are required.
		- `boundaryThickness`: Thickness of the boundary masks. Only used if showAsBoundaries is true.
		- `colorByColumn`: Name for this field.
		- `lut`: The look-up-table for categorical coloring modes.
		- `name`: Name for this field.
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `randomColorSeed`: Random seed for the random color lut (e.g. glasbey) to reproduce the exact colors of the view. (Optional).
		- `resolution3dView`: Resolution used for the 3d viewer, in physical units. Only relevant if 'showSelectedSegmentsIn3d' is true. Will be determined automatically if not specified. Contains a list of numbers.
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedSegmentIds`: List of selected segment ids, each of the form sourceName;timePoint;label_id. Contains a list of strings.
		- `showAsBoundaries`: Show boundary mask instead of segment masks. Default is false.
		- `showScatterPlot`: Whether to show the scatter plot. The default is 'false', i.e. if this property is not present the scatter plot should not be shown.
		- `showSelectedSegmentsIn3d`: Whether to show the selected segments in the 3d viewer.
		- `showTable`: Show the table GUI element. Default is true (if the display has a table).
		- `sources`: The segmentation sources that are part of this display group. Multiple sources should be moved apart spatially with source transform(s), e.g. grid, otherwise they will not be correctly displayed in the viewer. Contains a list of strings.
		- `tables`: The tables to load for this display. Must include the default table as the first item. Contains a list with items:
			- Path to a csv table.
			- Path to a tsv table.
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
		- `visible`: Are the sources of this display visible? Default is true.
	- `regionDisplay`:  The fields `sources`, `tableData`, `tables`, `opacity`, `lut` and `name` are required.
		- `boundaryThickness`: Thickness of the boundary masks. Only used if showAsBoundaries is true.
		- `colorByColumn`: Name for this field.
		- `lut`: The look-up-table for categorical coloring modes.
		- `name`: Name for this field.
		- `opacity`: The alpha value used for blending segmentation and image data in the viewer.
		- `randomColorSeed`: Random seed for the random color lut (e.g. glasbey) to reproduce the exact colors of the view. (Optional).
		- `scatterPlotAxes`: The names of columns which should be used for the scatter plot. Contains a list of strings.
		- `selectedRegionIds`: List of selected source region ids, each of the form timePoint;regionId. Contains a list of strings.
		- `showAsBoundaries`: Show boundary mask instead of region masks. Default is false.
		- `showScatterPlot`: Whether to show the scatter plot. The default is 'false', i.e. if this property is not present the scatter plot should not be shown.
		- `showTable`: Show the table GUI element. Default is true.
		- `sources`: Contains array with items of type [None](#None-metadata)
		- `tableData`: Contains a [tableData](#tableData-metadata).
		- `tables`: The tables to load for this display. Must include the default table as the first item. Contains a list with items:
			- Path to a csv table.
			- Path to a tsv table.
		- `valueLimits`: Value limits for numerical color maps like 'blueWhiteRed'. Contains a tuple of [number, number].
		- `visible`: Is the color overlay of this display visible? Default is true.
- `sourceTransforms`: The source transformations of this view. The transformations must be defined in the physical coordinate space and are applied in addition to the transformations given in the bdv.xml. Contains a list with items:
	- `affine`: Affine transformation applied to a list of sources. The fields `parameters` and `sources` are required.
		- `name`: Name for this field.
		- `parameters`: Parameters of the affine transformation, using the BigDataViewer convention. Contains a list of numbers.
		- `sourceNamesAfterTransform`: Names of the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `mergedGrid`: A grid view of multiple sources that creates an new merged source. Only valid if all sources have the same size (both in pixels and physical space). The fields `mergedGridSourceName` and `sources` are required.
		- `encodeSource`: Encode the source name into the pixel value. This is necessary for merged grid label sources.
		- `mergedGridSourceName`: Name for this field.
		- `positions`: Grid positions for the sources. If not specified, the sources will be arranged in a square grid. If given, must have the same length as `sources` and contain 2d grid positions specified as [y, x]. Contains a list of arrays.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
	- `crop`: Crop transformation applied to a list of sources. The fields `min`, `max` and `sources` are required.
		- `boxAffine`: The transformation to place the crop's bounding box in the global coordinate system (if not given assumes identity). Contains a list of numbers.
		- `centerAtOrigin`: Whether to center the source at the coordinate space origin after applying the crop. By default true.
		- `max`: Maximum coordinates for the crop. Contains a list of numbers.
		- `min`: Minimum coordinates for the crop. Contains a list of numbers.
		- `name`: Name for this field.
		- `rectify`: Whether to align the crop's bounding box with the coordinate system. By default true.
		- `sourceNamesAfterTransform`: Names of the sources after transformation. If given, must have the same number of elements as `sources`. Contains a list of strings.
		- `sources`: The sources this transformation is applied to. Contains a list of strings.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
	- `transformedGrid`: Arrange multiple sources in a grid by offseting sources with a grid spacing. The field `nestedSources` is required.
		- `centerAtOrigin`: Center the views at the origin for 3d sources.
		- `name`: Name for this field.
		- `nestedSources`:  Contains a list of arrays.
		- `positions`: Grid positions for the sources. If not specified, the sources will be arranged in a square grid. If given, must have the same length as `sources` and contain 2d grid positions specified as [y, x]. Contains a list of arrays.
		- `sourceNamesAfterTransform`:  Contains a list of arrays.
		- `timepoints`: The valid timepoints for this transformation. If none is given, the transformation is valid for all timepoints. Contains a list of integers.
- `uiSelectionGroup`: Name for this field.
- `viewerTransform`: A viewer transform to specify position, rotation, timepoint and/or zoom.Must contain exactly one of the following items:
	- 
		- `timepoint`: The initial timepoint shown in the viewer.
	- 
		- `normalVector`: The normal vector to the view plane. Contains a list of numbers.
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

**Examples:**
```yaml
{
  "default": {
    "isExclusive": false,
    "sourceDisplays": [
      {
        "imageDisplay": {
          "blendingMode": "sum",
          "color": "r=255,g=255,b=255,a=255",
          "contrastLimits": [
            290,
            23000
          ],
          "name": "em-overview",
          "opacity": 1.0,
          "sources": [
            "em-overview"
          ]
        }
      }
    ],
    "sourceTransforms": [
      {
        "affine": {
          "name": "MapScaleMat",
          "parameters": [
            -0.10198378825464686,
            -0.9710562907353596,
            0.0,
            0.0,
            -0.9846441741918877,
            0.11862126451903302,
            0.0,
            0.0,
            0.0,
            0.0,
            29.30832356389215,
            0.0
          ],
          "sources": [
            "em-overview"
          ]
        }
      },
      {
        "affine": {
          "name": "Translation",
          "parameters": [
            1.0,
            0.0,
            0.0,
            481.249,
            0.0,
            1.0,
            0.0,
            493.667,
            0.0,
            0.0,
            1.0,
            0.0
          ],
          "sources": [
            "em-overview"
          ]
        }
      },
      {
        "affine": {
          "name": "manual_shift_a3",
          "parameters": [
            1.0,
            0.0,
            0.0,
            1.7940359100750243,
            0.0,
            1.0,
            0.0,
            -6.6635619517072655,
            0.0,
            0.0,
            1.0,
            0.0
          ],
          "sources": [
            "em-overview"
          ]
        }
      }
    ],
    "uiSelectionGroup": "bookmark"
  }
}
```
```yaml
{
  "highmag_tomos": {
    "isExclusive": true,
    "sourceDisplays": [
      {
        "imageDisplay": {
          "blendingMode": "sumOccluding",
          "color": "r=255,g=255,b=255,a=255",
          "contrastLimits": [
            30,
            240
          ],
          "name": "highmag_tomos_images",
          "opacity": 1.0,
          "sources": [
            "tomo_37_hm",
            "tomo_38_hm",
            "tomo_40_hm",
            "tomo_41_hm",
            "tomo_53_hm",
            "tomo_54_hm"
          ]
        }
      },
      {
        "regionDisplay": {
          "lut": "glasbey",
          "name": "highmag_tomos",
          "opacity": 0.5,
          "sources": {
            "0": [
              "tomo_37_hm"
            ],
            "1": [
              "tomo_38_hm"
            ],
            "2": [
              "tomo_40_hm"
            ],
            "3": [
              "tomo_41_hm"
            ],
            "4": [
              "tomo_53_hm"
            ],
            "5": [
              "tomo_54_hm"
            ]
          },
          "tableData": {
            "tsv": {
              "relativePath": "tables/highmag_tomos"
            }
          },
          "tables": [
            "default.tsv"
          ]
        }
      }
    ],
    "sourceTransforms": [
      {
        "transformedGrid": {
          "centerAtOrigin": true,
          "nestedSources": [
            [
              "tomo_37_hm"
            ],
            [
              "tomo_38_hm"
            ],
            [
              "tomo_40_hm"
            ],
            [
              "tomo_41_hm"
            ],
            [
              "tomo_53_hm"
            ],
            [
              "tomo_54_hm"
            ]
          ]
        }
      }
    ],
    "uiSelectionGroup": "bookmark"
  }
}
```

```yaml
{
    "Figure2c": {
      "isExclusive": true,
      "sourceDisplays": [
        {
          "imageDisplay": {
            "blendingMode": "sumOccluding",
            "color": "r=255,g=255,b=255,a=255",
            "contrastLimits": [
              150.0,
              45700.0
            ],
            "name": "em-detail-a3",
            "opacity": 1.0,
            "showImagesIn3d": false,
            "sources": [
              "em-detail-a3-A"
            ],
            "visible": true
          }
        },
        {
          "imageDisplay": {
            "blendingMode": "sumOccluding",
            "color": "r=255,g=255,b=255,a=255",
            "contrastLimits": [
              30000,
              35000
            ],
            "name": "tomo_38_lm",
            "opacity": 1.0,
            "sources": [
              "tomo_38_lm"
            ]
          }
        },
        {
          "imageDisplay": {
            "blendingMode": "sumOccluding",
            "color": "white",
            "contrastLimits": [
              70.0,
              235.0
            ],
            "name": "tomo_38_hm",
            "opacity": 1.0,
            "sources": [
              "tomo_38_hm"
            ]
          }
        },
        {
          "imageDisplay": {
            "blendingMode": "sum",
            "color": "r=255,g=0,b=0,a=255",
            "contrastLimits": [
              55.0,
              400.0
            ],
            "name": "fluorescence-a3-c0",
            "opacity": 1.0,
            "showImagesIn3d": false,
            "sources": [
              "fluorescence-a3-c0"
            ],
            "visible": true
          }
        },
        {
          "imageDisplay": {
            "blendingMode": "sum",
            "color": "r=0,g=255,b=0,a=255",
            "contrastLimits": [
              40.0,
              250.0
            ],
            "name": "fluorescence-a3-c1",
            "opacity": 1.0,
            "showImagesIn3d": false,
            "sources": [
              "fluorescence-a3-c1"
            ],
            "visible": true
          }
        },
        {
          "imageDisplay": {
            "blendingMode": "sum",
            "color": "r=0,g=0,b=255,a=255",
            "contrastLimits": [
              40.0,
              400.0
            ],
            "name": "fluorescence-a3-c2",
            "opacity": 1.0,
            "showImagesIn3d": false,
            "sources": [
              "fluorescence-a3-c2"
            ],
            "visible": true
          }
        },
        {
          "regionDisplay": {
            "boundaryThickness": 0.2,
            "colorByColumn": "annotationColor",
            "lut": "argbColumn",
            "name": "lm-tomo-annotations",
            "opacity": 1.0,
            "selectedRegionIds": [
              "0;1"
            ],
            "showAsBoundaries": true,
            "sources": {
              "1": [
                "tomo_38_lm"
              ]
            },
            "tableData": {
              "tsv": {
                "relativePath": "tables/lm-tomogram-table"
              }
            },
            "tables": [
              "default.tsv"
            ]
          }
        },
        {
          "regionDisplay": {
            "boundaryThickness": 0.2,
            "colorByColumn": "annotationColor",
            "lut": "argbColumn",
            "name": "hm-tomo-annotations",
            "opacity": 1.0,
            "showAsBoundaries": true,
            "sources": {
              "1": [
                "tomo_38_hm"
              ]
            },
            "tableData": {
              "tsv": {
                "relativePath": "tables/highmag_tomos"
              }
            },
            "tables": [
              "default.tsv"
            ]
          }
        }
      ],
      "sourceTransforms": [
        {
          "affine": {
            "name": "MapScaleMat",
            "parameters": [
              -0.18777152869337194,
              0.9821399838237337,
              0.0,
              0.0,
              1.0032799126909004,
              0.16846097748363031,
              0.0,
              0.0,
              0.0,
              0.0,
              99.62143853357243,
              0.0
            ],
            "sources": [
              "em-detail-a3-A"
            ]
          }
        },
        {
          "affine": {
            "name": "Translation",
            "parameters": [
              1.0,
              0.0,
              0.0,
              203.422,
              0.0,
              1.0,
              0.0,
              238.934,
              0.0,
              0.0,
              1.0,
              0.0
            ],
            "sources": [
              "em-detail-a3-A"
            ]
          }
        },
        {
          "affine": {
            "name": "affine0",
            "parameters": [
              0.013245148924148945,
              1.0039595803164607,
              0.0,
              239.93945962096353,
              1.0206688295391182,
              -0.034661042654656964,
              0.0,
              300.37466120697667,
              0.0,
              0.0,
              1.0,
              -0.191475
            ],
            "sources": [
              "tomo_38_lm"
            ]
          }
        },
        {
          "affine": {
            "name": "affine0",
            "parameters": [
              0.013245148924148947,
              1.0039595803164607,
              0.0,
              243.59201639109855,
              1.0206688295391182,
              -0.03466104265465697,
              0.0,
              303.91519667035317,
              0.0,
              0.0,
              1.0,
              -0.0701
            ],
            "sources": [
              "tomo_38_hm"
            ]
          }
        },
        {
          "affine": {
            "name": "Translation",
            "parameters": [
              100.23021139885087,
              13.287015421562778,
              0.0,
              165.3568,
              -13.287015421562778,
              100.23021139885087,
              0.0,
              2243.2063,
              0.0,
              0.0,
              15.423117146329398,
              0.0
            ],
            "sources": [
              "fluorescence-a3-c0",
              "fluorescence-a3-c1",
              "fluorescence-a3-c2"
            ]
          }
        },
        {
          "affine": {
            "name": "MapScaleMat",
            "parameters": [
              -0.0018848506050240675,
              0.009858721157622638,
              0.0,
              0.0,
              0.010070923763591259,
              0.001691011291980681,
              0.0,
              0.0,
              0.0,
              0.0,
              1.0,
              0.0
            ],
            "sources": [
              "fluorescence-a3-c0",
              "fluorescence-a3-c1",
              "fluorescence-a3-c2"
            ]
          }
        },
        {
          "affine": {
            "name": "CLEMRegistration",
            "parameters": [
              1.0,
              0.0,
              0.0,
              203.422,
              0.0,
              1.0,
              0.0,
              238.934,
              0.0,
              0.0,
              1.0,
              0.0
            ],
            "sources": [
              "fluorescence-a3-c0",
              "fluorescence-a3-c1",
              "fluorescence-a3-c2"
            ]
          }
        }
      ],
      "uiSelectionGroup": "mobie-paper",
      "viewerTransform": {
        "normalizedAffine": [
          0.06345607117925063,
          0.0,
          0.0,
          -15.741442519524742,
          0.0,
          0.06344640651225365,
          0.0,
          -19.442105775080794,
          0.0,
          -0.0011074611451334798,
          0.06344640651225365,
          0.3410102495449885],
        "timepoint": 0
      }
    }
```
