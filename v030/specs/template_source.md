## <a name="source"></a>Source

A `source` consists of an image (volume, timeseries) and optionally associated tabular data. 
Two different types of sources are supported:
- `image`: intensity images corresponding to the "primary" data, e.g. electron microscopy or light microscopy images.
- `regions`: annotations for regions in the image (e.g. positions in a grid view). For reference in `regionDisplays`, see  [this section](#view-source-annotations) for details.
- `segmentation`: label masks corresponding to segmented objects labeled by integer ids, e.g. cell or ultrastructure segmentations.
- `spots`:  point-like data, corresponding to a table with spot coordinates and associated measurements. For example gene detections in spatial transcriptomics.

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
The tables should be stored as tab separated values `.tsv` files; they may also be stored as comma separated values (`.csv`).

The default segmentation table (which must be stored as `default.tsv` in the corresponding table folder, see also [dataset specification](#dataset)) must contain the columns `label_id`, `anchor_x`, `anchor_y`, `anchor_z`,
`bb_min_x`, `bb_min_y`, `bb_min_z` and `bb_min_x`, `bb_min_y`, `bb_min_z`. For two-dimension data the columns `anchor_z`, `bb_min_z` and `bb_max_z` must be omitted. The `anchor` columns specify a reference point for the object corresponding to this row. It will be centered
when the corresponding obejct is selected. The `bb_min` and `bb_max` columns specify the start and stop of the bounding box for the object. Both anchor and bounding box coordinates must
be given in phyisical units. The table may contain additional columns.

Additional segmentation tables must contain the column `label_id` and may contain arbitraty additional columns.
The `label_id`s in the additional tables may be incomplete, but they must not contain ids not present in the default table.
For example, given `label_id`s `[1, 2, 3, 4, 5]` in the default table the `label_id`s `[1, 2, 3, 4, 5]` or `[1, 3, 4]` are valid but `[1, 3, 4, 7]` is invalid.
The label id `0` is reserved for the background and must not be listed in any of the tables.

See an example segmentation default table for 2d data for 8 objects:
```tsv
label_id    anchor_x    anchor_y    bb_min_x    bb_min_y    bb_max_x    bb_max_y
1.0 49.78   41.25   8.7 45.23   3.36    56.053  44.24
2.0 42.79   40.06   9.0 38.29   3.81    48.513  43.55
3.0 52.79   44.33   9.9 48.41   3.81    56.946  47.02
4.0 57.90   42.95   7.8 53.77   3.59    62.204  45.63
5.0 47.19   45.17   9.8 43.45   4.49    51.490  47.91
6.0 40.31   41.75   9.9 37.00   4.71    46.430  44.84
7.0 64.68   43.91   8.4 60.12   4.71    70.439  46.72
8.0 35.57   43.39   10. 30.55   4.93    40.676  46.03
```

The color scheme used to display the segmentation can also be loaded from a table, see `colorByColumn` in the [view metadata](#view-metadata). In order to set an explicit color map, the field `color` may be set to `argbColumn`. In this case, the values in the column must follow the format `alpha-red-green-blue`, e.g. `255-0-0-255`.

Data for a spot source is defined by a table. This table must contain the column `spot_id`, which identifies each spot in the image. It must also contain the columns `x`, `y` and `z` (`z` is omitted in the case of 2d data). These three columns give the coordinates for each spot in the physical coordinate space. Otherwise the spot tables follow the same rules as segmentation tables.

Region tables also have an associated table. It is described in further detail [here](#view-source-annotations) 


### <a name="source-metadata"></a>Source Metadata

The metadata for the sources of a dataset is specified in the field `sources` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`sources` contains a mapping of source names to [source metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/source.schema.json).
The source metadata has the following elements (see below for an example json):

<!---
Don't add anything manually after this line. The example source metadata will be generated automatically when running
scripts/generate_spec_description.py
-->
