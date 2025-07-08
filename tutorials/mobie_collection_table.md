## MoBIE collection table 

A MoBIE collection table is a very convenient way to specify how to open multiple images, segmentations or spots, potentially correlative, in MoBIE.

In a nutshell, each row specifies one dataset, where the only required column is called **uri**, which must contain a valid path to that dataset. This path can be local (File system) or in the cloud (S3 or HTTP).

There are a few more reserved column names that can be used to specify how the data should be visualized in more detail. For example, the **affine** column that can be used to transform images into a common coordinate system, which is useful for correlative data.

[**Specification of supported columns.**](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java).

In addition to the specified columns the table can contain arbitrary other columns that may contain interesting information about the respective data sets. Please make sure not to use column names that are part of the above specification.

### Opening a collection table 

A collection table can be opened via the `Open Collection Table...` command to be found within `Fiji: Plugins > MoBIE`. In addition to the required path to the collection table the command takes a few optional arguments such as S3 keys.

### Supported collection table data formats

The collection table itself can be provided in a number of formats; notably also links to Google Sheets are supported. If you like to use the CSV file format we recommed quoting `"..."` the table cell values, because some of them may contain commas.

[**Supported table file formats.**](tutorials/index.md#table-data-formats)

### Example collection tables

Below are some examples. Those are all Google sheets, so those links could be directly opened in the above described command.

- [Correlative 2-D EM, fluorescence and 3-D tomography data](https://docs.google.com/spreadsheets/d/1d_khb5P-z1SHu09SHSS7HV0PmN_VK9ZkMKDuqF52KRg/edit?gid=0#gid=0)
- [Grid view of many OpenOrganelle EM volumes](https://docs.google.com/spreadsheets/d/1trSQFm_4Nc42C_Fum8N_ZzEmPuML6ACKVmLlc862Rp8/edit?usp=sharing)
- [Grid view of a few OpenOrganelle EM volumes and organelle segmentations](https://docs.google.com/spreadsheets/d/1jEnl-0_pcOFQo8mm8SUtszoWewvjyFXY0icO7gPUaQk/edit?gid=0#gid=0)
- [Large volume EM data, annotated cell segmentation, and a few spots](https://docs.google.com/spreadsheets/d/1xZ4Zfpg0RUwhPZVCUrX_whB0QGztLN_VVNLx89_rZs4/edit?gid=0#gid=0)