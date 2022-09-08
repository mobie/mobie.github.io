# High-throughput microscopy

High-throughput (screening) microscopy reference light microscopy techniques where a large number of images are taken, usually by imaging *wells* that are distributed on a *plate*.
This technique is often used to study samples under different conditions, each well potentially representing a different condition, for example for drug screening, diagnostic tests or knockout studies.
Here we showcase the [covid-if-project](https://github.com/mobie/covid-if-project) that visualizes data from an immunofluorescence assay to measure the SARS-CoV-2 antibody response in human serum.


## Data & project set-up

The data for this project comes from the publication [Microscopy-based assay for semi-quantitative detection of SARS-CoV-2 specific antibodies in human sera](https://doi.org/10.1002/bies.202000257), which provides several plates of immunofluorescence data.
We have imported one plate for demonstration purposes. Each position in the plate contains thre image channels, a nucleus channel, a serum channel and a virus marker channel, as well as derived nucleus and cell segmentations.
The assay derived from this data measures the SARS-CoV-2 antibody response via the intensity ratio between infected and non-infected cells.
These ratios and other relevant well,- image- and cell-level data are provided.

We converted the data from the original publication, which is stored in hdf5, to the MoBIE format using the [MoBIE python library](https://github.com/mobie/mobie-utils-python/tree/master/mobie/htm); the scripts that call the library are [here](https://github.com/mobie/covid-if-project/blob/main/add_plate.py).
The project metadata is stored [github](https://github.com/mobie/covid-if-project) and the image data stored on the EMBL S3 server.


## Exploring the project

TODO: with MoBIE spec v3 can we open the whole plate directly???
(Would making this part nicer and easier to write, because we don't have the toy data opening in the beginning)
