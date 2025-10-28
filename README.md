# VIRC - Virtusense IR Controller
## Quality Control Testing Station

Complete guide for setting up and using the VIRC IR remote testing system.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Firmware Setup](#firmware-setup-one-time-per-device)
3. [Python Application Setup](#python-application-setup)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

**Hardware:**
- Raspberry Pi Pico with IR receiver module (GPIO 15)
- USB cable (USB-A to Micro-USB)
- IR remote controls for testing

**Software:**
- Arduino IDE (https://www.arduino.cc/en/software)
- Python 3.8 or higher (https://python.org)

---

## Firmware Setup (One-Time per Device)

### Step 1: Install Arduino IDE & Board Support
1. Download and install Arduino IDE
2. Open Arduino IDE → **File → Preferences**
3. In "Additional Board Manager URLs", add:
   ```
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
   ```
4. Click **Tools → Board → Boards Manager**
5. Search for **"pico"**
6. Install: **"Raspberry Pi Pico/RP2040"** by Earle F. Philhower III (v3.2.1 or higher)

### Step 2: Install Required Libraries
1. Click **Sketch → Include Library → Manage Libraries**
2. Search and install the following:
   - **"Adafruit TinyUSB Library"** (v1.14.3 or higher)
     - Click "Install All" for dependencies
   - **"IRremote"** by Arduino-IRremote (v3.6.1 or higher)

### Step 3: Upload Firmware to Pico

**A. Put Pico in Bootloader Mode:**
1. **Unplug** the Pico from USB
2. **Hold down** the white BOOTSEL button on the Pico
3. While holding, **plug USB cable** into computer
4. Hold for 2 seconds, then **release**
5. Pico should appear as USB drive named **"RPI-RP2"**

**B. Configure Arduino IDE:**
1. **Tools → Board** → Raspberry Pi RP2040 Boards → **Raspberry Pi Pico**
2. **Tools → USB Stack** → **Adafruit TinyUSB** ⚠️ (Important!)
3. **Tools → Port** → Select the COM port showing "Raspberry Pi Pico"

**C. Upload Firmware:**
1. **File → Open** → Navigate to `virc_firmware/virc_firmware.ino`
2. Click the **Upload button (→)** at the top
3. Wait for compilation and upload (may take 1-2 minutes)
4. Look for **"Done uploading"** message

**D. Verify Upload:**
1. **Tools → Serial Monitor** (set baud to **115200**)
2. You should see:
   ```
   Starting VIRC...
   IR Receiver initialized
   ```
3. ✅ Success! Close Arduino IDE (not needed anymore)

---

## Python Application Setup

### Install Python Dependencies
1. Open Command Prompt/Terminal
2. Navigate to the project folder:
   ```bash
   cd path/to/virc-main/python_test
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Installs: hidapi and pillow)*

---

## Running the Application

### Launch the QC Testing Station

```bash
cd python_test
python complete_gui.py
```

The GUI application will:
- Auto-connect to the VIRC device
- Display device information
- Provide a complete testing interface

### Quick Test (CLI Alternative)
```bash
cd python_test
python main.py
```

---

## Using the Application

### QC Testing Workflow

1. **Connect Device**
   - Plug in VIRC device via USB
   - Wait for "Auto-connected" status

2. **Start Test**
   - Click **"Start QC Test"** button
   - Test checklist appears

3. **Test Remote**
   - Point remote at VIRC receiver (6-12 inches)
   - Press each button on the remote:
     - Short Pause
     - Long Pause
     - Bed Mode
     - Chair Mode
     - Square Button
     - Triangle Button
   - Each button shows ✅ (pass) or ❌ (fail)

4. **Export Results**
   - When complete, click **"Export Results"**
   - File saved as: `QC_Test_Results_[timestamp].txt`

5. **Test Next Remote**
   - Click **"Reset Test"**
   - Repeat from step 2

### Keyboard Shortcuts
- **Ctrl+S** - Start/Stop listening
- **Ctrl+L** - Clear log
- **Ctrl+T** - Start QC test

---

## Troubleshooting

### Device Not Found
- ✓ Check USB cable is connected
- ✓ Verify firmware is uploaded correctly
- ✓ Try different USB port
- ✓ Click "Refresh Devices" button
- ✓ Check Device Manager for "VIRC Controller"

### No IR Signals Detected
- ✓ Click "Start Listening" button
- ✓ Point remote DIRECTLY at IR receiver
- ✓ Move closer (6-12 inches optimal)
- ✓ Check remote batteries
- ✓ Verify IR receiver LED blinks when pressing buttons

### Firmware Upload Fails
- ✓ Make sure "Adafruit TinyUSB" is selected in USB Stack
- ✓ Verify Pico is in bootloader mode (BOOTSEL button)
- ✓ Try different USB cable (some are power-only)
- ✓ Close Serial Monitor if open
- ✓ Run Arduino IDE as Administrator

### Python Errors
- ✓ Verify Python 3.8+ is installed: `python --version`
- ✓ Reinstall packages: `pip install -r requirements.txt`
- ✓ Check that you're in the `python_test` directory

### Application Freezes
- ✓ Close and restart application
- ✓ Unplug and replug VIRC device
- ✓ Restart computer if persistent

---

## Supported Remote Types

**White Remote (Scanmode 1):**
- IR Codes ending in: `0x7F80`
- 6 buttons: Short Pause, Long Pause, Bed Mode, Chair Mode, Square, Triangle

**Black Remote (Scanmode 2):**
- IR Codes ending in: `0xFF00`
- 6 buttons: Short Pause, Long Pause, Bed Mode, Chair Mode, Square, Triangle

---

## File Structure

```
virc-main/
├── README.md                          # This file
├── QC_TESTING_USER_MANUAL.txt         # Detailed user manual
├── CHANGELOG.txt                      # Version history
├── virc_firmware/
│   ├── virc_firmware.ino              # Main firmware
│   └── PinDefinitionsAndMore.h        # IR library config
└── python_test/
    ├── complete_gui.py                # Main QC application ⭐
    ├── main.py                        # Simple CLI test
    ├── requirements.txt               # Python dependencies
    └── USER_GUIDE.md                  # End-user guide
```

---

## Technical Notes

- The Arduino core programs RP2040 with VID 0x239a (Adafruit) by default
- Application supports both Adafruit VID (0x239a) and Raspberry Pi VID (0x2e8a)
- IR receiver should be connected to GPIO 15 on the Pico
- HID communication uses Report ID 7 for IR data transfer

---

## Version Information

- **Version**: 1.2
- **Last Updated**: 2025-10-28
- **Firmware**: virc_firmware v1.1
- **Application**: complete_gui.py v1.2

---

## Support

For detailed daily operations and QC workflows, see: **QC_TESTING_USER_MANUAL.txt**

For technical issues:
- Check troubleshooting section above
- Review QC_TESTING_USER_MANUAL.txt for detailed guidance
- Contact your technical support team
