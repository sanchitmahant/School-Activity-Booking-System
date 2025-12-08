@echo off
REM ============================================================================
REM  ONE-CLICK SETUP AND RUN - School Activity Booking System
REM ============================================================================

echo.
echo ========================================
echo   Setting up School Activity Booking System
echo ========================================
echo.

REM 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM 2. Create Virtual Environment if missing
if not exist .venv (
    echo [1/4] Creating virtual environment...
    python -m venv .venv
) else (
    echo [1/4] Virtual environment exists.
)

REM 3. Activate and Install Dependencies
echo [2/4] Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM 4. Initialize Database
if not exist instance\school_activities.db (
    echo [3/4] Initializing database...
    python init_db.py
) else (
    echo [3/4] Database exists.
)

REM 5. Run Application
echo.
echo [4/4] Starting Application...
echo.
echo ========================================
echo   Server running at: http://127.0.0.1:5000
echo   Close this window to stop the server.
echo ========================================
echo.

python app.py
pause
