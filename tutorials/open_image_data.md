## Open generic image data with MoBIE

The `Open Image and Labels...` and `Open Multiple Images and Labels...` commands facilitate the opening and visualization of images alongside their corresponding label masks and label mask tables. The command allows for spatial calibration and grid type configuration.

### Command Description

The commands are specifically designed to:

- Open one or multiple single-channel images from a specified URI.
- Open corresponding label masks and label mask tables if available.
- Configure spatial calibration settings.
- Set the grid type for visualization of image data sets.

### Parameters

- Image URI: The location of the image to be opened. Can be a file or directory. The command supports specifying a single channel from a multi-channel image using a specific format (see details below).
- Label Mask URI: The location of the label mask. Can be a file or directory. Optional.
- Label Mask Table URI: The location of the label mask table. Optional.
- Spatial Calibration: Specifies the spatial calibration settings to be used. Default is SpatialCalibration.FromImage
- Grid: Determines the grid type for visualization. The default is  `GridType.Transformed`; use `GridType.Stitched` if you have many (several hundreds) of images to improve rendering performance.

### Usage

1. Opening Images and Labels:
- To open an image, provide the Image URI (local file system or remote S3 storage).
- If you have corresponding label masks or tables, provide their respective URIs.
2. Channel Selection in Multi-Channel Images:
- If the image is multi-channel, you can select a specific channel using the format `filePath;channelIndex`.
- If you don't specify a channel MoBIE will open channel `0`.
- Example: `/data/image.ome.tiff;2` opens the third channel (index starting from 0) of `image.ome.tiff`.
3. Image Name Prepending:
- You can prepend an image name using the `=` separator.
- Example: `dapi=/data/image.ome.tiff` assigns `dapi` as name.
4. Using Wildcards for Multiple Images and Labels:
- You can use Java-style wildcards `.*` to specify patterns for opening multiple images and labels.
- This allows batch visualisation of images and labels that match the specified pattern. Those images will be shown in a Grid View (see above).

### Video tutorials

- [Using Fiji/MoBIE for visual QC of CellProfiler and ilastik output](https://www.youtube.com/watch?v=xe3FlkJ0nfU) 
