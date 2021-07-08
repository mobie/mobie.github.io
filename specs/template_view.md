## <a name="view"></a>View

A `view` stores all metadata necessary to fully reproduce a MoBIE viewer state.

### <a name="view-source-annotations"></a>Source Annotations

Views can optionally contain source annotations, which are specified via a `sourceAnnotationDisplay` (see schema description below). Source annotations contain a table, which has rows that are associated with the sources in this view and can be used to navigate to the sources (by clicking on the row) and store additional source level annotations.
Source annotaiton tables should be stored as tab separated values, but may also be comma separated.
They must contain the column `source_annotation_id`, which is used for navigation in the viewer, and must contain at least one more column.

A primary application of source annotations are tables for views containing a `grid` transform (see schema description below).
In this case the `source_annotation_id` column corresponds to the flat grid position, which is computed from the 2d grid position according to the row-major indexing convention.
The mapping of grid positions to sources is defined in the `sources` field.

See an example grid view table for 4 grid positions that also gives the presence of different organelles for each position.
```tsv
source_annotation_id    mitochondria    vesicles    golgi   er
0   1   0   1   0
1   1   0   1   1
2   0   0   0   1
3   0   1   0   1
```

### <a name="view-metadata"></a>View Metadata

The metadata for the views of a dataset is specified in the field `views` of `dataset.json` (see also [dataset metadata](#dataset-metadata)).
`views` contains a mapping of view names to [view metadata](https://github.com/mobie/mobie.github.io/tree/master/schema/view.schema.json).

Additional views can be stored as json files with the field `views` mapping view names to metadata in the folder `misc/views`

The metadata entries have the following structure (see below for an example json file):
