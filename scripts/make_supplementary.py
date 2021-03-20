# helper script to compile a pdf from the markdown files, e.g. for the nature methods supplementary material

import os
from subprocess import run


# TODO need to have all image sources locally or enable download
# TODO write introductory supplementary note
# this is just an example of how to combine the different pages into one pdf
files = {
    # 'Supplementary': '',
    "# Supplementary Note 1: Usage": [
        "./tutorials/explore_a_project.md",
        "./tutorials/bookmarks_and_locations.md"
    ],
    "# Supplementary Note 2: Specification": [
        "./specs/mobie_project_spec.md",
        "./specs/metadata_and_tables.md"
    ]
}
out_file = './test.pdf'

text = ""
for title, file_list in files.items():
    text += f"{title}\n"
    for in_file in file_list:
        with open(in_file, 'r') as f:
            # TODO, all headings should get an additional # to have the correct nesting
            text += f.read()
    text += "\n"

tmp_file = './tmp.md'
with open(tmp_file, 'w') as f:
    f.write(text)

run(['pandoc', '--pdf-engine=xelatex', '-o', out_file, tmp_file])
os.remove(tmp_file)
