## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce the MoBIE viewer state.

### <a name="view-source-annotations"></a>Region Displays

Views may contain region displays, specified by a `regionDisplay` (see schema description below), which describe the physical locations of images or collection of images in the global coordinate system.
Region displays must contain a table with rows associated with the sources of the display. This table can be used in the viewer to navigate to the corresponding sources (by clicking on the row) and it may store additional annotations or measurements for the correspoding image(s).
The tables should be stored as tab separated values, but may also be comma separated.
They must contain the column `region_id` and must contain at least one more column.
The values in the `region_id` column must be strings and must correspond to the keys of the `sources` field in the `regionDisplay`.

A primary application of region displays are tables for views with a `grid` transform (see schema description below).
In this case the `region_id` column corresponds to the flattened grid position, which is computed from the 2d grid position according to the row-major indexing convention.
The mapping of grid positions to sources is defined in the `sources` field.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
region_id    mitochondria    vesicles    golgi   er
source1   1   0   1   0
source2   1   0   1   1
source3   0   0   0   1
source4   0   1   0   1
```

### <a name="view-metadata"></a>View Metadata

The metadata for the views of a dataset is specified in the field `views` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`views` contains a mapping of view names to [view metadata](../schema/view.schema.json).

Additional views can be stored as json files with the field `views` mapping view names to metadata in the folder `misc/views`

The view metadata has the following elements (see below for an example json file):

https://github.com/mobie/mobie.github.io/blob/48b4f9bb0528cfeae67f24d3d230d5a951b8f423/specs/examples/single_source_view.json#L1-L91