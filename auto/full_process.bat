
@ECHO BUILD PACKAGE

CALL .\auto\build_package.bat

@ECHO REINSTALL PACKAGE

CALL .\auto\reinstall_package.bat

@ECHO BUILD DOCUMENTATION

CALL .\docs\make html