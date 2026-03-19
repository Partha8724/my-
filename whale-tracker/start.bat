@echo off
setlocal

REM Run this file from the project root:
REM C:\Users\HP\crypto-whale-tracker\whale-tracker

set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"
set "FRONTEND_DIR=%PROJECT_DIR%frontend"
set "PYTHON_CMD=py"

if not exist "%BACKEND_DIR%" (
    echo Backend folder not found:
    echo %BACKEND_DIR%
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo Frontend folder not found:
    echo %FRONTEND_DIR%
    pause
    exit /b 1
)

where py >nul 2>&1
if errorlevel 1 (
    where python >nul 2>&1
    if errorlevel 1 (
        echo Python was not found in PATH.
        echo Install Python and make sure "python" or "py" works in CMD.
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

echo Starting backend in a new CMD window...
start "Whale Tracker Backend" cmd /k ""title Whale Tracker Backend && cd /d "%BACKEND_DIR%" && %PYTHON_CMD% -m uvicorn app.main:app --reload""

echo Starting frontend in a new CMD window...
start "Whale Tracker Frontend" cmd /k ""title Whale Tracker Frontend && cd /d "%FRONTEND_DIR%" && npm run dev""

echo.
set /p OPEN_BROWSER=Open http://localhost:5173 in your browser too? (Y/N, default Y): 
if /I not "%OPEN_BROWSER%"=="N" (
    start "" "http://localhost:5173"
)

echo.
echo Backend and frontend launch commands were started.
echo To stop them later, run stop.bat
pause
