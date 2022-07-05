@ECHO.
@ECHO REINSTALL PACKAGE
@ECHO.
REM Bibliography:
REM - https://snarky.ca/why-you-should-use-python-m-pip/

@ECHO PIP UNINSTALL
@ECHO.
python -m pip uninstall naive -y

@ECHO PIP INSTALL
@ECHO.
REM python -m pip install naive
python -m pip install -e .