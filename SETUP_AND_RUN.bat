@echo off
setlocal EnableDelayedExpansion

TITLE School Activity Booking System - Auto Setup

echo ============================================================================
echo   SCHOOL ACTIVITY BOOKING SYSTEM - ONE-CLICK SETUP
echo ============================================================================
echo.

REM --- STEP 1: Detect Python ---
echo [1/5] Checking for Python...
set PYTHON_CMD=python

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    'python' command not found, trying 'py' launcher...
    py --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo.
        echo    [ERROR] Python is not installed on this computer!
        echo    Please install Python 3.10 or newer from: https://www.python.org/downloads/
        echo    IMPORTANT: Check the box "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
)
echo    Using: !PYTHON_CMD!
!PYTHON_CMD! --version

REM --- STEP 2: Create Virtual Environment ---
echo.
echo [2/5] Setting up isolated environment (This may take a moment)...
if not exist .venv (
    !PYTHON_CMD! -m venv .venv
    if !errorlevel! neq 0 (
        echo    [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo    Virtual environment created.
) else (
    echo    Virtual environment already exists.
)

REM --- STEP 3: Install Dependencies ---
echo.
echo [3/5] Installing required libraries...
call .venv\Scripts\activate.bat

REM Upgrade pip and install build tools FIRST to prevent installation errors
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

REM Install dependencies with error checking
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo    [ERROR] Failed to install some libraries.
    echo    Retrying with relaxed constraints...
    REM Fallback: Try installing individual critical packages if bulk install fails
    pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Mail reportlab psycopg2-binary email-validator
    if !errorlevel! neq 0 (
         echo.
         echo    [CRITICAL ERROR] Still unable to install dependencies.
         echo    Please check your internet connection and try again.
         pause
         exit /b 1
    )
)
echo    Dependencies installed successfully.

REM --- STEP 4: Setup Database ---
echo.
echo [4/5] Checking database...
if not exist instance\school_activities.db (
    echo    Initializing new database...
    python init_db.py
    if !errorlevel! neq 0 (
        echo    [WARN] Database init script encountered an issue, but we will try to proceed.
    )
) else (
    echo    Database found.
)

REM --- STEP 5: Launch ---
echo.
echo ============================================================================
echo   SETUP COMPLETE! Starting Application...
echo ============================================================================
echo.
echo   OPEN YOUR BROWSER TO: http://127.0.0.1:5000
echo   (Press Ctrl+C in this window to stop the server)
echo.

python app.py

echo.
echo [INFO] Application stopped.
pause
