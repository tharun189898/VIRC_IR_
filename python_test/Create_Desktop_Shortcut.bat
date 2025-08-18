@echo off
title Create Desktop Shortcut for VIRC QC Station
echo.
echo ===============================================
echo    Creating Desktop Shortcut for VIRC QC
echo ===============================================
echo.

REM Get the current directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "BATCH_FILE=%SCRIPT_DIR%Launch_VIRC_QC_Station.bat"

REM Create VBScript to create shortcut
set "VBS_FILE=%TEMP%\create_shortcut.vbs"

echo Creating shortcut on Desktop...
echo.

REM Generate VBScript content
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = oWS.SpecialFolders^("Desktop"^) ^& "\VIRC QC Testing Station.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%BATCH_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
echo oLink.Description = "VIRC Quality Control Testing Station"
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,137"
echo oLink.Save
) > "%VBS_FILE%"

REM Execute VBScript
cscript //nologo "%VBS_FILE%"

REM Clean up
del "%VBS_FILE%" >nul 2>&1

if exist "%USERPROFILE%\Desktop\VIRC QC Testing Station.lnk" (
    echo ✓ SUCCESS: Desktop shortcut created successfully!
    echo.
    echo You can now double-click "VIRC QC Testing Station" 
    echo on your Desktop to launch the application.
) else (
    echo ✗ ERROR: Failed to create desktop shortcut.
    echo You can still use Launch_VIRC_QC_Station.bat directly.
)

echo.
echo Press any key to close...
pause >nul 