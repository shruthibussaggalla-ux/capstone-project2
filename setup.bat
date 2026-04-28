@echo off
REM SmartStudy Planner - Windows Setup Script

echo.
echo ========================================
echo   SmartStudy Planner - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    exit /b 1
)

REM Navigate to backend
echo [1/5] Navigating to backend directory...
cd backend || (echo Error: backend directory not found & exit /b 1)

REM Create virtual environment
echo [2/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

REM Run migrations
echo [4/5] Setting up database...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Database migration failed
    exit /b 1
)

REM Create superuser (optional)
echo [5/5] Creating superuser (optional)...
echo.
echo To skip superuser creation, press Ctrl+C
echo.
python manage.py createsuperuser

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Start the development server with:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then open in your browser:
echo   http://localhost:8001/frontend/auth.html
echo.
pause
