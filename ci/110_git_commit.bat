
REM References
REM     * https://github.com/git-guides/git-commit

git -c credential.helper= -c core.quotepath=false -c log.showSignature=false commit -m "build" --
git -c credential.helper= -c core.quotepath=false -c log.showSignature=false push --progress --porcelain origin refs/heads/master:master
