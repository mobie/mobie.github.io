## High content screening

MoBIE allows one to arrange many images into nested grids. This feature makes it possible to visualise high content screening (HCS) data, where a plate layout consists of a grid of wells, where each well consists of a grid of sites, which are the actual microscopy images.

Note that we previously build Fiji's [PlateViewer plugin](https://github.com/embl-cba/plateviewer#plateviewer) for visualisation of such HCS data. However, we plan to stop developing the PlateViewer plugin and instead aim to move all functionality to MoBIE, which has a more powerful and versatile backend.

### Supported HCS file naming schemes

MoBIE builds a grid view of wells and sites by parsing the HCS file names, which typically contain information about the channel, well and site. We are still working on supporting more file naming schemes. Please let us know if your naming scheme is not net supported.

#### Operetta (Harmony 4)

Regular expression:

`".*(?<"+WELL+">r[0-9]{2}c[0-9]{2})f(?<"+SITE+">[0-9]{2})p[0-9]{2}.*-ch(?<"+CHANNEL+">[0-9])sk.*.tiff$"`

Example file name and regular expression matching:

`r01c01f04p01-ch1sk1fk1fl1.tiff : WELL = r01c01, SITE = 04, CHANNEL = 1`


### Current limitations

At the moment MoBIE can only load and display one plate at a time. Please let us know if you need to visualise multiple plates in parallel.
