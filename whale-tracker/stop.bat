@echo off
setlocal

REM This closes the CMD windows opened by start.bat.
REM It looks for the window titles we set when starting backend and frontend.

echo Stopping backend window...
taskkill /FI "WINDOWTITLE eq Whale Tracker Backend*" /T /F >nul 2>&1

echo Stopping frontend window...
taskkill /FI "WINDOWTITLE eq Whale Tracker Frontend*" /T /F >nul 2>&1

echo.
echo If both windows were open, they should now be closed.
echo If a server is still running, close that CMD window manually.
pause
