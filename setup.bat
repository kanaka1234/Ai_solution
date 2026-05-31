@echo off
REM Quick setup script for AI Agent Platform on Windows

echo.
echo ========================================
echo AI Agent Platform - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Initializing database...
python init.py
if errorlevel 1 (
    echo Error: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open a new terminal and run:
echo    venv\Scripts\activate.bat
echo    python backend\runtime.py
echo.
echo 2. Open another terminal and run:
echo    venv\Scripts\activate.bat
echo    streamlit run frontend\app.py
echo.
echo 3. Open http://localhost:8501 in your browser
echo.
pause
