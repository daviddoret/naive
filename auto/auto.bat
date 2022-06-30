@ECHO OFF

ECHO.
@ECHO PIP List for version references
ECHO.
pip list


REM ECHO.
REM @ECHO Clean Documentation
REM ECHO.
REM CD docs
REM .\make clean

ECHO.
@ECHO Wipe Documentation Build
ECHO.
RMDIR /Q /S docs\source\pages
RMDIR /Q /S docs\build


pip uninstall naive -y
pip install naive

ECHO.
@ECHO Build Documentation
ECHO Same command as Read The Docs (except folder name 'build' instead of '_build')
ECHO.
CD docs\source
REM https://www.sphinx-doc.org/en/master/man/sphinx-build.html
python -m sphinx -a -v -T -E -W -b html ../build/doctrees ../build/html

