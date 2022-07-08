@ECHO.
@ECHO REINSTALL PACKAGE
@ECHO.
REM BIBLIOGRAPHY
REM - https://snarky.ca/why-you-should-use-python-m-pip/

@ECHO.
@ECHO PIP UNINSTALL
@ECHO.
python -m pip uninstall naive -y

@ECHO.
@ECHO PIP INSTALL requirements.txt
@ECHO.
python -m pip install -r requirements.txt

@ECHO.
@ECHO PIP INSTALL
@ECHO.
REM python -m pip install naive
python -m pip install -e .