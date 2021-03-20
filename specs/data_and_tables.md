# MoBIE image data, metadata and table specification

## Image data

MoBIE supports three different types of image data:
- `image`: intensity images corresponding to the "primary" data, e.g. electron microscopy or light microscopy images
- `segmentation`: label masks corresponding to segmented objects labeled by integer ids, e.g. cell or ultrastructure segmentations

The image data is stored in a multi-dimensionl, chunked data format.
MoBIE primarily supports the [n5](https://github.com/saalfeldlab/n5) data format, using the [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) to represent timepoints and multi-scale image pyramids.
In addition, MoBIE supports [HDF5](https://www.hdfgroup.org/solutions/hdf5/), again using the [bdv hdf5 format](https://imagej.net/BigDataViewer.html#About_the_BigDataViewer_data_format); however this format can only be read locally and **does not** support remote access from an object store.
There is also experimental support for the emerging [ome ngff](https://ngff.openmicroscopy.org/latest/).

## Table data

MoBIE supports tables associated with segmentations, where each row corresponds to properties of an object in the segmentation and grid views (see below), where
each row corresponds to properties of a source in the grid view.
The tables should be stored as tab separated values `.tsv` files; they may also be stored as comma separated values `.csv`.

The default segmentation table (which is stored in `default.tsv`, see also [dataset specification](TODO link)) must contain the columns `label_id`, `anchor_x`, `anchor_y`, `anchor_z`,
`bb_min_x`, `bb_min_y`, `bb_min_z` and `bb_min_x`, `bb_min_y`, `bb_min_z`. The `anchor` columns specify a reference point for the object corresponding to this row, that will be centered
when the corresponding obejct is selected. The `bb_min` and `bb_max` columns specify the start and stop of the bounding box for the object. Both anchor and bounding box coordinates must
be specified in phyisical units. It may contain additional columns.
Additional segmentation tables must contain the column `label_id` and may contain arbitraty additional columns.
The label id `0` is reseved for background and should not be listed in the table.
See an example segmentation default table for 8 objects with additional column `n_pixels` listing the number of pixels of the objects.
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

The grid view tables must contain the column `source_name` and may contain additional arbitrary columns.
See an example grid view table for 4 images which specifies the presence of different organelles for each image.
```tsv
source_name mitochondria    vesicles    golgi   er
imageA  1   0   1   0
imageB  0   1   1   0
imageC  0   0   1   1
imageD  1   0   1   1
```


## Metadata

Two different types of metadata are specified: source metadata, that describes the storage and type of an image source and view metadata, that 
describes the viewer state for one or multiple sources.

### Source Metadata

The sources and their metadata are specified in the `sources.json` file located in the dataset's image folder (see also [dataset specification](TODO link)) with
the source names acting as keys and the following values: 
- `imageLocation`: location of the bdv.xml file(s) for this image. This field must be present and at least one of `local` or `remote` must be given.
    - `local`: xml file for opening this image source local filesystem
    - `remote`:  xml file for opening this image source from object store
- `menuItem`: name of the dropdown menu in GUI for this source. This field must be present and must have the form `"menu-name/source-name"`.
- `tableRootLocation`: root directory for the tables associated for this source. This field may be present for segmentation and must not be present for other types of sources.
- `type`: type of the source. This field must be present and must be one of `image` or `segmentation`.
- `view`: the default view for this source, specified according to the view metadata format (see below). This field must be present.

All locations are relative to the dataset root directory.
See example for a `sources.json` with an image and segmentation source, ommiting the view specification for brevity:
```json
{
    "myImage": {
        "imageLocation": {
            "local": "images/local/my_image.xml",
            "remote": "images/remote/my_image.xml"
        },
        "menuItem": "images/the-image",
        "type": "image",
        "view": {}
    },
    "mySegmentation": {
        "imageLocation": {
            "local": "images/local/my_segmentation.xml",
            "remote": "images/remote/my_segmentation.xml"
        },
        "menuItem": "segmentations/the-segmentation",
        "type": "segmentation",
        "view": {}
    }
}
```

### View Metadata

**sourceDisplays:**

- `imageDisplays`
    - `color`
    - `contrastLimits`
    - `name`
    - `sources`: the list of sources always uses the keys used in `sources` of json as names
- `segmentationDisplays`
    - `alpha`
    - `color` (incl. multi-color LUTs such as "Glasbey")
    - `colorByColumn`
    - `selectedSegmentIds`: format is ["sourceName-timepoint-labelId", ...]
    - `showSelectedSegmentsIn3d`
    - `name`
    - `sources`
    - `tables` (currently only additional tables, to be added to the default table)

```json
{
    "sourceDisplays": [
        {
            "imageDisplays": {
                "color": "white",
                "contrastLimits": [0.0, 255.0],
                "name": "imageGroup1",
                "sources": ["myImage1", "myImage2"]
            }
        },
        {
            "segmentationDisplays": {
                "alpha": 0.75,
                "color": "glasbey",
                "name": "segGroup1",
                "sources": ["mySegmentation"]
            }
        }
    ]
}
```

**sourceTransforms:**

- `affine`
    - `name`
    - `parameters`
    - `sources`
    - `timepoint`: if no timepoint is specified, this transformation is valid for all timepoints (same for other transformations)
- `autoGrid`
    - `name`
    - `sources`
    - `tableRootLocation`
    - `timepoint`

```json
{
    "sourceTransforms": [
        {
            "affine": {
                "name": "myAffineTransform0",
                "parameters": [10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                "sources": ["myImage1", "mySegmentation"],
                "timepoint": 0
            }
        },
        {
            "affine": {
                "name": "myAffineTransform1",
                "parameters": [8.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                "sources": ["myImage1", "mySegmentation"],
                "timepoint": 1
            }
        }
    ]
}
```

**viewerTransform:**

- `normalizedAffine`
    - `name`
    - `parameters`
- `position`
- `timepoint`

```json
{
    "viewerTransform": {
        "timepoint": 0
    }
}
```
