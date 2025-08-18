================================================================================
                 VIRC QC Testing Station - Quick Start Guide
================================================================================

📋 WHAT IS THIS?
This software tests remote controls to make sure all buttons work correctly.
Perfect for quality control of remote controls from suppliers.

🎯 FIRST TIME SETUP (Do this once):

1. DOUBLE-CLICK: "SETUP_VIRC_QC_STATION.bat"
   - Follow the instructions on screen
   - It will install everything automatically
   - Creates a desktop shortcut for easy access

2. If you don't have Python installed:
   - Go to https://python.org
   - Download and install Python 3.7+
   - IMPORTANT: Check "Add Python to PATH" during installation
   - Restart your computer
   - Run setup again

🚀 HOW TO USE (Every time):

1. Connect your VIRC device to USB port
2. DOUBLE-CLICK: "VIRC QC Testing Station" on Desktop
   OR
   DOUBLE-CLICK: "Launch_VIRC_QC_Station.bat"
3. The application will open automatically
4. Click "Start QC Test"
5. Point remote at VIRC receiver and press each button
6. Watch for ✅ (working) or ❌ (broken) indicators
7. Click "Export Results" to save test report

📁 FILES IN THIS FOLDER:

SETUP_VIRC_QC_STATION.bat       ← RUN THIS FIRST (one-time setup)
Launch_VIRC_QC_Station.bat      ← Daily use (or use desktop shortcut)
Create_Desktop_Shortcut.bat     ← Creates desktop shortcut
USER_GUIDE.md                   ← Detailed instructions
complete_gui.py                 ← Main application (don't edit)

📞 TROUBLESHOOTING:

Problem: "Python not found"
Solution: Install Python from https://python.org

Problem: "No device detected"  
Solution: Check USB cable, make sure VIRC device is connected

Problem: Remote not working
Solution: Point remote directly at VIRC receiver, press buttons firmly

Problem: Application won't start
Solution: Run SETUP_VIRC_QC_STATION.bat again

💡 TIPS:
- Keep this folder together (don't move individual files)
- Test reports are saved in this same folder with timestamps
- Each remote test takes 2-3 minutes depending on number of buttons
- Works with both white and black VirtuSense remotes

================================================================================
Support: Share the test report file if you need help
================================================================================ 