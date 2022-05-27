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

pdfkit.from_url(urls, "test.pdf")
