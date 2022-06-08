import os
import re
import requests
import pdfkit

urls = [
    "https://mobie.github.io/",
    "https://mobie.github.io/tutorials/installation.html",
    "https://mobie.github.io/tutorials/explore_a_project.html",
    "https://mobie.github.io/tutorials/exploring_segmentations.html",
    "https://mobie.github.io/tutorials/views_and_locations.html",
    "https://mobie.github.io/tutorials/viewing_your_own_tables.html",
    "https://mobie.github.io/tutorials/creating_your_own_views.html",
    "https://mobie.github.io/tutorials/annotation_tutorial.html",
    "https://mobie.github.io/tutorials/image_grids_and_tables.html",
    "https://mobie.github.io/tutorials/branches_and_credentials.html",
    "https://mobie.github.io/tutorials/expert_mode.html",
    "https://mobie.github.io/tutorials/mobie_project_creator.html",
    "https://mobie.github.io/tutorials/scripting_project_creator.html",
    "https://mobie.github.io/specs/mobie_spec.html"
]


def download_and_remove_header(url):
    with requests.get(url) as r:
        text = r.text
    return text
    without_header = re.sub("<header>.*?</header>", "", text, flags=re.DOTALL)
    return without_header
    # out_dir = "./htmls"
    # os.makedirs(out_dir, exist_ok=True)
    # out_path = os.path.join(out_dir, os.path.basename(url))
    # with open(out_path, "w") as f:
    #     f.write(without_header)


x = download_and_remove_header(urls[1])
breakpoint()
pdfkit.from_string(x, "test.pdf")
