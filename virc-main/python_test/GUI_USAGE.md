# VIRC Basic GUI - Usage Instructions

## Installation
1. Install Python 3.7 or higher
2. Install required package:
   ```bash
   pip install -r gui_requirements.txt
   ```

## Usage
1. Connect your VIRC hardware (Raspberry Pi Pico) to your computer
2. Ensure firmware is uploaded to the Pico
3. Run the GUI from the python_test directory:
   ```bash
   cd python_test
   python basic_gui.py
   ```

## Features
- **Device Selection**: Dropdown to select from available VIRC devices
- **Connect/Disconnect**: Simple connection management
- **Real-time IR Monitoring**: Live display of received IR signals
- **Timestamp Logging**: Each IR signal is timestamped
- **Start/Stop Listening**: Control when to monitor IR signals

## Quick Start
1. Run `python basic_gui.py` from the python_test directory
2. Click "Refresh" to find devices
3. Select your VIRC device from dropdown
4. Click "Connect"
5. Click "Start Listening"
6. Point IR remote at VIRC receiver and press buttons
