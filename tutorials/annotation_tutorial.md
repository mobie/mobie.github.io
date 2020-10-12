# Annotation tutorial

You can also annotate the segmented objects in your project using MoBIE. You can either do it from scratch or correct an already existing annotation.

## Annotating from scratch

1. To start with, open a project and add the segmentation image you want to annotate. We will use the cell segmentation of the published ['Platybrowser' project](https://github.com/mobie/platybrowser-datasets) as an example:
<br> <img width="800" alt="image" src="./tutorial_images/cellSegm.png"> <br>
2. In the segmentation table select Annotate -> Start new annotation... You will be asked to name your annotation. In this example we will annotate cell types, so we name it **cell_type**.
Starting the annotation will add a new column into the segmentation table, where the annotations will be saved:
<br> <img width="400" alt="image" src="./tutorial_images/cellTypeCol.png"> <br>
At the moment all the values in the column are **None**. <br>
3. After starting the annotation we get a new annotation window, where we can add new categories:
<br> <img width="400" alt="image" src="./tutorial_images/annotMenu.png"> <br>
To start with, we add two categories: muscles and neurons. The button **C** next to the category name allows to choose a color that will be used to color all the segments of this category:
<br> <img width="400" alt="image" src="./tutorial_images/chooseAnnotColor.png"> <br>
4. To select cells to annotate we have two options:
  *  Navigating with **Select previous** and **Select next** buttons. This will sequentially show you all segments in the table. It is important to unselect the **Skip "None" & "NaN"** since, when selected, it skips all the unannotated segments (in our case **all** the segments).
  We click **Select next** till we see a neuron:
  <br><img width="400" alt="image" src="./tutorial_images/neuronSelected.png"> <br>
  Then we click on **neuron** in the annotation window. This should change the color of the selected cell to red and change the **None** in the table to the selected category - **neuron**:
  <br> <img width="400" alt="image" src="./tutorial_images/neuronLabeled.png"> <br>
  *  Navigating directly in the BigDataViewer. For this we just scroll through the volume till we see cells we want to annotate. We can select a cell with **[Ctrl + left click]** and click the corresponding category in the annotation window.
5. During the annotation process we can add more categories. For example, here we noticed an epithelial cell, so we add a new category and annotate the cell:
<br> <img width="800" alt="image" src="./tutorial_images/epithelialLabeled.png"> <br>
6. After we are done, we can save the resulting annotation as follows: in the table click on Table -> Save Columns as.... Here we select the columns we want, in our example we just need the segment id and the cell type, but one can select more features for the further analysis:
<br> <img width="400" alt="image" src="./tutorial_images/saveAnnot.png"> <br>
7. If the annotation was saved with the **label_id** column, it can always be reopened and modified/corrected using MoBIE.

... to be continued
