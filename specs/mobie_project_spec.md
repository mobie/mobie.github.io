# MoBIE project and dataset specification

A `project` groups data, for example from the same series of experiments, that can be accessed by the MoBIE viewer. It contains one or multiple `datasets`.
A `dataset` contains data that can be explored *jointly* in the MoBIE viewer.

## Project

Project and associated datasets are stored in a directory structure where the project corresponds to the root directory.
This directory must contain a `datasets.json` file, which lists the available datasets and determines the default dataset that
will be opened when starting the MoBIE viewer for this project and it must contain at least one dataset directory.
The dataset directory names and the names in `datasets.json` must be identical.

Below you can find an example directory structure and the corresponding `datasets.json`.
This example was slightly adapted from the [zebrafish-lm project](https://github.com/mobie/zebrafish-lm-datasets).

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

TODO add spec once changes to views / bookmarks are done

TODO this will partly change now with the changes discussed for the bookmark / view layout,
which will be relevant for images.json and bookmarks

```
actin/
├── images
│   ├── images.json
│   ├── local
│   └── remote
├── misc
│   └── bookmarks
└── tables
    ├── membrane-00E41C184C_lynEGFP_seg
    ├── membrane-2BDB74A7D6_lynEGFP_seg
    └── membrane-F80ACE04D5_lynEGFP_seg
```

## Local & remote storage

TODO explain

MoBIE projects can be hosted on
- filesystem:
- s3 compatible object store:
- github:
