@echo off
echo ========================================
echo AI Coding Mentor - Frontend Setup
echo ========================================
echo.

cd frontend

echo [1/2] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/2] Setup complete!
echo.
echo ========================================
echo To start the frontend:
echo   1. cd frontend
echo   2. npm start
echo ========================================
echo.
pause
