## Registration

There are several tools that enable to spatially transform one or several of the shown images. Typically, the reason to do this is to "register" images in a multi-modal imaging setting, thus the tools are called "registration" (and not "transformation").

### Methods

TODO

### Output 

While all registration tools work differently and require different inputs, the output are always transformed images. MoBIE will not re-save the image voxel data, but only save the transformation as a new "view" on the voxel data. This new view will be added to the MoBIE UI in a **group** of your choice, the **name** of the view will be the name of the input image with a postfix of your choice, e.g. "-transformed".  

In addition,  one must choose whether and where this view should be saved. Currently, three options are supported:

- "Current Project": Traditionally, images in MoBIE are loaded from a JSON based [MoBIE project](specs/mobie_spec.dmd) to which new views can be saved. Currently, selecting this option when the data has not been loaded from a MoBIE project will lead to an error message.
- "External File": In recent years several new ways have been added to load data into MoBIE, which do not follow this project structure. In such cases views can be saved into a stand-alone "external" JSON file that contains the view. Even if you are loading data from a MoBIE project you sometimes may not want to alter the project; also then saving the view to an external file can be a good option.
- "Don't Save": This option can be a good choice when you are exploring different registrations, but do not want to store those trials.



