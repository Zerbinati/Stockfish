@echo off
:MENU
cls
echo ===========================
echo   Book Learning Automation
echo ===========================
echo.
echo Choose the game result:
echo 1. Win
echo 2. Loss
echo 3. Draw
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    set RESULT=win
) else if "%choice%"=="2" (
    set RESULT=loss
) else if "%choice%"=="3" (
    set RESULT=draw
) else if "%choice%"=="4" (
    exit
) else (
    echo Invalid choice.
    pause
    goto MENU
)

echo.
echo === Preparing book log for result: %RESULT% ===
python prepare_book_log_generic.py %RESULT%

echo.
echo === Applying learning updates ===
python apply_learn.py

echo.
echo Done. Press any key to close.
pause >nul

