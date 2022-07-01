@ECHO OFF
ECHO.
@ECHO Build Documentation
ECHO.
ECHO Current Directory: %CD%
CD docs
ECHO.
ECHO Current Directory: %CD%
ECHO.
ECHO Remove Documentation Directory: build
RMDIR /S /Q docs
ECHO.
ECHO Remove Documentation Directory: source\pages
CD source
RMDIR /S /Q pages
CD ..
ECHO.
@ECHO Make Clean
CALL make clean
ECHO.
@ECHO Make HTML
CALL make html
REM https://www.sphinx-doc.org/en/master/man/sphinx-build.html
REM python -m sphinx -a -v -T -E -W -b html ../build/doctrees ../build/html

CD ..\..
ECHO Current Directory: %CD%