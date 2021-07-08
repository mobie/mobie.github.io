import json
import os
import unittest
import jsonschema


class TestSchema(unittest.TestCase):
    schema_root = os.path.join(
        os.path.split(__file__)[0], '../schema'
    )

    def _test_schema(self, schema_name):
        path = os.path.join(self.schema_root, schema_name + ".schema.json")
        self.assertTrue(os.path.exists(path))

        with open(path, 'r') as f:
            schema = json.load(f)
        jsonschema.Draft7Validator.check_schema(schema)

    def test_dataset(self):
        self._test_schema('dataset')

    def test_project(self):
        self._test_schema('project')

    def test_source(self):
        self._test_schema('source')

    def test_view(self):
        self._test_schema('view')

    def test_views(self):
        self._test_schema('views')


if __name__ == '__main__':
    unittest.main()
