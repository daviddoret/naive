# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Configuration file for the Sphinx documentation builder.
import sys
import os
import pathlib

# Reference: https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module
sys.path.insert(0, os.path.abspath('../../naive'))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
# Reference: https://www.sphinx-doc.org/en/master/tutorial/describing-code.html
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# -- Project information

project = 'naive'
copyright = '2022, David Doret'
author = 'David Doret'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    # 'myst_parser',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_exec_code'
    # 'jupyter_sphinx.execute'
]

autosummary_generate = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Reference: https://www.sphinx-doc.org/en/master/usage/markdown.html
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

exclude_patterns = ['requirements.txt']

# Reference: https://stackoverflow.com/questions/62226506/python-sphinx-autosummary-failed-to-import-module
autodoc_mock_imports = ["typing", "numpy", "collections.abc", "nptyping"]

# sphinx-exec-code configuration
# source: https://sphinx-exec-code.readthedocs.io/en/latest/configuration.html
# exec_code_working_dir = '../..'
exec_code_folders = ['../..']
# exec_code_example_dir = '../..'
