@echo off

setlocal

:check_arguments
if [%1] == [] (
    echo No Path Specified for Data to Import
    goto error
) else (
    set DB_CSV_DIR=%1

    rem Some magic to remove annoying double quotes
    rem https://stackoverflow.com/questions/1964192/removing-double-quotes-from-variables-in-batch-file-creates-problems-with-cmd-en
    set DB_CSV_DIR=%DB_CSV_DIR:"='%

    echo Base Dir set to '%DB_CSV_DIR%'
    goto data_import
)

:data_import
set PROJ_MAIN_DIR=%~dp0..\..
set PACKAGE_ROOT=ozpricechecker

pushd "%PROJ_MAIN_DIR%\%PACKAGE_ROOT%"

echo %date% - %time%

rem Check our Files Exists
if not exist "%DB_CSV_DIR%" echo Cannot find "%DB_CSV_DIR%" & goto error

rem Import the Data
echo Calling 'python manage.py import_db_data "%DB_CSV_DIR%"'
python manage.py import_db_data "%DB_CSV_DIR%"
if %errorlevel% gtr 0 goto error

goto end

:error
echo ### DATA IMPORT WITH ERRORS ###
echo exit /B 1
popd
exit /B 1

:end
echo %date% - %time%
echo ### DATA IMPORT OK ###
popd
endlocal
echo exit /B 0
exit /B 0
