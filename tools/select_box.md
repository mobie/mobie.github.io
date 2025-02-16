## Select Box

The "Select Box" tools allows you to select a 3-D box, using the "TransformedBox" code of big. Use cases include documenting a region of biological interest or selecting a region to be further processed in a correlative microscopy setting. 

The **size** of the box can be interactively changed using the graphical user interface of the tool. The **rotation** however is fixed to be aligned with the current viewing axes. Thus, to set the box rotation you need to configure the viewing axes *before* starting the tool, using the usual [BigDataViewer functionality](https://imagej.net/plugins/bdv/). In particular, it may sometimes be useful to align the box with the axes of one specific image. To achieve this, press `P` to show the BigDataViewer control panel and check the image of interest as the "current" one. Then press `Shift + Z` (or `X` or `Y`) to align the viewer with one of the image axes.

Currently, the only **output** of this tool is the location of the box, written in the log window. 

The box location is given in the following way:

1. The 3-D **center** location in the global (physical) coordinate system
1. The 3-D **size** of the box in the global (physical) units
1. An **affine transformation** that encodes the box rotation

Note that the center is just given for convenience, but could also be computed using the box size and the affine transformation, via `center = affine( size[0]/2,  size[1]/2,  size[2]/2 )`. To locate any voxel within the box in the global coordinate system, you may affine transform any voxel within the interval `[ 0, 0, 0 ]-[ size[0], size[1], size[2] ]`.


### References

- The box is implemented using this code: https://github.com/bigdataviewer/bigdataviewer-core/tree/master/src/main/java/bdv/tools/boundingbox



