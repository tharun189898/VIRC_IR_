# VIRC Complete GUI - Usage Instructions

## Overview
This GUI provides the exact same functionality as the main.py command-line tool, but with a user-friendly graphical interface.

## Installation
1. Install Python 3.7 or higher
2. Install required package:
   ```bash
   pip install hidapi
   ```

## Usage
1. Connect your VIRC hardware (Raspberry Pi Pico) to your computer
2. Ensure firmware is uploaded to the Pico
3. Run the GUI from the python_test directory:
   ```bash
   cd python_test
   python complete_gui.py
   ```

## Features (100% match with main.py)
- **Device Enumeration**: Lists all HID devices and VIRC devices
- **Device Information**: Retrieves device type, API version, and firmware version
- **IR Signal Monitoring**: Real-time display of received IR signals
- **Button Name Mapping**: Maps IR codes to button names (Short Pause, Long Pause, etc.)
- **Remote Type Detection**: Identifies white vs black remotes
- **Error Handling**: Automatic reconnection attempts
- **Timestamp Logging**: All events are timestamped

## GUI Components
- **Device Management**: Select, connect, and disconnect devices
- **Device Information Panel**: Displays manufacturer, product, and version info
- **IR Signal Monitor**: Real-time log of IR signals with button names and remote types
- **Control Buttons**: Start/stop listening and clear log

## Quick Start
1. Run `python complete_gui.py`
2. Click "Refresh Devices" to find VIRC devices
3. Select your device from the dropdown
4. Click "Connect"
5. Click "Get Device Info" to retrieve device details
6. Click "Start Listening" to begin monitoring IR signals
7. Point any IR remote at the VIRC receiver and press buttons
8. Watch the IR codes, button names, and remote types appear in real-time
