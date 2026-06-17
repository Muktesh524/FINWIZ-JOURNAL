@echo off
REM FinWiz Journal - Quick Start Script for Windows

echo.
echo ========================================
echo   FinWiz Journal - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment.
        echo Make sure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

REM Install/update dependencies
echo.
echo Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies.
    pause
    exit /b 1
)

REM Run Streamlit app
echo.
echo Starting FinWiz Journal...
echo.
echo The app will open at: http://localhost:8501
echo.

streamlit run app.py

pause
