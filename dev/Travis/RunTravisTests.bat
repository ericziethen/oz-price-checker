@echo off

setlocal

rem From https://graysonkoonce.com/getting-the-current-branch-name-during-a-pull-request-in-travis-ci/
if "%TRAVIS_PULL_REQUEST%" == "false" (
    set FROM_BRANCH=%TRAVIS_BRANCH%
) else (
    set FROM_BRANCH=%TRAVIS_PULL_REQUEST_BRANCH%
)

echo "TRAVIS_BRANCH=%TRAVIS_BRANCH%, PR=%PR%, FROM_BRANCH=%FROM_BRANCH%"

if "%TRAVIS_BRANCH%" == "%FROM_BRANCH%" goto branch_ok
if not "%TRAVIS_BRANCH%" == "master" goto branch_ok
if "%FROM_BRANCH%" == "development" goto branch_ok

rem if we come here we have a branch issue
goto branch_issue

:branch_ok
echo "No Merging Issue"
goto exit_ok

:branch_issue
echo "*** Cannot Merge Branch '%FROM_BRANCH%' into '%TRAVIS_BRANCH%'"
goto exit_error

:exit_error
popd
endlocal
echo exit /B 1
exit /B 1

:exit_ok
popd
endlocal
echo exit /B 0
exit /B 0
