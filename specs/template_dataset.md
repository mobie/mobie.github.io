## <a name="dataset"></a>Dataset

A `dataset` consists of a root directory, which must contain the file `dataset.json` with a valid [dataset schema](https://github.com/mobie/mobie.github.io/tree/master/schema/dataset.schema.json).
It should contain the subdirectories `images`, containing the image data, `tables`, containing the table data and may contain the directory `misc`, containing additional data associated with this dataset.
Note that the location of image and table data is determined in `dataset.json` and it is thus possible to choose a different directory structure than `images/` and `tables/` to store them,
but the layout using `images/` and `tables/` is recommended for consistency with other MoBIE projects and assumed throughout this document.

The `images` directory contains the metadata files describing the image data, see [data specification](#data) for details.
It may contain additional subdirectories to organise these files. By convention the files for different data formats are often separated into folders named accordingly, e.g. `images/bdv-n5` and `images/bdv-n5-s3`.

The `tables` directory contains all tabular data assoicated with segmentation, spot or region sources (see the [data specification](#data) for details)
The tables associated with a segmentation or view, must all be located in the same subdirectory. This subdirectory must contain a default table, which should be called `default.tsv`, and may contain additional tables. 
See the [table data specification](#table-data) for details on how tables are stored.

The `misc` directory may contain the subdirectory `views` with additional views stored in json files according to the [views spec](https://github.com/mobie/mobie.github.io/tree/master/schema/views.schema.json).

As an example see the dataset directory structure for the `hela` dataset of the clem project:
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
