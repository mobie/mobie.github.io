## Bookmarks

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
		"view" : [1,2,3,4,5,6,7,8,9,10,11,12]
	}
		
}			
```

You can specify as many images as you like within "layers", to display them. If you specify no images,
it will keep the user's currently displayed images.

Within each image's {}, you can adjust various settings, described below.

Position / view are as specified by **Log Current Location** - see that tutorial...

### Settings

- **contrastLimits** [min, max] Minimum and maximum values for contrast.
- **selectedLabelIds** [label_id_1, label_id_2] Which label ids to show as selected.
- **showSelectedSegmentsIn3d** true; false Whether to show selected objects in 3D viewer.
- **color** "colourName" Name of a solid colour e.g. magenta, or name of a colour look up tables (see tutorial...)
- **colorByColumn** "columnName" Name of column to colour by
- **tables** ["nameOfTable1", "nameofTable2"] Names of further tables to add to the default.

### Examples

An example default.json can be found [here](https://github.com/mobie/platybrowser-datasets/blob/master/data/1.0.1/misc/bookmarks/default.json), 
and bookmark .json [here](https://github.com/mobie/platybrowser-datasets/blob/master/data/1.0.1/misc/bookmarks/manuscript_bookmarks.json).



