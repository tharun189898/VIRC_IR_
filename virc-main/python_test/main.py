import hid  # Changed back from hidapi
import sys
import time

# Adafruit VID (0x239a)
USB_VID = 0x239a
USB_PID = 0xcafe  # Add PID constant

def list_all_devices():
    print("\nAll HID devices:")
    for device in hid.enumerate():
        print(f"VID: 0x{device['vendor_id']:04x}, PID: 0x{device['product_id']:04x}, Manufacturer: {device.get('manufacturer_string', 'N/A')}")
    print()

def ir_code_name(ir_code):
    code_map = {
        0xFE017F80: "Short Pause",
        0xFC037F80: "Long Pause",
        0xFB047F80: "Bed Mode",
        0xF9067F80: "Chair Mode",
        0xF8077F80: "Square Button",
        0xF6097F80: "Triangle Button",
        0xFE01FF00: "Short Pause",
        0xFC03FF00: "Long Pause",
        0xFB04FF00: "Bed Mode",
        0xF906FF00: "Chair Mode",
        0xF807FF00: "Square Button",
        0xF609FF00: "Triangle Button"
    }
    return code_map.get(ir_code, "Unknown Button")

def detect_remote_type(ir_code):
    # Example: IR_Scanmode mapping for white remote is 1, black remote is 2
    # You can adjust the ranges or codes as needed
    white_remote_codes = {
        0xFE017F80, 0xFC037F80, 0xFB047F80, 0xF9067F80, 0xF8077F80, 0xF6097F80
    }
    black_remote_codes = {
        0xFE01FF00, 0xFC03FF00, 0xFB04FF00, 0xF906FF00, 0xF807FF00, 0xF609FF00
        # Add more black remote codes here as needed
    }
    if ir_code in white_remote_codes:
        return "White Remote (Scanmode 1)"
    elif ir_code in black_remote_codes:
        return "Black Remote (Scanmode 2)"
    else:
        return "Unknown Remote"

def main():
    list_all_devices()
    print("Searching for VIRC device...")
    devices = list(hid.enumerate(USB_VID))
    
    if not devices:
        print(f"No devices found with VID 0x{USB_VID:04x}")
        print("Please check:")
        print("1. Device is connected")
        print("2. Firmware is uploaded correctly")
        print("3. Device appears in Device Manager")
        sys.exit(1)

    print(f"Found {len(devices)} device(s):")
    for device in devices:
        print(f"VID: 0x{device['vendor_id']:04x}, PID: 0x{device['product_id']:04x}")

    try:
        dev = hid.device()
        dev.open(USB_VID, devices[0]['product_id'])
        print(f"\nSuccessfully opened device")
        print(f"Manufacturer: {devices[0]['manufacturer_string']}")
        print(f"Product: {devices[0]['product_string']}")
        
        # Initialize device
        commands = [
            (b'\x00\x01', "Device Type"),
            (b'\x00\x03', "API Version"),
            (b'\x00\x05', "Firmware Version")
        ]

        for cmd, desc in commands:
            print(f"\nGetting {desc}...")
            dev.write(cmd)
            response = dev.read(64, 1000)  # timeout as positional argument
            print(f"{desc} response:", response)

        print("\nWaiting for IR signals... (Press Ctrl+C to exit)")
        print("Press any button on your remote to detect remote type...")
        while True:
            try:
                response = dev.read(64, 100)
                if response:
                    if response[0] == 7:
                        ir_code = 0
                        for i in range(4):
                            ir_code |= response[2+i] << (8*i)
                        name = ir_code_name(ir_code)
                        remote_type = detect_remote_type(ir_code)
                        print("\nReceived IR signal:")
                        print(f"Raw bytes: {[hex(x) for x in response[:6]]}")
                        print(f"IR Code: 0x{ir_code:08X} : {name}")
                        print(f"Detected remote type: {remote_type}")
            except Exception as e:
                print(f"HID error: {e}")
                print("Device may have been disconnected. Attempting to reconnect...")
                dev.close()
                # Try to reconnect
                for attempt in range(10):
                    time.sleep(1)
                    devices = list(hid.enumerate(USB_VID))
                    if devices:
                        try:
                            dev = hid.device()
                            dev.open(USB_VID, devices[0]['product_id'])
                            print("Reconnected to device.")
                            break
                        except Exception as reconnect_ex:
                            print(f"Reconnect attempt {attempt+1} failed: {reconnect_ex}")
                    else:
                        print(f"Reconnect attempt {attempt+1}: Device not found.")
                else:
                    print("Failed to reconnect after multiple attempts. Exiting.")
                    sys.exit(1)
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(1)
    except IOError as ex:
        print(ex)
        print("Error accessing device. Please check connection and permissions.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            dev.close()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()