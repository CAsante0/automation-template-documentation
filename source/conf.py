import os
import sys



# Provide the absolute path to your original repository's src folder
# This completely bypasses the root-level 'app.py' file!
repo_root = os.environ['AT_REPO_URL']
src_folder = os.path.join(repo_root, "src")

# Force Python to prioritize looking INSIDE src/ before scanning the repository root.
# This prevents it from picking up the root-level 'app.py' script file!
sys.path.insert(0, src_folder)
sys.path.insert(1, repo_root)

# Set the PYTHONPATH environment variable globally for child processes/autodoc imports
os.environ["PYTHONPATH"] = src_folder + os.pathsep + repo_root + os.pathsep + os.environ.get("PYTHONPATH", "")

project = 'Automation Template Documentation'
copyright = '2026, Christina Asante - NOAA Affiliate'
author = 'Christina Asante - NOAA Affiliate'
release = '1.0.0'

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosummary", "myst_parser"]
autosummary_generate = True
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
