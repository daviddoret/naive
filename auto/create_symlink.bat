REM Creating a symlink in the docs folder
REM was necessary to make import naive packages
REM function properly in Jupyter notebooks
REM embedded in Sphinx documentation.
REM This is dirty stuff...

C:\
cd "C:\Users\david\PycharmProjects\naive\docs"
mklink /D naive "C:\Users\david\PycharmProjects\naive\naive"
