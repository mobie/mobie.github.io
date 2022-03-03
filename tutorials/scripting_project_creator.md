## Scripting MoBIE Project Creator

For datasets with many images, it may be more convenient to use the project
creator via a script. Here we provide a few examples for using groovy scripting
within Fiji (this can also be adapted for the other scripting languages within
  Fiji).

### Script editor

In Fiji, click File > New > Script, to open the script editor. Then, in the
menu at the top of the editor, select Language > Groovy.

### Creating a simple project
Here, we create a project folder, and add a dataset and image:

```
import ij.IJ;
import org.embl.mobie.io.ImageDataFormat;
import org.embl.mobie.viewer.command.OpenMoBIEProjectCommand;
import org.embl.mobie.viewer.projectcreator.ProjectCreator;

projectFolder = new File("C:\\Users\\meechan\\Documents\\temp\\test_project")
dataDirectory = new File(projectFolder, "data");
dataDirectory.mkdirs();

try {
    projectCreator = new ProjectCreator(dataDirectory);

    // create a dataset called 'testDataset'
    projectCreator.getDatasetsCreator().addDataset("testDataset");

	// open an example image to add to project
    currentImage = IJ.openImage("http://imagej.nih.gov/ij/images/mri-stack.zip");

    // add image to dataset "testDataset" in project with name "testImage"
    projectCreator.getImagesCreator().addImage( currentImage, "testImage", "testDataset",
                           ImageDataFormat.BdvN5, ProjectCreator.ImageType.image,
                           "images", true )

    // open it in MoBIE
    openMoBIE = new OpenMoBIEProjectCommand();
    openMoBIE.projectLocation = projectCreator.getDataLocation().getAbsolutePath();
    openMoBIE.run();
} catch (IOException e) {
    e.printStackTrace();
}
```

### Datasets

You can create a new empty dataset, with a specific name like so:
```
datasetName = "testDataset"
projectCreator.getDatasetsCreator().addDataset( datasetName );
```

You can rename a dataset like so:
```
oldName = "testDataset"
newName = "newDataset"

// rename 'testDataset' to 'newDataset'
projectCreator.getDatasetsCreator().renameDataset( oldName, newName );
```

You can set which dataset is shown by default in MoBIE like so:
```
datasetName = "testDataset"
projectCreator.getDatasetsCreator().makeDefaultDataset ( datasetName );
```

### Adding ImagePlus images

The main function to add images + segmentations is this one:
```
currentImage = IJ.openImage("http://imagej.nih.gov/ij/images/mri-stack.zip")
imageName = "testImage"
datasetName = "testDataset"
imageFormat = ImageDataFormat.BdvN5
imageType = ProjectCreator.ImageType.image
uiSelectionGroup = "images"
exclusive = false

// add image to project
projectCreator.getImagesCreator().addImage( currentImage, imageName,
          datasetName, imageFormat, imageType, uiSelectionGroup, exclusive )
```
which takes the following parameters (in order):
- image to add, as ImagePlus
- image name
- dataset name
- image format (ImageDataFormat.BdvN5 or ImageDataFormat.OmeZarr)
- image type - ProjectCreator.ImageType.image or ProjectCreator.ImageType.segmentation
- ui selection group name - i.e. name of MoBIE drop-down menu to place view in
- exclusive - Whether to make the view exclusive.

If you want more control over the resolution levels / chunking that the
project creator uses, you can explicitly give these like so:
```
import org.janelia.saalfeldlab.n5.GzipCompression;

resolutions = [ [1,1,1], [2,2,2], [4,4,4] ] as int[][]
subdivisions = [ [64,64,64], [64,64,64], [64,64,64] ] as int[][]
compression = new GzipCompression()

// add image with specific resolution levels and chunks
projectCreator.getImagesCreator().addImage ( currentImage, imageName,
              datasetName, imageFormat, imageType,
              uiSelectionGroup, exclusive, resolutions,
              subdivisions, compression )
```
This takes 3 additional parameters to the function above:
- resolutions - the resolution/downsampling levels to write e.g.
the example above will write one full resolution level,
then one 2x downsampled, and one 4x downsampled. The order is {x, y, z}.
- subdivisions - Chunk size. Must have the same number of entries as 'resolutions'.
e.g. the example above will use a chunk size of (64, 64. 64) for all levels.
The order is {x, y, z}.
- compression - type of compression to use

There are also versions of both of these functions, that allow you to specify
an affine transform for the image. Note that this will be added to the image
view, and will be added on top of the usual scaling coming from imp.getCalibration().
```
import net.imglib2.realtransform.AffineTransform3D;

// create an affine transform that translates by 2 units in x, y and z
sourceTransform = new AffineTransform3D();
sourceTransform.translate(2,2,2);

// add image to project with source transform
projectCreator.getImagesCreator().addImage( currentImage, imageName, datasetName,
                       imageFormat, imageType, sourceTransform, uiSelectionGroup,
                       exclusive )

// add image with specific resolution levels, chunks and source transform
projectCreator.getImagesCreator().addImage ( currentImage, imageName,
              datasetName, imageFormat, imageType,
              sourceTransform, uiSelectionGroup, exclusive,
              resolutions, subdivisions, compression )
```

### Adding bdv format images (N5/OME-ZARR)

If your image is already in a compatible format (N5 / OME-ZARR), then you can
also add this directly to your project e.g. for n5:
```
// use 'copy' add method
addMethod = ProjectCreator.AddMethod.copy
imageFormat = ImageDataFormat.BdvN5

// copy an existing N5 image into project
projectCreator.getImagesCreator().addBdvFormatImage (
          new File("path/to/image.xml"), imageName, datasetName,
          imageType, addMethod, uiSelectionGroup, imageFormat, exclusive )
```

and for ome-zarr:
```
// use 'copy' add method
addMethod = ProjectCreator.AddMethod.copy
imageFormat = ImageDataFormat.OmeZarr

// copy an existing OME-ZARR image into project
projectCreator.getImagesCreator().addBdvFormatImage (
          new File("path/to/image.ome.zarr"), imageName, datasetName,
          imageType, addMethod, uiSelectionGroup, imageFormat, exclusive )
```

This function takes the following parameters (in order):
- image file location - for n5, location of the xml, for ome-zarr,
the location of the .ome.zarr directory.
- image name
- dataset name
- image type - ProjectCreator.ImageType.image or ProjectCreator.ImageType.segmentation
- add method - ProjectCreator.AddMethod.link (leave image as-is, and link to
  this location. Only supported for N5 and local projects),
  ProjectCreator.AddMethod.copy (copy image into project), or
  ProjectCreator.AddMethod.move (move image into project - be careful as this
  will delete the image from its original location!)
- ui selection group name - i.e. name of MoBIE drop-down menu to place view in
- image format (ImageDataFormat.BdvN5 or ImageDataFormat.OmeZarr)
- exclusive - Whether to make the view exclusive.

### Adding remote metadata

You can generate the remote metadata for a specific image format with:
```
signingRegion = "us-west-2"
serviceEndpoint = "https://s3.embl.de"
bucketName = "bucketName"
imageFormat = ImageDataFormat.BdvN5S3 // for OME-ZARR use ImageDataFormat.OmeZarrS3

projectCreator.getRemoteMetadataCreator().createRemoteMetadata(
          signingRegion, serviceEndpoint, bucketName, imageFormat )
```
Note that this will overwrite any existing remote metadata for the
given image format.
