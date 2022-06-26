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


ECHO.
@ECHO Build Documentation
ECHO Same command as Read The Docs (except folder name 'build' instead of '_build')
ECHO.
CD docs\source
python -m sphinx -T -E -b html -d ../build/doctrees -D language=en . ../build/html

