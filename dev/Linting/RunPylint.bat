@echo off

setlocal

set BATCH_DIR=%~dp0
set PROJ_MAIN_DIR=%BATCH_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\ozpricechecker
set ERROR_FOUND=
set ERROR_LIST=

set PYTHONPATH=%PYTHONPATH%;%MODULE_PATH%

: Pylint requires __init__.py files to run, but the Django root doesn't have it so we have to specify the folders separately
call:run_pylint "%MODULE_PATH%\ozpricechecker"
call:run_pylint "%MODULE_PATH%\inventory"

if defined ERROR_FOUND (
    goto exit_error
) else (
    goto exit_ok
)

:exit_error
endlocal
exit /B 1

:exit_ok
endlocal
exit /B 0


: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################
:run_pylint
set LINT_PATH=%~1

echo ### PYLINT START - '%LINT_PATH%' ###
pylint --load-plugins pylint_django "%LINT_PATH%"
set return_code=%errorlevel%
if %return_code% gtr 0 (
    set ERROR_FOUND=TRUE
    set ERROR_LIST=%ERROR_LIST% %LINT_PATH%
    echo   Issues Found
) else (
    echo   No Issues
)
echo ### PYLINT END - '%LINT_PATH%' ###
echo[
goto:eof
: #######################################
: ##### END OF FUNCTION DEFINITIONS #####
: #######################################
