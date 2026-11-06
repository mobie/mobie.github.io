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

- **`uri` (mandatory)**: defines the location of a dataset
    - allowed values: absolute or relative file paths or URL to an intensity image, label mask image, or spots table
- `type`: defines the type of dataset; this column can be omitted if all data are intensity images.
    - allowed values:
        - `intensities` (default): normal images
        - `labels`: label mask (segmentation) images
        - `spots`: a table with annotated spots 
    - [example collection containing all three types](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)
- `channel`: the index of the channel that should be opened; necessary to load an image with multiple channels, please add one row per channel (note that MoBIE works with a single channel data model and thus each channel of an image must be loaded individually); this column can be omitted if all your data only has a single channel (e.g. EM data)
    - allowed values: zero based integers
    - [example collection with multiple channels](https://docs.google.com/spreadsheets/d/11dd3WXS1LJRPC4B_omwAPU0JJtFI8WVwdaLJs3L2XSk/edit?usp=sharing)
- `color`: supports various encodings, e.g.
    - `r(0)-g(255)-b(0)-a(255)`
    - `white`, `red`, etc.
- `blend`: defines the blending mode
    - allowed values:
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
- `affine`: additional transformation(s) to apply on display (i.e. where/how the image is rendered in the viewer)
    - supports two modes:
                - **single affine transform (inline)**: row-packed 3x4 affine parameters, preferably semicolon-separated without brackets (comma-separated and/or bracketed forms also supported; see [How to Specify Lists in Table Cells](#how-to-specify-lists-in-table-cells))
                    - e.g. identity: `1;0;0;0;0;1;0;0;0;0;1;0`
                    - e.g. x-shift: `1;0;0;-105.34;0;1;0;0;0;0;1;0`
        - **transform sequence (URI/path)**: points to a transformation table with columns:
            - `type` (required)
            - `value` (required)
            - `name` (optional)
          supported `type` entries in that table: `affine`, `displacement_field_uri`, `elastix_bspline_uri`, `thin_plate_spline_uri`
    - default: no additional transformation
    - if this column is absent, or if its value cannot be parsed/opened, no additional transformation is applied
    - transformations from this column are applied on top of any transformation already found in the image data
    - [example table with affine transforms](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
- `thin_plate_spline`: **legacy** column name for inline BigWarp JSON in the collection table cell
    - preferred approach: use a transformation table referenced via `affine`, with `type = thin_plate_spline_uri`
- `thin_plate_spline_uri`: transformation-table `type` token
    - the corresponding `value` is a URI/path to BigWarp landmark JSON
- `elastix_bspline_uri`: transformation-table `type` token
    - the corresponding `value` is a URI/path to an Elastix TransformParameters file for a BSpline transform
    - note: initial transforms in Elastix files are currently ignored; if needed, convert those to an affine and add them explicitly
- `displacement_field_uri`: transformation-table `type` token
    - the corresponding `value` is a URI/path to a JSON metadata file for a precomputed 3D inverse displacement field
    - currently, a convenient way to create such a file is in Fiji via: `Plugins > MoBIE > Create > Create Inverse Displacement Field From Elastix BSpline...`
- `exclusive`: boolean
  - `true`: when displaying the dataset all other currently displayed datasets will be removed
  - `false` (default): when displaying the dataset it will be shown on top of already displayed datasets
- `name`: free text
    - defines the name of the dataset in the MoBIE user interface
    - necessary if two datasets have the same file name
- `group`: free text
    - creates a new drop-down in the MoBIE UI
    - useful to group data together
- `labels_table`: path to a labels table
    - only considered in conjunction with `type`: `labels`
    - [example labels table](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=890359520#gid=890359520)
    - [supported labels table column naming schemes](https://github.com/mobie/mobie-viewer-fiji/tree/main/src/main/java/org/embl/mobie/lib/table/columns)
- `contrast_limits`: `min;max` or `auto`
    - list syntax: see [How to Specify Lists in Table Cells](#how-to-specify-lists-in-table-cells)
    - e.g., `10;240` or `1000;38000` or `auto`
    - changes the initial display settings
    - `auto` will trigger an auto-contrast algorithm
- `grid`: free text
    - if non-empty, all datasets with the same entry will be layed out into a 2-D grid
    - [example collection with a grid](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- `grid_position`: `x;y`
    - list syntax: see [How to Specify Lists in Table Cells](#how-to-specify-lists-in-table-cells)
    - e.g., `0;0`, `1;0`, `5;2`
    - defines where the dataset is layed out in the grid
    - only considered in conjuction with a non-empty `grid` entry.
    - useful to put several datasets (e.g., image and corresponding labels) into the same grid position
    - [example collection with grid positions](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- `format`: 
    - `OmeZarr`: needed if the path to an OME-Zarr does not contain `.ome.zarr`
    - all other entries will be ignored as the file types will be auto-determined
- `spot_radius`: number larger than zero
    - defines the rendering radius of spots 
    - only considered in for a dataset of `type` `spots`
- `bounding_box`: configures the size of a spot image. E.g., `0.0;0;0-200.5;200;50.3`
    - list syntax: see [How to Specify Lists in Table Cells](#how-to-specify-lists-in-table-cells)
    - only considered in for a dataset of `type` `spots`


The only required column is **uri**, which must contain a valid path to that dataset. This path can be local (File system) or in the cloud (S3 or HTTP).

For a more complete specification of all columns please [read the comments in the code](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java). 

In addition to the specified columns, the table may contain an arbitrary number of additional columns, where you can annotate your respective data sets.

#### How to Specify Lists in Table Cells

Several fields in the table accept **list values** (for example numeric lists or group lists).

##### Supported list syntax

You can write list items using:

- **Semicolon-separated** values (recommended): `a;b;c`
- **Comma-separated** values: `a, b, c`

Optional surrounding brackets are accepted and ignored:

- Parentheses: `(a;b;c)` or `(a, b, c)`
- Square brackets: `[a;b;c]` or `[a, b, c]`
- Curly braces: `{a;b;c}` or `{a, b, c}`

Whitespace around items is ignored, so these are equivalent:

- `1;2;3`
- `1; 2; 3`
- `( 1 ; 2 ; 3 )`

##### Recommendation: prefer semicolon (`;`) without brackets

We recommend using **semicolon-separated lists without enclosing brackets** whenever possible.

Recommended style:

- `1;2;3`
- `views;qc;publication`

Brackets remain optional and equivalent when you prefer them.

Why:

1. A comma can conflict with CSV field separation.
2. In some spreadsheet locale settings (for example certain Excel regional settings), comma-separated values may be interpreted as a **decimal number** instead of two list entries.

##### If you use commas, be careful

If you choose comma-separated lists in a CSV file, make sure the full cell is quoted:

- Correct CSV cell content: `"1,2"` or `"(1, 2)"`
- Without quotes, commas may be treated as column delimiters and break the file.

As an alternative, consider using **tab-separated files (TSV)**, which avoids comma ambiguity in list cells.

##### Examples

- Integer pair (recommended): `3;5`
- Integer pair (optional bracket form): `(3;5)`
- Integer pair (comma version): `"(3, 5)"` in CSV  
- Double list (recommended): `0.1;1.5;3.0`  
- Double list (optional bracket form): `[0.1;1.5;3.0]`  
- Groups (recommended): `views;qc;publication`

### Opening a collection table in Fiji/MoBIE

Within the Fiji menu select: `Plugins > MoBIE > Open > Open Collection Table...`

A user interface will pop up with the following fields:

* `Table Uri`: Location of a MoBIE collection table.
    - This may be a path to a file on your computer or to a "cloud resource" such as an S3 object store, a GitHub URL, or a Google Sheet URL. 
    - The collection table can be provided in a number of formats, including EXCEL, CSV, TSV and Google Sheets. 
    - For Google Sheets simply copy and paste the link that shows in your browser or use the link that you obtain when using Google's sharing functionality. 
* `( S3 Access Key )` & `( S3 Secret Key )`: free text
    - These are optional fields. Use those if the `uri` column of the collection table points to data in a protected S3 bucket.

### Defining complex views

The advantage of the collection table is that it is easy to create. A disadvantage as compared to a traditional MoBIE project is that you cannot define very complex views on your data.

However, you can do the following: After opening a collection table, you can configure a complex view and then right click in the BigDataViewer window and say "Save current view...". It will ask you for the name of this view and importantly also for the file in which you want to save it. Please call this file "mobie-views.json" and save it in the same folder as your collection table. The next time you open the collection table, MoBIE will automatically pick it up and then you can look at the views defined in this file. Note that you can add several views to that file. So next time you want to save a view, simply select that file again as the destination. Please note that any changes in your collection table will probably invalidate those views! Thus, in practice, once you created such a mobie-views.json, you may not change the collection table anymore. 

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

For remote data it is convenient to use Google Sheets as the collection table, as this will allow you to have an entirely cloud based solution that you can readily share with anyone.

Please note that the Google Sheet link must allow **public read access**. 

Here are some Google Sheet collection tables that are pointing to remotely hosted data. They can be opened like this:
-  `Plugins > MoBIE > Open > Open Collection Table...`
    - `Table Uri`: Paste link to the Google Sheet
    - `Data Root`: `PathsInTableAreAbsolute`
    - `Viewing Mode`: `ThreeDimensional`
    - *Leave all other fields empty*


- [IDR hosted multi-channel OME-Zarr v0.5](https://docs.google.com/spreadsheets/d/14HsoEGXnMwzZM_bLASYym8fT7Sq5-THmioytGvQMa7s/edit?gid=0#gid=0)
- [BioImage Archive hosted multi-channel OME-Zarr](https://docs.google.com/spreadsheets/d/11dd3WXS1LJRPC4B_omwAPU0JJtFI8WVwdaLJs3L2XSk/edit?usp=sharing)
- [Correlative 2-D EM, fluorescence and 3-D tomography data](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
    - The same data [as an OME-Zarr Scene](https://ome.github.io/ome-ngff-validator/?source=https://livingobjects.ebi.ac.uk/idr/mobie/clem-scene.ome.zarr)
- [Grid view of OpenOrganelle EM volumes](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- [Grid view of OpenOrganelle EM volumes and organelle segmentations](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- [Large volume EM data with annotated cell segmentation](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)
- [3-D spatial transcriptomics](https://docs.google.com/spreadsheets/d/1BhIzNYZXoSST38vbOrMEMCwrM3y2nyPl9t_9RKOzFbk/edit?usp=sharing) (The genes are initially not visible, because they are in a different z-plane; click on one gene in the table to move the view.)
- [ThinPlateSpline transformed EM volume](https://docs.google.com/spreadsheets/d/1elair242cN5rbYtlODKu5yIscZHQ9O0Lci598-NoY4I/edit?usp=sharing)

#### Learning tips

- In MoBIE collections tables only the `uri` column is mandatory. It can be instructive to remove some or all of the other columns and see what you get. You can then sequentially add back the other columns and observe how the visualisation changes (and/or errors appear).
    - Practically, you can "remove" a column by giving it a name that MoBIE does not recognise, e.g. renaming `affine` (recognised) to `x_affine` (not recognised).

### Creating your own MoBIE collection tables

#### Manually

The motivation of using a table format to specify image collections was that it should be very easy to manually create such tables, for example in spreadsheet software like Excel.
We recommend taking any of the above examples as a starting point and modify them according to your needs.

#### In Fiji

For local image data, you can use `Plugins > MoBIE > Create > Create MoBIE Collection Table...` to get started and then modify or add columns in the table.

#### Using python code

[Here](code/create_mobie_collection_table.py) is a simple example of how to create a MoBIE collection table using pandas in python. 
The example is intended as an inspiration and does not cover every situation. Feel free to copy and adjust to your needs!

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



