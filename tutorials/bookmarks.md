## Bookmark file details

Bookmarks are a way to save the current setup of your viewer, so anyone can browse to it
quickly and easily.
All bookmarks are saved in .json files in each dataset of your project, under
misc/bookmarks.

You must have one file called **default.json** - this controls what view you show when you 
first open the dataset. Then, you can have as many additional bookmark .json files as you'd
like.

### Syntax of bookmarks

The general syntax of a bookmark is as below:
```
{
	"Name_of_my_bookmark" : {
		"layers": {
		
			"name_of_image_1" {
				"setting_1":[],
				"setting_2":[]
				},
				
			"name_of_image_2" {
				"setting_1":[],
				"setting_2:[]
				}
		}, 
		"position" : [x, y, z],
		"normView" : [n1,n2,n3,n4,n5,n6,n7,n8,n9,10,n11,n12]
	}
		
}			
```

You can specify as many images as you like within "layers", to display them. If you specify no images,
it will keep the user's currently displayed images.

Within each image's {}, you can adjust various settings, described below.

Position / view are as specified by **Log Current Location** - see the location and bookmark tutorial [here](./bookmarks_and_locations.md)

### Settings

- **contrastLimits** [min, max] Minimum and maximum values for contrast.
- **selectedLabelIds** [label_id_1, label_id_2...] Which label ids to show as selected.
- **showSelectedSegmentsIn3d** true; false Whether to show selected objects in 3D viewer.
- **showImageIn3d** true; false Whether to show image in 3D viewer.
- **resolution3dView** resolution in physical units to use for 3d display. Leaving this at 0.0 will calculate a sensible default on loading.
- **color** "colourName" Name of a solid colour e.g. magenta, or name of a colour look up table (see the 'Colour by column..' section of this [tutorial](./exploring_segmentations) for options)
- **colorByColumn** "columnName" Name of column to colour by
- **valueLimits** [min, max] Minimum and maximum values to use for colouring by column with a numeric colour scheme e.g. BlueWhiteRed or Viridis
- **tables** ["nameOfTable1", "nameofTable2"...] Names of further tables to add to the default.


### Examples

An example default.json can be found [here](https://github.com/mobie/platybrowser-datasets/blob/master/data/1.0.1/misc/bookmarks/default.json), 
and bookmark .json [here](https://github.com/mobie/platybrowser-datasets/blob/master/data/1.0.1/misc/bookmarks/manuscript_bookmarks.json).



