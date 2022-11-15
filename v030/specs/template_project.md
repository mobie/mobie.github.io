# MoBIE specification

MoBIE projects follow the specification described here; it is based on four key concepts:
- A `project`, which groups data, for example from the same publication, that can be opened by the MoBIE viewer. It consists of multiple `datasets`.
- A `dataset`, which contains all the data that can be opened in the same MoBIE viewer instance.
- A `source`, which corresponds to the data for a single image (also volume, timeseries), segmentation image or spot coordinates. For segmentation images it may also contain the associated tabular data. For spots the only data associated with the source is a table.
- A `view`, which describes the full viewer state.

The specification is defined via [jsonschema](https://json-schema.org/). The schema files are located [here](https://github.com/mobie/mobie.github.io/tree/master/schema).
It is versioned, following [the semantic versioning convention](https://semver.org/). The current version is `0.3.0`.

**Using jsonschema:**

The jsonschema files can be used in the following ways:
- Static validation against the schema: using e.g. [jsonschema-python](https://python-jsonschema.readthedocs.io/en/stable/) `jsonschema -i my-dataset-schema.json schema/dataset.schema.json`. See also the [full project validation script](https://github.com/mobie/mobie.github.io/blob/master/scripts/validate_project.py).
- Generate example data from the schema with [fake-schema-cli](https://github.com/atomsfat/fake-schema-cli): `fake-schema schema/dataset.schema.json`

## <a name="project"></a>Project 

The `project` and its associated `datasets` are stored in a directory structure, with the project corresponding to the root directory.
This directory must contain the file `project.json`, which must contain a valid [project schema](https://github.com/mobie/mobie.github.io/tree/master/schema/project.schema.json).
See an example project structure, slightly adapted from the [clem project](https://github.com/mobie/clem-example-project):
```
clem/
├── project.json
├── hela
└── yeast
```

### <a name="project-metadata"></a>Project Metadata

The project metadata, stored in `project.json`, has the following structure:
- `datasets`: List of the available datasets. The dataset directory names must match the names in this list. It must contain at least one dataset.
- `defaultDataset`: The dataset that will be opened when the MoBIE viewer is started for this project.
- `description`: Description of this project.
- `references`: List of references (publications, urls etc.) for this project.
- `specVersion`: The MoBIE specification version of this project.

For the clem project the `project.json` looks like this:
```yaml
{
  "datasets": ["hela", "yeast"],
  "defaultDataset": "hela",
  "description": "Correlative electron microscopy data from the Schwab Lab at EMBL Heidelberg.",
  "references": ["https://doi.org/10.1083/jcb.201009037", "https://doi.org/10.1038/nmeth.1486"],
  "specVersion": "0.3.0"
}
```

### <a name="project-storage"></a>Local & Remote Projects

Projects can be stored locally or hosted remotely and  the `image data`, i.e. the images in one of the [supported data formats](#data) and `metadata`, i.e. the json files describing the project and [tabular data](#tables) can be accessed from different storage locations for one project.

In more detail, MoBIE currently supports the following three storage options:
- filesystem: can store `image data` and `metadata`.
- s3 object storage: can store `image data` and `metadata`; public and private buckets are supported.
- github: can only store `metadata`, `image data` must be loaded from object storarge.

This enables different combinations of hosting a project, see also [this figure](fig-storage):
<ol type="a">
<li>only on filesystem: project is only available locally.</li>
<li>only on s3 object storage: project is self-contained in object storage and can be shared with collaborators privately (using a privat bucket) or shared publicly (using a public bucket).</li>
<li>on github and s3 object storage: the metadata is stored on github, which also serves as entrypoint for the viewer. The image data is stored on the s3 bucket. This set-up has the advantage that the metadata is under version control.</li>
</ol>

![fig-storage](../assets/hosting.png)
