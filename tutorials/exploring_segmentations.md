## Exploring segmentations

Adding a segmentation to the viewer, will display it as a coloured overlay on your image. If available,
a corresponding table will also appear, where each row corresponds to one segmented object.

<img width="800" alt="image" src="./tutorial_images/segmentationView.png"> 

Both the table and segmentation overlay can be explored interactively:

### Interacting with the segmentation in the viewer

All keyboard shortcuts are available by clicking Help > Show Segmentation Image Help in the menu at the
top of the table.

To summarise:
- **[Ctrl + left click]** Select a segmented object. This will also cause the corresponding row of the
table to highlight. If you have **V** ticked in the sources panel, it will also display it in the 3D viewer.
- **[Ctrl + L] Randomly shuffle the colours of the segmented objects.
- **[Ctrl + shift + N]** Undo any segment selections. 
- **[Ctrl + M]** Toggle show as binary mask - will switch beween showing all segmented objects in different colours vs
showing whole segmentation as one colour.

More options are available if you right click in the viewer:
<img width="500" alt="image" src="./tutorial_images/segmentationContextMenu.png"> 

- **Undo Segment Selections** Same as Ctrl + Shift + N above.
- **Segment Selection Colouring Mode** Change how your selected objects are displayed.
	- **OnlyShowSelected** only show the selected objects, with their usual colour.
	- **SelectionColor** Show all segmented objects (usual colour), and selected objects with selection colour (yellow)
	- **SelectionColorandDimNotSelected** Show all segmented objects (very dimly), and selected objects with selection colour (yellow)
	- **DimNotSelected** Show all segmented objects (very dimly), and selected objects with usual colour
- **Segment Animation Settings...** Change speed of movements in viewer.

### Interacting with segmentation table

Clicking on a row in the table, will move you to the location of that object in the viewer.
The first column 'label_id' states the id of each segmented object from the image.

<img width="800" alt="image" src="./tutorial_images/segmentInteraction.gif"> 

### Adding more tables

### Colour by column...

### Saving tables