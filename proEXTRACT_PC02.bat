@echo off
:start
cls
python C:\Projects\_extensions\proEXTRACT\proEXTRACT_PC02.py --config="C:\\Projects\\_extensions\\proEXTRACT\\base_config2.json"
echo.
echo Process complete.
echo.
echo Enter ' to search again or any other key to exit.
set /p "choice="
if "%choice%"=="'" goto start
echo.
echo Exiting...
timeout /t 2 > nul
