# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Configuration file for the Sphinx documentation builder.
import sys
import os

sys.path.insert(0, os.path.abspath('../../naive'))
# Reference: https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module

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
    'sphinx.ext.napoleon'
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
