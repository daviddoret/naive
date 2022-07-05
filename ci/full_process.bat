
REM @ECHO SET PATH
REM CALL .\ci\set_syspath.bat

@ECHO INCREMENT PACKAGE VERSION
CALL .\ci\increment_package_version.bat

@ECHO BUILD PACKAGE
CALL .\ci\build_package.bat

@ECHO REINSTALL PACKAGE
CALL .\ci\reinstall_package.bat

@ECHO BUILD DOCUMENTATION
CALL .\ci\build_documentation.bat

