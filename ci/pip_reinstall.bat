@ECHO.
@ECHO PIP REINSTALL LOCAL PACKAGE
@ECHO.

@ECHO.
@ECHO STEP 1/4
@ECHO.
CALL .\ci\build_package.bat

@ECHO.
@ECHO STEP 2/4
@ECHO.
CALL .\ci\pip_uninstall.bat

@ECHO.
@ECHO STEP 3/4
@ECHO.
CALL .\ci\pip_install_requirements.bat

@ECHO.
@ECHO STEP 4/4
@ECHO.
CALL .\ci\pip_install_local_package.bat
