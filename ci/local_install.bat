@ECHO.
@ECHO REINSTALL PACKAGE
@ECHO.
REM BIBLIOGRAPHY
REM - https://snarky.ca/why-you-should-use-python-m-pip/

@ECHO PIP UNINSTALL
@ECHO.
python -m pip uninstall naive -y

@ECHO PIP REQUIREMENTS
@ECHO.
python -m pip -r ../../requirements.txt

@ECHO PIP INSTALL
@ECHO.
REM python -m pip install naive
python -m pip install -e .