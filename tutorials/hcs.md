## High content screening

MoBIE allows one to arrange many images into nested grids. This feature makes it possible to visualise high content screening (HCS) data, where a plate layout consists of a grid of wells, where each well consists of a grid of sites, which are the actual microscopy images.

We already used this feature to [visualise data from a SARS-CoV-2 microscopy screen](https://mobie.github.io/use-cases/htm.html). However, this required re-saving the data as a MoBIE project.

We are now adding support for directly opening HCS data as it is produced by HCS microscopes. This is convenient as one does not need to resave the data, however it may be less responsive as the data produced by such microscopes typically lacks chunking and lacks scale pyramids.

Note that we previously build Fiji's [PlateViewer plugin](https://github.com/embl-cba/plateviewer#plateviewer) for visualisation of such HCS data. However, we plan to stop developing the PlateViewer plugin and instead aim to move all functionality to MoBIE, which has a more powerful and versatile backend.

### Usage

In Fiji select `Plugins › MoBIE › Open › Open HCS Dataset...` and browse to a folder that contains one HCS plate. If the naming scheme is among the supported ones (s.b.) it will be automatically detected and a plate view will open.

### Supported HCS file naming schemes

MoBIE builds a grid view of wells and sites by parsing the HCS file names, which typically contain information about the channel, well and site.

#### Operetta (Harmony 4)

Regular expression:

`".*(?<"+WELL+">r[0-9]{2}c[0-9]{2})f(?<"+SITE+">[0-9]{2})p[0-9]{2}.*-ch(?<"+CHANNEL+">[0-9])sk.*.tiff$"`

Example file name and regular expression matching:

`r01c01f04p01-ch1sk1fk1fl1.tiff : WELL = r01c01, SITE = 04, CHANNEL = 1`

### Current limitations

One can only load and display one plate at a time. Please let us know if you need to visualise multiple plates in parallel and we will consider adding this functionality.

The HCS naming scheme must be among the supported ones (s.a.), one cannot enter an own naming scheme. Please contact us if your naming scheme is not supported, and we will add it for you.

