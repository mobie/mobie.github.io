## MoBIE collection tables 

MoBIE collection tables provide a convenient human editable)way to define large (correlative) image data sets, including images, segmentations, segmentation annotations and annotated spots (e.g. useful for browsing gene locations in [spatial transcriptomics data](https://www.youtube.com/watch?v=1dDaxOAZ9Sg)). 

Watch the last part of [this talk](https://youtu.be/GT2LS2NxHoY?t=1083) to obatin a short overview (the URL already starts at the relevant time point).

If you can't wait to try this out, you may skip the explanations and immediately scroll to the below "Quick start" section.

### Collection table specification

Each row specifies one dataset, which are be specified by a number of predefined columns. 

Defined column names:
- `uri`: **mandatory**, file path or URL to an image
- `name`: free text
- `type`: 
    - `intensities` (default): normal images
    - `labels`: label mask images (aka segmentation images)
    - `spots`: a table with annotated spots 
    - [example collection containing all three types](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)
- `channel`: zero based integers; necessary to load an image with multiple channels, please add one row per channel
    - [example collection with multiple channels](https://docs.google.com/spreadsheets/d/11dd3WXS1LJRPC4B_omwAPU0JJtFI8WVwdaLJs3L2XSk/edit?usp=sharing)
- `color`: e.g., `r(0)-g(255)-b(0)-a(255)` or `white`, `red`, etc.
- `blend`: `sum`, `alpha`
- `affine`: row-packed affine transform.
    - e.g., shift along x-axis: `(1,0,0,-105.34,0,1,0,0,0,0,1,0)`
    - [example table with affine transforms](https://docs.google.com/spreadsheets/d/1hj_JKnBLp1nJzeSG6mcL6INIsFH2meKzNx59vmYL53Y/edit?gid=0#gid=0)
- `thin_plate_spline`: BigWarp JSON
    - [example colletion with thin plate spline transform](https://docs.google.com/spreadsheets/d/1elair242cN5rbYtlODKu5yIscZHQ9O0Lci598-NoY4I/edit?usp=sharing)
- `view`: free text
- `exclusive`: `true`, `false`
- `group`: free text
- `labels_table`: path to a labels table; only valid in conjuction with `type` `labels`
    - [example labels table](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=890359520#gid=890359520)
    - [supported labels table column naming schemes](https://github.com/mobie/mobie-viewer-fiji/tree/main/src/main/java/org/embl/mobie/lib/table/columns)
- `contrast_limits`: e.g., `(10,240)`
- `grid`: free text; the name of the grid (ignored if empty)
    - [example collection with a grid](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- `grid_position`: e.g., `(0,0)`, `(1,0)`, `(5,2)`; only valid in conjuction with a non-empty `grid` table cell.
    - useful to arrange several images (or labels) into the same grid layout
    - [example collection with grid positions](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- `display`: free text
- `format`: `OmeZarr`
    - needed if the path to the OME-Zarr does not contain `.ome.zarr`
- `spot_radius`: number
- `bounding_box`: configures the size of a spot image. E.g., `(0.0,0,0)-(200.5,200,50.3)`


The only required column is **uri**, which must contain a valid path to that dataset. This path can be local (File system) or in the cloud (S3 or HTTP).

For a more complete specification of all columns please [read the comments in the code](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java). 

In addition to the specified columns, the table may contain an arbitrary number of additional columns, where you can annotate your respective data sets.

### Opening a collection table in Fiji/MoBIE

Within the Fiji menu select: `Plugins > MoBIE > Open > Open Collection Table...`

A user interface will pop up with the following fields:

* `Table Uri`: This is a mandatory field. Put here the location of a MoBIE collection table. This may be a path to a file on your computer or to a "cloud resource" such as an S3 object store, a GitHub URL, or a Google Sheet URL. The collection table can be provided in a number of formats, including EXCEL, CSV, TSV and Google Sheets. For Google Sheets simply copy and paste the link that shows in your browser or use the link that you obtain when using Google's sharing functionality. 
* `Data Root`: This is a mandatory field.
    - `PathsInTableAreAbsolute`: Choose this if the `uri` column in the table contains absolute paths (for cloud resources that is always the case, for files on your computer it may be the case)
    - `UseTableFolder`: Choose this option if the paths in the `uri` column are relative to the location of the collection table. This supports the scenario, where you have all your data organised within some folder structure and the collection table is at the root of this folder structure. This is a very useful setup because it allows you to move or copy the whole folder structure and opening the data via the collection table will still work.
    - `UseBelowRootDataFolder`: Choose this option if the paths in the `uri` column are relative to the location of the root data folder that you can specify below. This supports the scenario, where you have all your data organised within some folder structure and the collection table is, for some reason, not at the root of this folder structure.
    - *Note that in principle we could probably support a mix of local relative and cloud absolute paths; if you need this please [get in touch](https://forum.image.sc/).*
* `( Data Root Folder )`: This is an optional field. It is only considered if you chose `UseBelowRootDataFolder` above.
* `Viewing mode`: This is a mandatory field. It changes the browsing mode of BigDataViewer.
    - `ThreeDimensional`: Choose this is your data also contains 3-D images.
    - `TwoDimensional`: Choose this if all your data is 2-D (it will make your life easier, because this mode avoids getting lost in 3-D while browsing).
* `( S3 Access Key )` & `( S3 Secret Key )`: These are optional fields. Use those if the `uri` column of the collection table points to data in a protected S3 bucket.

### Example collection tables

#### Learning tips

- In the below example tables only the `uri` column is mandatory. It can be instructive to remove some or all of the other columns and see what you get. You can then sequentially add back the other columns and observe how the visualisation changes (and/or errors show or go).
    - Practically, you can "remove" a column by giving it a name that MoBIE does not recognise, e.g. renaming `affine` (recognised) to `x_affine` (not recognised).
- For local image data, you can use `Plugins > MoBIE > Create > Create MoBIE Collection Table...` to get started and then modify or add columns

#### Local data 

- [Segmented nuclei with measurements tables](https://github.com/mobie/mobie.github.io/raw/refs/heads/master/tutorials/data/collection_tables/segmented_nuclei.zip)
    - Segmentations and measurements tables have been created using [this CellProfiler project](https://github.com/NEUBIAS/training-resources/raw/refs/heads/master/scripts/cellprofiler/segment_2d_nuclei_measure_shape_cp4.2.8.cpproj)
    - After download unzip the data
    - `Plugins > MoBIE > Open > Open Collection Table...`
        - `Table Uri:` Enter path to `one-image-collection.csv` or `two-images-collection.csv`
        - `Data Root`: `UseTableFolder`
        - `Viewing Mode`: `TwoDimensional`
        - *Leave all other fields empty*

#### Google sheets pointing to remote data

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
- [ThinPlateSpline transformed EM volume](https://docs.google.com/spreadsheets/d/1elair242cN5rbYtlODKu5yIscZHQ9O0Lci598-NoY4I/edit?usp=sharing)


### Quick start

Make sure to have [MoBIE installed on your computer](installation.md).

Within the Fiji menu select: `Plugins > MoBIE > Open > Open Collection Table...`.

In the user interface that pops up choose:

* `Table Uri`: https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0
* `Data Root`: `PathsInTableAreAbsolute`
* `( Data Root Folder )`: _leave empty_
* `Viewing mode`: `ThreeDimensional`
* `( S3 Access Key )`: _leave empty_
* `( S3 Secret Key )`: _leave empty_

Have fun browsing the data! 

Note that you could use any of the URL of the above "Example collection tables" in the exact same way (just copy and paste the links into the `Open Collection Table...` command).

If you are unsure how to browse the data, [this video](https://www.youtube.com/watch?v=oXOXkWyIIOk&pp=0gcJCQMKAYcqIYzv) should be helpful. More videos can be found in the [MoBIE YouTube channel](https://www.youtube.com/@MoBIE-Viewer).

[Troubleshooting](troubleshooting.md)



