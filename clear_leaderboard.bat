@echo off

REM Go to project folder (location of this .bat)
cd /d %~dp0

if not exist leaderboard.txt (
    echo leaderboard.txt not found. Nothing to clear.
    pause
    exit /b 0
)

echo This will erase all saved player names and scores.
set /p confirm=Type YES to continue: 

if /I not "%confirm%"=="YES" (
    echo Cancelled.
    pause
    exit /b 0
)

break > leaderboard.txt
echo leaderboard.txt has been cleared.
pause
