@ECHO Commit the project to GitHub
@ECHO.


REM Stores credentials for automated execution.
REM git config --global credential.helper manager-core
REM References:
REM     * https://stackoverflow.com/questions/46878457/adding-git-credentials-on-windows

REM References
REM     * https://github.com/git-guides/git-commit

git -c credential.helper= -c core.quotepath=false -c log.showSignature=false status
git -c credential.helper= -c core.quotepath=false -c log.showSignature=false add .
git -c credential.helper= -c core.quotepath=false -c log.showSignature=false commit -am "build" --
git -c credential.helper= -c core.quotepath=false -c log.showSignature=false push --progress --porcelain origin refs/heads/master:master
