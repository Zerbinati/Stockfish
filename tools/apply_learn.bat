@echo off
setlocal

:: Set the match result: win / loss / draw
set RESULT=win

:: Set the delta to apply for each type of result
set WIN_DELTA=500
set LOSS_DELTA=-500
set DRAW_DELTA=0

:: Calculate the actual value of delta
if "%RESULT%"=="win"  set DELTA=%WIN_DELTA%
if "%RESULT%"=="loss" set DELTA=%LOSS_DELTA%
if "%RESULT%"=="draw" set DELTA=%DRAW_DELTA%

:: Files to read
set LOG_FILE=book_usage.log

echo Applying learn update with result=%RESULT% (delta=%DELTA%)

for /f "tokens=3,4 delims== " %%a in (%LOG_FILE%) do (
    set KEY=%%a
    set MOVE=%%b
    call :apply %%a %%b
)

goto :eof

:apply
echo Updating: key=%1 move=%2
learn_tool.exe book.bin %1 %2 %DELTA%
goto :eof
