@echo off
title VIRC QC Testing Station - One-Time Setup
echo.
echo ================================================
echo    VIRC QC Testing Station - Initial Setup
echo ================================================
echo.
echo This will set up the VIRC QC Testing Station on your computer.
echo You only need to run this ONCE.
echo.
echo What this setup will do:
echo  ✓ Check if Python is installed
echo  ✓ Install required software packages
echo  ✓ Create a desktop shortcut
echo  ✓ Test the installation
echo.
set /p CONTINUE="Press Y to continue, or N to cancel: "
if /i "%CONTINUE%" NEQ "Y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo ========================================
echo Step 1: Checking Python Installation...
echo ========================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Python is not installed!
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org
    echo 2. Download Python 3.7 or newer
    echo 3. Install it (make sure to check "Add Python to PATH")
    echo 4. Restart your computer
    echo 5. Run this setup again
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo ✓ Python is installed
)

echo.
echo ==========================================
echo Step 2: Installing Required Packages...
echo ==========================================

echo Installing required packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install required packages
    pause
    exit /b 1
)
echo ✓ All required packages installed successfully

echo.
echo =======================================
echo Step 3: Creating Desktop Shortcut...
echo =======================================

call "Create_Desktop_Shortcut.bat"

echo.
echo ============================
echo Step 4: Testing Setup...
echo ============================

echo Testing if GUI can start...
python -c "import tkinter; import hid; print('✓ All required components are working')" 2>nul
if errorlevel 1 (
    echo ✗ There may be an issue with the installation
    echo ✓ But basic packages are installed, try running the application
) else (
    echo ✓ Setup test passed
)

echo.
echo ================================================
echo           SETUP COMPLETE! 🎉
echo ================================================
echo.
echo ✓ VIRC QC Testing Station is ready to use!
echo.
echo To start the application:
echo   • Double-click "VIRC QC Testing Station" on your Desktop
echo   OR
echo   • Double-click "Launch_VIRC_QC_Station.bat" in this folder
echo.
echo For help, read "QC_TESTING_USER_MANUAL.txt"
echo.
echo Press any key to finish...
pause >nul 