import tkinter as tk
from tkinter import ttk, messagebox
import threading
import hid
import time
from datetime import datetime

# Constants from main.py
USB_VID = 0x239a

class VIRCCompleteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VIRC IR Controller - Complete GUI")
        self.root.geometry("900x700")
        self.device = None
        self.is_listening = False
        self.listen_thread = None
        
        # IR code mappings from main.py
        self.code_map = {
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
        
        self.white_remote_codes = {
            0xFE017F80, 0xFC037F80, 0xFB047F80, 0xF9067F80, 0xF8077F80, 0xF6097F80
        }
        self.black_remote_codes = {
            0xFE01FF00, 0xFC03FF00, 0xFB04FF00, 0xF906FF00, 0xF807FF00, 0xF609FF00
        }
        
        self.create_widgets()
        self.refresh_devices()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="VIRC IR Controller - Complete GUI", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 10))
        
        # Device frame
        device_frame = ttk.LabelFrame(main_frame, text="Device Management", padding="5")
        device_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Device selection
        device_select_frame = ttk.Frame(device_frame)
        device_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(device_select_frame, text="Available Devices:").pack(side=tk.LEFT, padx=5)
        self.device_combo = ttk.Combobox(device_select_frame, state="readonly", width=50)
        self.device_combo.pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(device_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh Devices", command=self.refresh_devices)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.connect_btn = ttk.Button(button_frame, text="Connect", command=self.connect_device)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        self.get_info_btn = ttk.Button(button_frame, text="Get Device Info", command=self.get_device_info, state=tk.DISABLED)
        self.get_info_btn.pack(side=tk.LEFT, padx=5)
        
        # Device info frame
        info_frame = ttk.LabelFrame(main_frame, text="Device Information", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.device_info = {
            'manufacturer': tk.StringVar(value="N/A"),
            'product': tk.StringVar(value="N/A"),
            'serial': tk.StringVar(value="N/A"),
            'device_type': tk.StringVar(value="N/A"),
            'api_version': tk.StringVar(value="N/A"),
            'fw_version': tk.StringVar(value="N/A")
        }
        
        info_items = [
            ("Manufacturer:", self.device_info['manufacturer']),
            ("Product:", self.device_info['product']),
            ("Serial:", self.device_info['serial']),
            ("Device Type:", self.device_info['device_type']),
            ("API Version:", self.device_info['api_version']),
            ("Firmware Version:", self.device_info['fw_version'])
        ]
        
        for i, (label, var) in enumerate(info_items):
            frame = ttk.Frame(info_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
            ttk.Label(frame, textvariable=var, width=30).pack(side=tk.LEFT)
        
        # IR Monitor frame
        monitor_frame = ttk.LabelFrame(main_frame, text="IR Signal Monitor", padding="5")
        monitor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons
        control_frame = ttk.Frame(monitor_frame)
        control_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.start_btn = ttk.Button(control_frame, text="Start Listening", command=self.start_listening, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(control_frame, text="Clear Log", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # IR log
        self.ir_text = tk.Text(monitor_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(monitor_frame, orient="vertical", command=self.ir_text.yview)
        self.ir_text.configure(yscrollcommand=scrollbar.set)
        
        self.ir_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(5, 0))
        
    def refresh_devices(self):
        """List all devices like main.py"""
        devices = hid.enumerate(USB_VID)
        device_list = []
        for device in devices:
            name = f"{device.get('manufacturer_string', 'Unknown')} - {device.get('product_string', 'Unknown')} (PID: 0x{device['product_id']:04x})"
            device_list.append(name)
        
        self.device_combo['values'] = device_list
        if device_list:
            self.device_combo.current(0)
            self.status_var.set(f"Found {len(device_list)} device(s)")
        else:
            self.device_combo.set('')
            self.status_var.set("No devices found")
        
        # Also log all devices like main.py
        self.log_message("All HID devices:")
        for device in hid.enumerate():
            self.log_message(f"VID: 0x{device['vendor_id']:04x}, PID: 0x{device['product_id']:04x}, Manufacturer: {device.get('manufacturer_string', 'N/A')}")
        self.log_message("")
        
    def connect_device(self):
        """Connect to device like main.py"""
        selected_index = self.device_combo.current()
        if selected_index == -1:
            messagebox.showwarning("Warning", "No device selected")
            return
            
        devices = list(hid.enumerate(USB_VID))
        if not devices:
            messagebox.showerror("Error", "No devices found")
            return
            
        try:
            self.device = hid.device()
            self.device.open(USB_VID, devices[selected_index]['product_id'])
            self.log_message("Successfully opened device")
            self.log_message(f"Manufacturer: {devices[selected_index]['manufacturer_string']}")
            self.log_message(f"Product: {devices[selected_index]['product_string']}")
            
            # Update UI
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.get_info_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
            
            self.device_info['manufacturer'].set(devices[selected_index]['manufacturer_string'] or 'Unknown')
            self.device_info['product'].set(devices[selected_index]['product_string'] or 'Unknown')
            self.device_info['serial'].set(devices[selected_index]['serial_number'] or 'N/A')
            
            self.status_var.set("Connected")
            
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.status_var.set("Connection failed")
        
    def disconnect_device(self):
        """Disconnect from device"""
        if self.device:
            self.stop_listening()
            self.device.close()
            self.device = None
            
            # Update UI
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.get_info_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            
            # Reset device info
            for var in self.device_info.values():
                var.set("N/A")
                
            self.status_var.set("Disconnected")
            self.log_message("Disconnected from device")
        
    def get_device_info(self):
        """Get device info like main.py"""
        if not self.device:
            return
            
        commands = [
            (b'\x00\x01', "Device Type"),
            (b'\x00\x03', "API Version"),
            (b'\x00\x05', "Firmware Version")
        ]
        
        for cmd, desc in commands:
            try:
                self.log_message(f"Getting {desc}...")
                self.device.write(cmd)
                response = self.device.read(64, 1000)
                self.log_message(f"{desc} response: {list(response)}")
                
                if desc == "Device Type" and len(response) >= 3:
                    self.device_info['device_type'].set(str(response[2]))
                elif desc == "API Version" and len(response) >= 4:
                    self.device_info['api_version'].set(f"{response[2]}.{response[3]}")
                elif desc == "Firmware Version" and len(response) >= 4:
                    self.device_info['fw_version'].set(f"{response[2]}.{response[3]}")
                    
            except Exception as e:
                self.log_message(f"Error getting {desc}: {e}")
        
    def start_listening(self):
        """Start listening for IR signals like main.py"""
        if not self.device:
            messagebox.showwarning("Warning", "No device connected")
            return
            
        self.is_listening = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Listening for IR signals...")
        
        self.log_message("Waiting for IR signals... (Press Stop to exit)")
        self.log_message("Press any button on your remote to detect remote type...")
        
        self.listen_thread = threading.Thread(target=self.listen_for_ir, daemon=True)
        self.listen_thread.start()
        
    def stop_listening(self):
        """Stop listening for IR signals"""
        self.is_listening = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Stopped listening")
        self.log_message("Stopped listening for IR signals")
        
    def listen_for_ir(self):
        """Listen for IR signals like main.py"""
        while self.is_listening and self.device:
            try:
                response = self.device.read(64, 100)
                if response and response[0] == 7:
                    ir_code = 0
                    for i in range(4):
                        ir_code |= response[2+i] << (8*i)
                    
                    name = self.code_map.get(ir_code, "Unknown Button")
                    remote_type = self.detect_remote_type(ir_code)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    self.log_message(f"\n[{timestamp}] Received IR signal:")
                    self.log_message(f"Raw bytes: {[hex(x) for x in response[:6]]}")
                    self.log_message(f"IR Code: 0x{ir_code:08X} : {name}")
                    self.log_message(f"Detected remote type: {remote_type}")
                    self.log_message("-" * 50)
                    
            except Exception as e:
                self.log_message(f"HID error: {e}")
                self.log_message("Device may have been disconnected. Attempting to reconnect...")
                self.handle_reconnection()
                break
            except Exception as e:
                self.log_message(f"Unexpected error: {e}")
                time.sleep(1)
                
    def detect_remote_type(self, ir_code):
        """Detect remote type like main.py"""
        if ir_code in self.white_remote_codes:
            return "White Remote (Scanmode 1)"
        elif ir_code in self.black_remote_codes:
            return "Black Remote (Scanmode 2)"
        else:
            return "Unknown Remote"
            
    def handle_reconnection(self):
        """Handle reconnection like main.py"""
        if self.device:
            self.device.close()
            
        for attempt in range(10):
            time.sleep(1)
            devices = list(hid.enumerate(USB_VID))
            if devices:
                try:
                    self.device = hid.device()
                    self.device.open(USB_VID, devices[0]['product_id'])
                    self.log_message("Reconnected to device.")
                    return
                except Exception as reconnect_ex:
                    self.log_message(f"Reconnect attempt {attempt+1} failed: {reconnect_ex}")
            else:
                self.log_message(f"Reconnect attempt {attempt+1}: Device not found.")
        
        self.log_message("Failed to reconnect after multiple attempts.")
        self.stop_listening()
        
    def clear_log(self):
        """Clear the IR log"""
        self.ir_text.delete(1.0, tk.END)
        
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.ir_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.ir_text.see(tk.END)

def main():
    root = tk.Tk()
    app = VIRCCompleteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
