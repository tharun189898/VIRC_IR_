@echo off
title VIRC QC Testing Station Launcher
echo.
echo ========================================
echo    VIRC QC Testing Station Launcher
echo ========================================
echo.
echo Starting VIRC QC Testing Station...
echo Please wait while the application loads...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import hid" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        echo.
        pause
        exit /b 1
    )
)

REM Check if Pillow is installed for image support
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Launch the GUI
echo.
echo Launching VIRC QC Testing Station...
python complete_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo The application encountered an error.
    pause
) 