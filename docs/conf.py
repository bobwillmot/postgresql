project = "PostgreSQL Python Starter"
author = "Project Contributors"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
