@echo off

setlocal

rem This is just an Example how to call the Scrape Django Command

set PROJ_MAIN_DIR=%~dp0..\..
set PACKAGE_ROOT=ozpricechecker

pushd "%PROJ_MAIN_DIR%\%PACKAGE_ROOT%"

set CHROME_EXEC_PATH=D:\temp\# Chrome Portable\GoogleChromePortable81\GoogleChromePortable.exe
set CHROME_EXEC_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_WEBDRIVER_PATH=D:\temp\# Chrome Portable\chromedriver_win32\81.0.4044.69\chromedriver.exe

echo Calling 'python manage.py scrape_products "%CHROME_EXEC_PATH%" "%CHROME_WEBDRIVER_PATH%"'
python manage.py scrape_products "%CHROME_EXEC_PATH%" "%CHROME_WEBDRIVER_PATH%"

popd
endlocal
