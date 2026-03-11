@echo off

echo Starting AI Hand Cricket...

REM Go to the folder where this bat file is located
cd /d %~dp0

REM Activate virtual environment
call .\venv\Scripts\activate.bat

REM Run the program
python main.py

echo.
echo Game closed.
pause