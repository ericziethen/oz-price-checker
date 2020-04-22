@echo off

setlocal

set SCRIPT_DIR=%~dp0
set PROJ_MAIN_DIR=%SCRIPT_DIR%..\..
set PACKAGE_ROOT=%PROJ_MAIN_DIR%\ozpricechecker
set DB_CSV_DIR=%PACKAGE_ROOT%\BaseData\MasterData

call "%SCRIPT_DIR%\data_import.bat" "%DB_CSV_DIR%"

endlocal
