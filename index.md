# Welcome to the tutorials for MoBIE!

The MoBIE Fiji viewer is a [Fiji](https://imagej.net/Fiji) plugin allowing easy exploration
of big multi-modal images and associated tabular data.

**Main Features:**

- Smooth browsing of large image data thanks to [BigDataViewer](https://imagej.net/BigDataViewer)
- Overlay many types of images in the same coordinate system (e.g. electron microscopy, light microscopy,
segmentations...)
- Explore tabular data interactively alongside the images they're derived from
- Easy sharing with colleagues (no need to download the raw images!)
- Easy sharing of points of interest in your data e.g. create bookmarks showing selected
- Image registration directly in MoBIE
views, images and tables for your colleagues to explore
- ... and more!

**Get started with the tutorials below:**

- [Installation](./tutorials/installation.md)

## Opening data

- [Open generic image and segmentation data](./tutorials/open_image_data.md)
- [Open various high content screening data](./tutorials/hcs.md)
- [Open MoBIE collection tables](./tutorials/open_mobie_collections.md)
- [Open MoBIE projects](./tutorials/open_projects.md)

### Advanced opening features

- [Opening MoBIE projects from branches and with credentials](./tutorials/branches_and_credentials.md)
- [Open a MoBIE project (expert mode)](./tutorials/expert_mode.md)
- [Using MoBIE from the command line](./tutorials/cli.md)

## Exploring image and segmentation data 

- [Exploring images](./tutorials/exploring_images.md)
- [Exploring segmentations and tables](./tutorials/exploring_segmentations.md)
- [Grid views & image region tables](./tutorials/image_grids_and_tables.md)
- [Volume rendering using BigVolumeViewer](./tutorials/bigvolumeviewer.md)
- [Locations and views](./tutorials/views_and_locations.md)
- [Importing and exporting tables](./tutorials/importing_and_exporting_tables.md)
- [Creating your own views](./tutorials/creating_your_own_views.md)

## Image registration and annotation 

- [Volume registration tutorial](./tutorials/volume_registration.md)
- [Annotation tutorial](./tutorials/annotation_tutorial.md)
- [More features](./tutorials/more_features.md)

## Creating a MoBIE project

Please note that creating a MoBIE project is somewhat involved. For many cases, a [MoBIE collection table](./tutorials/mobie_collection_table.md) will do the job and is  easier to create and maintain.

- [Scripting Project Creation in Python](https://github.com/mobie/mobie-utils-python?tab=readme-ov-file#mobie-utils-python)
- [Project Creator GUI in Fiji](./tutorials/mobie_project_creator.md)
- [Scripting Project Creation in Fiji](./tutorials/scripting_project_creator.md)
- [MoBIE project specification](./specs/mobie_spec.md)

## Use-cases and example projects

Most of the examples in the tutorial are from [Whole-body integration of gene expression and single-cell morphology](https://www.sciencedirect.com/science/article/pii/S009286742100876X), where MoBIE is used to visualize a EM volume of a *Platynereis dumerilii* larva, derived segmentations and gene expression profiles.
MoBIE supports several other data modalities and combinations thereof, for example:

- [Correlative light and electron microscopy](./use-cases/clem.md)
- [High-throughput microscopy](./use-cases/htm.md)
- [3D light microscopy timeseries](./use-cases/timeseries.md)
- [Spatial transcriptomics](./use-cases/spatial_transcriptomics.md)

## Live demonstrations

The MoBIE functionality is also demonstrated in a series of videos:
- [MoBIE core functionality](https://youtu.be/oXOXkWyIIOk)
- [Creating MoBIE projects in Fiji](https://youtu.be/3oP3t6elsQU)
- [Image Registration in MoBIE](https://youtu.be/jKlM68lrhso)
- [Interactive user annotation](https://youtu.be/M-QUE-Qh97w)
- [Timeseries in MoBIE](https://youtu.be/Md4PbK50NE0)
- [Spatial Transcriptomics data in MoBIE](https://youtu.be/1dDaxOAZ9Sg)

There is also a [NEuBIAS BigData Seminar](https://youtu.be/CZpaTCuSQao?t=2868) introducing MoBIE.

## Citation

If you use MoBIE in your research please cite [the MoBIE Nature Methods publication](https://www.nature.com/articles/s41592-023-01776-4).

## Contact

For questions or issues about MoBIE, please open a topic in the [image.sc](https://forum.image.sc/) forum using the tag `mobie`. For specific technical issues or bugs, you can also open an issue on [github](https://github.com/mobie/mobie-viewer-fiji).
