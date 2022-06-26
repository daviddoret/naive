@ECHO OFF

ECHO.
@ECHO PIP List for version references
ECHO.
pip list

ECHO.
@ECHO Build Documentation
ECHO.
ECHO Same command as Read The Docs (except folder name 'build' instead of '_build')
CD docs\source
python -m sphinx -T -E -b html -d ../build/doctrees -D language=en . ../build/html
CD ..\..
REM docs/make html

