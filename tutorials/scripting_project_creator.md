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

    // add image to project
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
