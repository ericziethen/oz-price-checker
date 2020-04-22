@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..\..
set PACKAGE_ROOT=ozpricechecker

pushd "%PROJ_MAIN_DIR%\%PACKAGE_ROOT%"

set IMPORT_DATE=2019.12.04

set DB_CSV_DIR=BaseData\Master Data

echo %date% - %time%

rem Check our Files Exists
if not exist "%DB_CSV_DIR%" echo Cannot find "%DB_CSV_DIR%" & goto error

rem Import the Rebrickable Data
python manage.py import_db_data "%DB_CSV_DIR%"
if %errorlevel% gtr 0 goto error

goto end

:error
echo ### DATA IMPORT WITH ERRORS ###
echo exit /B 1
exit /B 1

:end
echo %date% - %time%
echo ### DATA IMPORT OK ###
popd
endlocal
echo exit /B 0
exit /B 0
