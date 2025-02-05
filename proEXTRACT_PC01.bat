@echo off
:start
cls
python C:\Projects\_extensions\proEXTRACT\proEXTRACT_PC01.py %1
echo.
echo Process complete.
echo.
echo Enter ' to search again or any other key to exit.
set /p "choice="
if "%choice%"=="'" goto start
echo.
echo Exiting...
timeout /t 2 > nul
