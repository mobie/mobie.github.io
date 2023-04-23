import json
import os
import unittest
from copy import deepcopy

import jsonschema


class TestSchema(unittest.TestCase):
    schema_root = os.path.join(os.path.split(__file__)[0], "../schema")
    example_root = os.path.join(os.path.split(__file__)[0], "../specs/examples")

    def _test_schema(self, schema_name, examples=None):
        path = os.path.join(self.schema_root, schema_name + ".schema.json")
        self.assertTrue(os.path.exists(path))

        with open(path, "r") as f:
            schema = json.load(f)
        jsonschema.Draft7Validator.check_schema(schema)

        if examples is not None:
            for example in examples:
                example_path = os.path.join(self.example_root, example)
                assert os.path.exists(example_path)
                with open(example_path) as f:
                    spec = json.load(f)
                for name, instance in spec.items():
                    jsonschema.validate(instance=instance, schema=schema)

        return schema

    def test_dataset(self):
        self._test_schema("dataset")

    def test_project(self):
        self._test_schema("project")

    def test_source(self):
        examples = ["image_source.json", "segmentation_source.json"]
        schema = self._test_schema("source", examples)

        # test an example image source
        source = {"image": {"imageData": {"bdv.hdf5": {"relativePath": "blob.h5"}}}}
        jsonschema.validate(instance=source, schema=schema)

        # test an example region table source
        source = {"regions": {"tableData": {"tsv": {"relativePath": "tables/my_table"}}}}
        jsonschema.validate(instance=source, schema=schema)

        # test an example spot source
        source = {"spots": {
            "boundingBoxMin": [0.0, 0.0],
            "boundingBoxMax": [100.0, 100.0],
            "tableData": {"tsv": {"relativePath": "tables/my_table"}},
            "unit": "pixel",
        }}
        jsonschema.validate(instance=source, schema=schema)

    def test_view(self):
        examples = ["single_source_view.json", "grid_view.json", "advanced_fig2c.json"]
        self._test_schema("view", examples)

    def test_views(self):
        self._test_schema("views")

    # make sure that the other color models work
    def test_color_scheme(self):
        with open("../specs/examples/single_source_view.json") as f:
            view = json.load(f)["default"]

        schema_path = os.path.join(self.schema_root, "view.schema.json")
        with open(schema_path, "r") as f:
            schema = json.load(f)

        # make sure that all patterns work
        # {"pattern": "^(\\d+)-(\\d+)-(\\d+)-(\\d+)$"},
        # {"pattern": "^r=(\\d+),g=(\\d+),b=(\\d+),a=(\\d+)$"},
        # {"pattern": "^r(\\d+)-g(\\d+)-b(\\d+)-a(\\d+)$"}
        for color_string in ["255-255-255-255", "r=255,g=255,b=255,a=255", "r255-g255-b255-a255"]:
            this_view = deepcopy(view)
            this_view["sourceDisplays"][0]["imageDisplay"]["color"] = color_string
            jsonschema.validate(instance=this_view, schema=schema)


if __name__ == "__main__":
    unittest.main()
