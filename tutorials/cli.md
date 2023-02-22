## MoBIE CLI

**Experimental:** MoBIE can also be used from the command line to open images, segmentations and segmentation tables.
This data can be stored in many different data formats, and does not have to be organized according to the MoBIE project format.


### Installation

You can install the MoBIE CLI via conda:

```
$ conda create -n mobie -c conda-forge mobie
```

Note that the first start-up (running the `mobie` command) may be slow because additional dependencies are downloaded.


### Usage

Once installed, the CLI can be used to open single images, segmentations and tables:
```
$ mobie -i my-image.tif -s my-segmentation.tif -t my-table.csv
```

or multiple images, segmentations and tables using wildcards:
```
$ mobie -i "*-im.tif" -s "*-seg.tif" -t "*.csv"
```

You can check all options by just running `$ mobie` (here's the current options:)
```
(mobie) tischer@mac-almf13 Documents $ mobie
Usage: mobie [-hV] [-p=<project>] [-i=<images>]... [-s=<segmentations>]...
             [-t=<tables>]...
Visualise multi-modal big image data, see https://mobie.github.io/
  -h, --help                Show this help message and exit.
  -i, --image=<images>      intensity image, e.g. -i "/home/image.tif"
  -p, --project=<project>   project, e.g. -p "https://github.
                              com/mobie/platybrowser-datasets"
  -s, --segmentation=<segmentations>
                            segmentation label mask image, e.g. -s
                              "/home/labels.tif"
  -t, --table=<tables>      segments feature table, e.g. -t "/home/features.csv"
  -V, --version             Print version information and exit.
```
