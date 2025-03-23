## Select Box

The "Select Box" tools allows you to select a 3-D box, using the "TransformedBox" code of big. Use cases include documenting a region of biological interest or selecting a region to be further processed in a correlative microscopy setting. 

### Input

The **size** of the box can be interactively changed using the graphical user interface of the tool. 

The **rotation** however is fixed to be aligned with the current viewing axes. Thus, to set the box rotation you need to configure the viewing axes *before* starting the tool, using the usual [BigDataViewer functionality](https://imagej.net/plugins/bdv/). In particular, it may sometimes be useful to align the box with the axes of one specific image. To achieve this, press `P` to show the BigDataViewer control panel and check the image of interest as the "current" one. Then press `Shift + Z` (or `X` or `Y`) to align the viewer with one of the image axes.

### Output 

The output of this tool is the location of the box, written in the log window. 

The box location is given in the following way:

1. The 3-D **center** location in the global (physical) coordinate system
1. The 3-D **size** of the box in the global (physical) units
1. An **box affine transformation** that encodes the box location, size and rotation in global (physical) units

The box affine transformation is constructed such that you can locate any voxel within the box in the global coordinate system by applying the affine transform to voxel within the interval `[ 0, 0, 0 ] - [ 1, 1, 1 ]`.

### Notes

- Have a look at the [source code](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/command/context/BoxSelectionCommand.java).




