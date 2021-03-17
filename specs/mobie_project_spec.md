# MoBIE project and dataset specification

A `project` groups data, for example from the same series of experiments, that can be accessed by the MoBIE viewer. It must contain at least one `dataset`.
A `dataset` contains data that can be explored *jointly* in the MoBIE viewer.

## Project

The `project` and its associated `datasets` are stored in a directory structure with the project corresponding to the root directory.
This directory must contain a `datasets.json` file, which lists the available datasets and specifies the default dataset, 
which will be opened when starting the MoBIE viewer for this project. The project must contain at least one dataset directory.
The dataset directory names and the names in `datasets.json` must be identical.

See an example project structure, slightly adapted from the [zebrafish-lm project](https://github.com/mobie/zebrafish-lm-datasets), and the corresponding `datasets.json` below.
```
zebrafish-lm/
├── datasets.json  # contains list of available datasets and the default dataset
├── actin
├── cisgolgi
├── lysosomes
├── membrane
├── nuclei
└── trans_golgi
```

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
  "defaultDataset": "membrane"
}
```

## Dataset

Each dataset consists of a root directory, which must include the file `sources.json` listing the available image sources for this dataset according to the [source metadata specification](TODO proper link).
It should contain the subdirectories `images`, containing the image (meta)data, `tables`, containing the table data and must contain the directory `misc`, containing additional data associated with this dataset.
Note that the location of image and table data is determined in `sources.json` and it is thus possible to choose a different directory structure than `images/` and `tables/` to store them,
but the `images/`, `tables/` layout is recommended for consistency with other MoBIE projects and assumed throughout this specification.

The `images` directory contains the xml files specifying image sources, see [Image Data specification](TODO link) for details.
It may contain additional subdirectories to organise these files; by convention the files specifying local and remote image sources are often separated into `images/local` and `images/remote`.

The `tables` directory contains all data for tables assoicated with segmentations or grid views. All tables associated with one segmentation or view, must be located in the same subdirectory.
and this directory must contain a table `default.tsv`, which is the table loaded by default for this object. It may contain additional tables. 
See the [table data specification](TODO proper link) for the table data format.

The `misc` directory must contain the subdirectory `bookmarks` with the file `default.json`, which specifies the default view according to the [view metadata specification](TODO proper link).
It may contain the file `leveling.json`, which specifies the "natural" orientation of the dataset and other subdirectories or files that are associated with the dataset.

See an example dataset structure for one of the zebrafish-lm project's dataset below.
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
    ├── membrane-00E41C184C_lynEGFP_seg
    ├── membrane-2BDB74A7D6_lynEGFP_seg
    └── membrane-F80ACE04D5_lynEGFP_seg
```

## Local & remote storage

MoBIE projects can be either stored locally or hosted on a remote object store.
Currently, MoBIE supports the following storage options:
- filesystem: supports image sources and metadata
- s3 object store: supports image sources and metadata; public and private buckets are supported
- github: supports metadata, image sources must be loaded from object store

This enables different combinations of hosting a project, see also the figure below:
<ol type="a">
<li>only on filesystem: project is only available locally; this is the best mode for development.</li>
<li>only on s3 object store: project is self-contained in object store and can be shared with collaborators privately (using a privat bucket) or shared publicly (using a public bucket).</li>
<li>on github and s3 object store: the metadata is stored on github, which also serves as entrypoint for the viewer. The image sources are stored on the s3 bucket. This set-up has the advantage that metadata is under version control.</li>
</ol>

![figure](../assets/hosting.png)
