@ECHO OFF

ECHO.
@ECHO PIP List for version references
ECHO.
pip list

ECHO.
@ECHO Build Documentation
ECHO.
REM python -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html

docs/make html

