# 3D light microscopy timeseries

Light-microscopy images or volumes taken over time are commonly used to study dynamical problems, for example in developmental biogly.
Here we showcase the [arabidopsis-root-lm-project](https://github.com/mobie/arabidopsis-root-lm-project) that visualizes a timeseries of a growing *Arabidopsis thaliana* root imaged with lightsheet microscopy.


## Data & project set-up

The data for this project comes from the publication [Accurate and versatile 3D segmentation of plant tissues at cellular resolution](https://elifesciences.org/articles/57613).
It contains a timeseries of lightsheet volumes with a cell membrane and nucleus channel, as well as derived cell and nucleus segmentations and lineage tracking for selected cells.

The data from the original publication was converted to the MoBIE data format using the [MoBIE python library](https://github.com/mobie/mobie-utils-python/tree/master/mobie/htm), which is called in [this script](https://github.com/mobie/arabidopsis-root-lm-project/blob/main/create_project.py). 
The project metadata is stored on [github](https://github.com/mobie/arabidopsis-root-lm-project) and the image data is stored on the EMBL S3 server.


## Exploring the project


