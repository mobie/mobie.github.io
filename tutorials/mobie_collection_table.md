## MoBIE collection tables 

MoBIE collection tables provide a convenient human editable way to define large (correlative) image data sets, including images, segmentation images, segmentation annotations and annotated spots. 

- The below [example collection tables](#example-collection-tables) demonstrate a number of use cases, such as:
    - Inspection of a set of locally stored (i.e. on your computer) images with segmented objects and corresponding object measurements
    - Visualisation of correlative light and transmission and tomography electron microscopy data, where the data is hosted remotely at the [BioImage Archive](http://ebi.ac.uk/bioimage-archive/)
    - Visualisation of a set of segmented 3D electron microscopy datasets from the [open organelle project](https://openorganelle.janelia.org/), hosted remotely at the Janelia Research Farm 
    - Visualisation of 3-D spatial transcriptomics data

- You may skip the below explanations and immediately try it out using the below [quick start](#quick-start) section.

- Watch the last part of [this video](https://youtu.be/GT2LS2NxHoY?t=1083) to obtain a brief overview (the URL already starts at the relevant time point); or check out the [corresponding slide deck](https://zenodo.org/records/18184329) (starting from slide 9). 

### Collection table specification

Each row specifies one dataset, which can be  configured by one of these columns:

- `uri` (mandatory): file path or URL to an image, label mask, or spots table
    - defines the absolute or relative location of a dataset that can be visualised with MoBIE
- `name`: free text
    - defines the name of the dataset in the MoBIE user interface
    - necessary if two datasets have the same file name
- `type`: 
    - `intensities` (default): normal images
    - `labels`: label mask images (aka segmentation images)
    - `spots`: a table with annotated spots 
    - [example collection containing all three types](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)
- `channel`: zero based integers
    - necessary to load an image with multiple channels, please add one row per channel
    - [example collection with multiple channels](https://docs.google.com/spreadsheets/d/11dd3WXS1LJRPC4B_omwAPU0JJtFI8WVwdaLJs3L2XSk/edit?usp=sharing)
- `color`: supports various encodings, e.g.
    - `r(0)-g(255)-b(0)-a(255)`
    - `white`, `red`, etc.
- `blend`: 
    - `sum` (default): image intensities will be displayed in an additive manner
    - `alpha`: images that are displayed later will be rendered "on top" of the previous images; the corresponding opacity can be configured in the user interface
    - [example collection with alpha blending](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
- `view`: free text
    - datasets that are part of the same view (i.e., same free text in the table cell) will be shown together
    - useful to show images together that have been acquired in the same physical coordinate system, e.g. using a tiled acquisition or multi-modal imaging of the same specimen
- `display`: free text
    - all datasets that have the same (non-empty) entry will have a shared display settings UI item
    - useful if you want show several images together in the same `view` that have been acquired with the same microscope settings, e.g. a tiled acquisition of GFP images (in which case you could use "GFP" as the table cell entry)
    - also useful for `grid` layouts (s.b.) where all images may have been acquired with comparable settings
    - [example collection with display column](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- `affine`: row-packed affine transform.
    - e.g., shift along x-axis: `(1,0,0,-105.34,0,1,0,0,0,0,1,0)`
    - [xxample table with affine transforms](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
    - example prompt for AI chat models to learn more: "please explain 3d affine transforms in a 3x4 matrix form, give a few simple examples (translation, rotation, scaling) and explain its row packed serialisation"
- `thin_plate_spline`: BigWarp JSON
    - applies a thin plate spline transformation to the dataset
    - [example colletion with thin plate spline transform](https://docs.google.com/spreadsheets/d/1elair242cN5rbYtlODKu5yIscZHQ9O0Lci598-NoY4I/edit?usp=sharing)
- `exclusive`:
    - `true`: when displaying the dataset all other currently displayed datasets will be removed
    - `false` (default): when displaying the dataset it will be shown on top of already displayed datasets
- `group`: free text
    - creates a new drop-down in the MoBIE UI
    - useful to group data together
- `labels_table`: path to a labels table
    - only considerd in conjuction with `type`: `labels`
    - [example labels table](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=890359520#gid=890359520)
    - [supported labels table column naming schemes](https://github.com/mobie/mobie-viewer-fiji/tree/main/src/main/java/org/embl/mobie/lib/table/columns)
- `contrast_limits`: `(min, max)`
    - e.g., `(10,240)` or `(1000, 38000)`
    - changes the initial display settings
- `grid`: free text
    - if non-empty, all datasets with the same entry will be layed out into a 2-D grid
    - [example collection with a grid](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- `grid_position`: `(x,y)`
    - e.g., `(0,0)`, `(1,0)`, `(5,2)`
    - defines where the dataset is layed out in the grid
    - only considered in conjuction with a non-empty `grid` entry.
    - useful to put several datasets (e.g., image and corresponding labels) into the same grid position
    - [example collection with grid positions](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- `format`: 
    - `OmeZarr`: needed if the path to the OME-Zarr does not contain `.ome.zarr`
    - all other entries will be ignored as the file types will be auto-determined
- `spot_radius`: number larger than zero
    - defines the rendering radius of spots 
    - only considered in for a dataset of `type` `spots`
- `bounding_box`: configures the size of a spot image. E.g., `(0.0,0,0)-(200.5,200,50.3)`
    - only considered in for a dataset of `type` `spots`


The only required column is **uri**, which must contain a valid path to that dataset. This path can be local (File system) or in the cloud (S3 or HTTP).

For a more complete specification of all columns please [read the comments in the code](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java). 

In addition to the specified columns, the table may contain an arbitrary number of additional columns, where you can annotate your respective data sets.

### Opening a collection table in Fiji/MoBIE

Within the Fiji menu select: `Plugins > MoBIE > Open > Open Collection Table...`

A user interface will pop up with the following fields:

* `Table Uri`: Location of a MoBIE collection table.
    - This may be a path to a file on your computer or to a "cloud resource" such as an S3 object store, a GitHub URL, or a Google Sheet URL. 
    - The collection table can be provided in a number of formats, including EXCEL, CSV, TSV and Google Sheets. 
    - For Google Sheets simply copy and paste the link that shows in your browser or use the link that you obtain when using Google's sharing functionality. 
* `Data Root`:
    - `PathsInTableAreAbsolute`: Choose this if the `uri` column in the table contains absolute paths (for cloud resources that is always the case, for files on your computer it may be the case)
    - `UseTableFolder`: Choose this option if the paths in the `uri` column are relative to the location of the collection table. This supports the scenario, where you have all your data organised within some folder structure and the collection table is at the root of this folder structure. This is a very useful setup because it allows you to move or copy the whole folder structure and opening the data via the collection table will still work.
    - `UseBelowRootDataFolder`: Choose this option if the paths in the `uri` column are relative to the location of the root data folder that you can specify below. This supports the scenario, where you have all your data organised within some folder structure and the collection table is, for some reason, not at the root of this folder structure.
    - *Note that in principle we could probably support a mix of local relative and cloud absolute paths; if you need this please [get in touch](https://forum.image.sc/).*
* `( Data Root Folder )`: path to a folder
    - This is an optional field. It is only considered if you chose `UseBelowRootDataFolder` above.
* `Viewing mode`: 
    - `ThreeDimensional`: Choose this is your data also contains 3-D images.
    - `TwoDimensional`: Choose this if all your data is 2-D (it will make your life easier, because this mode avoids getting lost in 3-D while browsing in BigDataViewer).
* `( S3 Access Key )` & `( S3 Secret Key )`: free text
    - These are optional fields. Use those if the `uri` column of the collection table points to data in a protected S3 bucket.

### Example collection tables

#### Local data 

- [Segmented nuclei with measurements tables](https://github.com/mobie/mobie.github.io/raw/refs/heads/master/tutorials/data/collection_tables/segmented_nuclei.zip)
    - Segmentations and measurements tables have been created using [this CellProfiler project](https://github.com/NEUBIAS/training-resources/raw/refs/heads/master/scripts/cellprofiler/segment_2d_nuclei_measure_shape_cp4.2.8.cpproj)
    - Download and unzip the data
    - `Plugins > MoBIE > Open > Open Collection Table...`
        - `Table Uri:` Enter path to `one-image-collection.csv` or `two-images-collection.csv`
        - `Data Root`: `UseTableFolder`
        - `Viewing Mode`: `TwoDimensional`
        - *Leave all other fields empty*

#### Remote data

Here are some Google Sheet collection tables that are pointing to remotely hosted data. They can be opened like this:
-  `Plugins > MoBIE > Open > Open Collection Table...`
    - `Table Uri`: Paste link to the Google Sheet
    - `Data Root`: `PathsInTableAreAbsolute`
    - `Viewing Mode`: `ThreeDimensional`
    - *Leave all other fields empty*

- [BioImage Archive hosted multi-channel OME-Zarr](https://docs.google.com/spreadsheets/d/11dd3WXS1LJRPC4B_omwAPU0JJtFI8WVwdaLJs3L2XSk/edit?usp=sharing)
- [Correlative 2-D EM, fluorescence and 3-D tomography data](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
- [Grid view of OpenOrganelle EM volumes](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- [Grid view of OpenOrganelle EM volumes and organelle segmentations](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- [Large volume EM data, annotated cell segmentation, and some annotated spots](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)
- [3-D spatial transcriptomics](https://docs.google.com/spreadsheets/d/1BhIzNYZXoSST38vbOrMEMCwrM3y2nyPl9t_9RKOzFbk/edit?usp=sharing) (The genes are initially not visible, because they are in a different z-plane; click on one gene in the table to move the view.)
- [ThinPlateSpline transformed EM volume](https://docs.google.com/spreadsheets/d/1elair242cN5rbYtlODKu5yIscZHQ9O0Lci598-NoY4I/edit?usp=sharing)

#### Learning tips

- In MoBIE collections tables only the `uri` column is mandatory. It can be instructive to remove some or all of the other columns and see what you get. You can then sequentially add back the other columns and observe how the visualisation changes (and/or errors appear).
    - Practically, you can "remove" a column by giving it a name that MoBIE does not recognise, e.g. renaming `affine` (recognised) to `x_affine` (not recognised).
- For local image data, you can use `Plugins > MoBIE > Create > Create MoBIE Collection Table...` to get started and then modify or add columns

### Quick start

Make sure to have [MoBIE installed on your computer](installation.md).

Within the Fiji menu select: `Plugins > MoBIE > Open > Open Collection Table...`.

In the user interface that pops up choose:

* `Table Uri`: https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0
* `Data Root`: `PathsInTableAreAbsolute`
* `Viewing mode`: `ThreeDimensional`
* *Leave all other fields empty*

Have fun browsing the data! 

- You can use any of the URL of the above [example collection tables](#example-collection-tables) in the exact same way.
- If you are unsure how to browse the data within MoBIE, [this video](https://www.youtube.com/watch?v=oXOXkWyIIOk&pp=0gcJCQMKAYcqIYzv) should be helpful.
- More videos can be found in the [MoBIE YouTube channel](https://www.youtube.com/@MoBIE-Viewer).
- General [troubleshooting](troubleshooting.md).



