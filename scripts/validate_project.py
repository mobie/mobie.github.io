import argparse
import json
import os
import sys
from glob import glob

import jsonschema
import requests


SCHEMA_URLS = {
    "bookmarks": "https://raw.githubusercontent.com/mobie/mobie.github.io/master/schema/bookmarks.schema.json",
    "dataset": "https://raw.githubusercontent.com/mobie/mobie.github.io/master/schema/dataset.schema.json",
    "project": "https://raw.githubusercontent.com/mobie/mobie.github.io/master/schema/project.schema.json",
    "source": "https://raw.githubusercontent.com/mobie/mobie.github.io/master/schema/source.schema.json",
    "view": "https://raw.githubusercontent.com/mobie/mobie.github.io/master/schema/view.schema.json"
}


def download_schemas():
    def _download(address, out_file):
        if os.path.exists(out_file):
            return True
        r = requests.get(address)
        with open(out_file, 'w') as f:
            f.write(r.content.decode('utf-8'))

    for name, url in SCHEMA_URLS.items():
        _download(url, f"{name}.schema.json")


def validate_project(project):
    download_schemas()

    project_metadata = os.path.join(project, "project.json")
    assert os.path.exists(project_metadata), f"Cannot find project metadata at {project_metadata}"
    with open(project_metadata) as f:
        project_metadata = json.load(f)
    with open('project.schema.json') as f:
        project_schema = json.load(f)
    jsonschema.validate(project_metadata, project_schema)

    datasets = project_metadata["datasets"]
    for name in datasets:
        dataset_folder = os.path.join(project, name)
        assert os.path.exists(dataset_folder), f"Cannot find dataset at {dataset_folder}"

        dataset_metadata = os.path.join(dataset_folder, 'dataset.json')
        assert os.path.exists(dataset_metadata), dataset_metadata
        with open(dataset_metadata) as f:
            dataset_metadata = json.load(f)
        with open('dataset.schema.json') as f:
            dataset_schema = json.load(f)
        jsonschema.validate(dataset_metadata, dataset_schema)

        # check that the filepaths exist
        sources = dataset_metadata['sources']
        for source in sources.values():
            source = list(source.values())[0]
            storage_locations = source["imageDataLocations"]
            for name, location in storage_locations.items():
                abs_location = os.path.join(dataset_folder, location)
                assert os.path.exists(abs_location), f"Could not find storage {name} in {abs_location}"

            if "tableRootLocation" in source:
                table_location = source["tableDataRootLocation"]
                default_table_location = os.path.join(dataset_folder, table_location, 'default.tsv')
                assert os.path.exists(default_table_location), f"Cannot find default table at {default_table_location}"

        bookmark_files = glob(os.path.join(dataset_folder, "misc/bookmarks/*.json"))
        with open('bookmarks.schema.json') as f:
            bookmark_schema = json.load(f)
        for bookmark in bookmark_files:
            with open(bookmark) as f:
                bookmark = json.load(f)
            jsonschema.validate(bookmark, bookmark_schema)

        print("Successfully validate MoBIE project at", project)
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    args = parser.parse_args()
    validate_project(args.project)
