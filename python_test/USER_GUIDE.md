# 🚀 VIRC QC Testing Station - User Guide

## For Users

### 📋 What This Does
This application tests remote controls to make sure all buttons work correctly. Perfect for quality control testing of remote controls from third-party suppliers.

### 🎯 How to Use (3 Easy Steps)

#### Step 1: Launch the Application
**Double-click on:** `Launch_VIRC_QC_Station.bat`

- The first time you run it, it may install some required software automatically
- Wait for the application window to open

#### Step 2: Connect Your VIRC Device
1. Plug in your VIRC device (Raspberry Pi Pico) to your computer via USB
2. The application will automatically detect and connect to it
3. You'll see "Connected" status and device information

#### Step 3: Test Remote Controls
1. Click **"Start QC Test"** button
2. Point the remote control at the VIRC receiver
3. Press each button on the remote as instructed
4. Watch for green checkmarks ✅ (working) or red X's ❌ (not working)
5. When done, click **"Export Results"** to save a test report

### 📊 Understanding Results

- **✅ Green checkmarks** = Button works correctly
- **❌ Red marks** = Button failed or not working
- **🔄 Repeat marks** = Button already tested
- **Test Report** = Saved file with complete results

### 🔧 Troubleshooting

**Problem:** Application won't start
- **Solution:** Make sure Python is installed from https://python.org

**Problem:** No device detected
- **Solution:** Check USB cable and make sure VIRC device is connected

**Problem:** Remote not responding
- **Solution:** Point remote directly at VIRC receiver and press buttons firmly

### 📞 Support
If you need help, share the test report file and describe what happened.

---
*VIRC QC Testing Station - Professional Remote Control Testing* 