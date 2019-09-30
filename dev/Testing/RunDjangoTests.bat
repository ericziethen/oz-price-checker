@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0../..
set PACKAGE_ROOT=ozpricechecker

:run_django_test
python "%PROJ_MAIN_DIR%\%PACKAGE_ROOT%\manage.py" test
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Test Issues Found
    goto exit_ok
) else (
    echo *** Some Test Issues Found
    goto exit_error
)

:exit_error
endlocal
echo exit /B 1
exit /B 1

:exit_ok
endlocal
echo exit /B 0
exit /B 0
