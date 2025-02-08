## Open image and segmentation collections

The `Open Collection Table...` command allows users to open a collection table containing references to multiple datasets, facilitating batch visualization. The command supports various viewing and grouping modes and data root configurations.

### Command Description

The `Open Collection Table...` is designed to:

- Open a collection table specified by the user.
- Configure data root paths based on absolute paths or relative paths.
- Support different viewing modes for data visualization.
- Optionally handle access credentials for protected S3 buckets.

### Parameters

- Table Path: The file location of the collection table to be opened. The table must be a TAB-separated text file.
- Data Root: Specifies how the data URIs in the table are interpreted:
-  PathsInTableAreAbsolute : Assume URIs are absolute paths.
-  UseTableFolder : Use the folder containing the table as the root for relative paths.
-  UseBelowDataRootFolder : Use a specified folder as the root for relative paths.
- Data Root Folder: Optional. Specify this if paths in the table are relative and you want to use a specific directory as the root.
- Viewing Mode: Determines the visualization mode:
  - ThreeDimensional : Enables arbitrary plane slicing for volumetric viewing.
  - Planar : Restricts browsing to the XY, YZ, or XZ planes.
- S3 Access Key: Optional. Access key for accessing data in a protected S3 bucket.
- S3 Secret Key: Optional. Secret key for accessing data in a protected S3 bucket.

### Collection Table Specification

The collection table must adhere to the following specifications, with exact column names given in brackets. 

#### Important notes

- The table must be a **TAB-separated** text file
  - You can create such a table, e.g., in Excel via "Save As..", choosing the "File Format" "Tab-delimited Text".
- Only the `uri` column must be present; all other columns are optional.
- Please see the [JavaDoc](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java) for an up-to-date and a more comprehensive description.
- Please see this [folder](https://github.com/mobie/mobie-viewer-fiji/tree/main/src/test/resources/collections) for example tables.

#### Columns

This list just provides an overview. See the [JavaDoc](https://github.com/mobie/mobie-viewer-fiji/blob/main/src/main/java/org/embl/mobie/lib/table/columns/CollectionTableConstants.java) for more details and example entries.

- URI Column (`uri`): Must contain valid URIs pointing to image or spots datasets. Supported formats include OME-Zarr, BDV XML, ilastik HDF5, Parquet, and others.
- Name Column (`name`): Optional. Determines the label for data display within MoBIE. If absent, a name is derived  from the file name.
- Type Column (`type`): Optional. Specifies the pixel type ("intensities", "labels", "spots"). Defaults to "intensities" if absent or invalid.
- Channel Column (`channel`): Optional. Zero-based integer Determines which channel of a multi-channel dataset to load. Defaults to channel 0 if absent or invalid.
- Color Column (`color`): Optional. Specifies the lookup table coloring for intensities. Defaults to "white" if absent or invalid.
- Blend Column (`blend`): Optional. Determines the blending mode ("sum" or "alpha"). Defaults to "sum" if absent or invalid.
- Affine Column (`affine`): Optional. Specifies an affine transformation to apply upon display.
- View Column (`view`): Optional. Determines the view name for access in MoBIE UI. Defaults to the name from the Name column.
- Exclusive Column (`exclusive`): Optional. Determines if a view is exclusive ("true" or "false"). Defaults to "false".
- Group Column (`group`): Optional. Specifies a UI selection group for the view. Defaults to "views" if absent.
- Labels Table Column (`labels_table`): Optional. Used for "labels" type data, specifies a path to a segmentation table.
- Contrast Limits Column (`contrast_limits`): Optional. Specifies contrast limits for intensities. Defaults to auto-contrast if absent or invalid.
- Grid Column (`grid`): Optional. Groups data into a grid view. Defaults to no grid if absent.
- Format Column (`format`): Optional. Specifies the data format (e.g., OmeZarr). Defaults based on file ending if absent.

### Usage

- Provide the path to the collection table and configure the data root as needed.
- Choose the desired viewing mode for data visualization.
- Optionally, provide S3 access credentials if accessing protected data.

