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

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
# Reference: https://www.sphinx-doc.org/en/master/tutorial/describing-code.html
# Project root
project_root = pathlib.Path(__file__).parents[2].resolve()
print(f'project_root: {project_root}')
sys.path.insert(0, project_root.as_posix())
naive_source = pathlib.Path(str(project_root) + r'/src/naive')
print(f'naive_source: {naive_source}')
sys.path.insert(0, naive_source.as_posix())

# Reference: https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module
package_path = project_root.as_posix() #os.path.abspath('src')
os.environ['PYTHONPATH'] = ':'.join((package_path, os.environ.get('PYTHONPATH', '')))
print(f'package_path: {package_path}')
python_path = os.environ['PYTHONPATH']
print(f'python_path: {python_path}')
print(f'sys.path: {sys.path}')
print(f'os.getcwd(): {os.getcwd()}')
print(' ')

# import src.naive as naive
# naive.hello_world('Mira')

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
    #'sphinx_exec_code',
    'sphinxcontrib.bibtex', # for bibliographic references
    'sphinx_copybutton',  # for adding “copy to clipboard” buttons to all text/code boxes
    'jupyter_sphinx' # https://jupyter-sphinx.readthedocs.io/en/latest/
    #'jupyter-execute'
    #'jupyter_sphinx.execute'
]


bibtex_bibfiles = ['bibliography.bib']

#Other interesting extensions are:
#'sphinx.ext.mathjax' (Sphinx loads this by default) for math formulas
#'sphinxcontrib.rsvgconverter' for SVG->PDF conversion in LaTeX output
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
#html_theme = 'python_docs_theme'
#import kotti_docs_theme
#html_theme = 'kotti_docs_theme'
#html_theme_path = [kotti_docs_theme.get_theme_dir()]

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
autodoc_mock_imports = ["annotations", "warnings", "typing", "numpy", "collections.abc", "nptyping"]

# sphinx-exec-code configuration
# source: https://sphinx-exec-code.readthedocs.io/en/latest/configuration.html
# exec_code_working_dir = pathlib.Path(u'../../samples')
exec_code_folders = ['..\\..\\src']
exec_code_example_dir = pathlib.Path('..\\..\\src\\samples')

# https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
# https://www.sphinx-doc.org/ar/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autoclass_content = 'class'
#autodoc_default_flags = [
#    'members',
#    'undoc-members',
#    'private-members',
#    'special-members',
#    'inherited-members',
#    'show-inheritance',
#    'ignore-module-all',
#    'exclude-members'
#]
autodoc_default_options = {
    'members': True,
    'member-order': 'alphabetical',
    'special-members': True,
    # 'undoc-members': True,
    # 'exclude-members': '__weakref__'
    #'imported-members':
    'show-inheritance': True
}

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

napoleon_custom_sections = [
    ('Sample use cases', 'example_style'),
    ('Design choice', 'example_style')]
