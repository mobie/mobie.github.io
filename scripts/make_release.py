# script to copy all the relevant files to a release folder

import argparse
import os
from shutil import copytree, copyfile

parser = argparse.ArgumentParser()
parser.add_argument("version")
args = parser.parse_args()
version = args.version
if not version.startswith("v"):
    version = f"v{version}"

folder = os.path.join("..", version)
os.makedirs(folder, exist_ok=True)

copyfile("../index.md", os.path.join(folder, "index.md"))
copytree(
    "../schema",
    os.path.join(folder, "schema")
)
copytree(
    "../tutorials",
    os.path.join(folder, "tutorials")
)
copytree(
    "../specs",
    os.path.join(folder, "specs")
)
copytree(
    "../use-cases",
    os.path.join(folder, "use-cases")
)
