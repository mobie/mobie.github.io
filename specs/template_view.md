## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce the MoBIE viewer state.

### <a name="view-source-annotations"></a>Region Displays

Views may contain region displays, specified by a `regionDisplay` (see schema description below), which describe the physical locations of images or collection of images in the global coordinate system.
Region displays must contain a reference to a region source.
The region source is associated with a table, which has rows associated with the regions. This table can be used in the viewer to navigate to the corresponding region (by clicking on the row) and may store additional annotations or measurements.
The table must contain the column `region_id` and must contain at least one more column.
The values in the `region_id` column must be strings and must correspond to the keys of the `sources` field of the `regionDisplay`.
The sources field in the dispalay defines the mapping of the `region_id` values to the source(s) for each region. 
Otherwise the same rules as outlined in the [Table Data setion](#table-data) apply.

A primary application of region displays are tables for views with a `grid` transform (see schema description below).
See an example grid view table for four positions in a grid of tomograms for the clem project, which contains indicator values for the presence of different organelles for each position.
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

<!---
Don't add anything manually after this line. The example view metadata will be generated automatically when running
scripts/generate_spec_description.py
-->
