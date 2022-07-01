# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Configuration file for the Sphinx documentation builder.
import sys
import os
import pathlib

# Reference: https://jupyter-sphinx.readthedocs.io/en/latest/
#package_path = os.path.abspath('../..')
#os.environ['PYTHONPATH'] = ':'.join((package_path, os.environ.get('PYTHONPATH', '')))
#os.environ['PYTHONPATH'] = ':'.join(('C:/Users/david/PycharmProjects/naive', os.environ.get('PYTHONPATH', '')))

# Reference: https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module
#sys.path.insert(0, os.path.abspath(u'../../naive'))
# sys.path.insert(0, os.path.abspath('..'))
#sys.path.insert(0, os.path.abspath('C:\\Users\\david\\PycharmProjects\\naive'))
#print(f'sys.path: {sys.path}')
#package_path = os.path.abspath('../..')
#os.environ['PYTHONPATH'] = ':'.join((package_path, os.environ.get('PYTHONPATH', '')))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
# Reference: https://www.sphinx-doc.org/en/master/tutorial/describing-code.html
# sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# -- Project information

project = 'naive'
copyright = '2022, David Doret'
author = 'David Doret'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'nbsphinx',
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
    'sphinx_exec_code',
    'jupyter_sphinx' # https://jupyter-sphinx.readthedocs.io/en/latest/
    #'jupyter-execute'
    #'jupyter_sphinx.execute'
]


#Other interesting extensions are:
#'sphinx.ext.mathjax' (Sphinx loads this by default) for math formulas
#'sphinxcontrib.bibtex' for bibliographic references
#'sphinxcontrib.rsvgconverter' for SVG->PDF conversion in LaTeX output
#'sphinx_copybutton' for adding “copy to clipboard” buttons to all text/code boxes
#'sphinx_gallery.load_style' to load CSS styles for thumbnail galleries

#suppress_warnings = [
#    'nbsphinx',
#]
#suppress_warnings = [
#    'nbsphinx.localfile',
#    'nbsphinx.gallery',
#    'nbsphinx.thumbnail',
#    'nbsphinx.notebooktitle',
#    'nbsphinx.ipywidgets',
#]


source_encoding = 'utf-8'

autosummary_generate = True

intersphinx_mapping = {
    'python': (u'https://docs.python.org/3/', None),
    'sphinx': (u'https://www.sphinx-doc.org/en/master/', None),
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
# exec_code_working_dir = pathlib.Path(u'../../samples')
#exec_code_folders = ['../..']
#exec_code_example_dir = pathlib.Path(u'../../samples')


import os
os.chdir('/')
sys.path.insert(0, '/')