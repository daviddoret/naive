

REM TODO: COMMIT
REM TODO: PUSH

@ECHO
@ECHO INCREMENT PACKAGE VERSION
CALL .\ci\increment_package_version.bat
@ECHO
@ECHO BUILD PACKAGE
CALL .\ci\build_package.bat
@ECHO
@ECHO REINSTALL PACKAGE
CALL .\ci\reinstall_package.bat
@ECHO
@ECHO BUILD DOCUMENTATION
CALL .\ci\build_documentation.bat
@ECHO
