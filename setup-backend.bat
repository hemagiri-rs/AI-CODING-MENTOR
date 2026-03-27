@echo off
echo ========================================
echo AI Coding Mentor - Backend Setup
echo ========================================
echo.

cd backend

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo.
    echo *** IMPORTANT ***
    echo Please edit backend\.env and add your GROQ_API_KEY
    echo Get your key from: https://console.groq.com/keys
    echo.
)

echo [5/5] Setup complete!
echo.
echo ========================================
echo To start the backend:
echo   1. cd backend
echo   2. venv\Scripts\activate
echo   3. python app.py
echo ========================================
echo.
pause
