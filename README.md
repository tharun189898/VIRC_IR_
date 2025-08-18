# VIRC - Virtusense IR Controller
## Developement setup:
1. Install Arduino IDE
2. Install Arduino Core by Earl https://github.com/earlephilhower/arduino-pico (3.2.1)
3. Select Tools > USB Stack > Adafruit tinyUSB
4. Tools > Board > RaspberryPi Pico
5. Plugin the VIRC Hardware by setting in bootmode.
6. Upload the program
## Test setup - Python
1. Install python3.
2. Create a Virtual Environment. 
3. Activate virtual Environment.
4. Install python3 HID package https://pypi.org/project/hid/
5. Run the python script. 

## Complete Testing Guide

### Step 1: Hardware Setup
1. Connect your VIRC Hardware (Raspberry Pi Pico) to your computer via USB
2. Hold the BOOTSEL button while plugging in to enter bootloader mode
   - The Pico should appear as a USB drive when done correctly
3. Have an IR remote control ready for testing (any standard remote will work)

### Step 2: Upload Firmware
1. Open Arduino IDE
2. Set the following in Tools menu:
   - Board: "RaspberryPi Pico"
   - USB Stack: "Adafruit TinyUSB"
3. Open `virc_firmware.ino` from this project
4. Click Upload button (→) in Arduino IDE
5. Wait for "Upload Complete" message

### Step 3: Python Test Setup
1. Open Command Prompt/Terminal
2. Navigate to the project's python_test folder:
   ```
   cd path/to/virc-main/python_test
   ```
3. Create and activate virtual environment:
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```
4. Install required package:
   ```
   pip install hid
   ```

### Step 4: Testing
1. Run the Python test script:
   ```
   python main.py
   ```
2. You should see:
   - Device information printed
   - Three version/type messages
3. Point any IR remote at the VIRC receiver
4. Press buttons on the remote
5. You should see output like:
   ```
   Received from HID Device: [7, 0, XX, XX, XX, XX, 0, 0, ...]
   ```
   Where XX XX XX XX will be different numbers for each button

### Troubleshooting
- If no device found: Check if Pico is properly connected and firmware uploaded
- If no IR codes showing: Make sure remote is pointing directly at the receiver
- If Python errors: Verify virtual environment is activated and hid package installed

### Observation: Looks like somewhere in between the arduino core programs the RP2040 with VID- 0x239a which is Adafruit Vendor ID. But our desired vendor ID is  0x2e8a which is Raspberry Pi Vendor ID. to make sure we use our desired vendorID we need to add a line in Arduino code before usb_hid.begin().

