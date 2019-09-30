@echo off

setlocal

rem DON'T CHANGE, ALSO USED FOR KILLING
set SERVER_WINDOW_NAME=python_test_server

set PROJ_MAIN_DIR=%~dp0..
set TEST_SERVER_DIR=%PROJ_MAIN_DIR%\tests\TestServerContent

rem --directory only available since Python 3.7
set COMMAND=python -m http.server --bind localhost 8000

pushd "%TEST_SERVER_DIR%"

if [%1] == [] (
    echo No Argument Found, run attached
    goto run_attached
) else (
    echo Argument Found, run detached
    goto run_detached
)

:run_attached
%COMMAND%
goto end

:run_detached
start "%SERVER_WINDOW_NAME%" %COMMAND%
echo Command: 'tasklist /V /FI "imagename eq python.exe"'
tasklist /V /FI "imagename eq python.exe"
goto end

:end
popd
endlocal
