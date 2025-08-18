import tkinter as tk
from tkinter import ttk, messagebox
import threading
import hid
import time
from datetime import datetime
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Constants from main.py
USB_VID = 0x239a

class VIRCCompleteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VIRC IR Controller - QC Testing Station")
        self.root.geometry("1100x750")
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
        
        # Welcome message with styling demonstration
        self.log_message("🚀 VIRC QC Testing Station - Ready", "header")
        self.log_message("Enhanced with colorful logging and improved layout!", "instruction")
        
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
        

        
        self.disconnect_btn = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        self.get_info_btn = ttk.Button(button_frame, text="Get Device Info", command=self.get_device_info, state=tk.DISABLED)
        self.get_info_btn.pack(side=tk.LEFT, padx=5)
        
        # Create horizontal layout for Device Info and Remote Display
        info_remote_frame = ttk.Frame(main_frame)
        info_remote_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Device info frame (left side)
        info_frame = ttk.LabelFrame(info_remote_frame, text="Device Information", padding="5")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
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
            ttk.Label(frame, textvariable=var, width=25).pack(side=tk.LEFT)
        
        # Remote Display frame (right side)
        remote_frame = ttk.LabelFrame(info_remote_frame, text="Detected Remote", padding="5")
        remote_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create a frame to hold image and info side by side
        remote_content_frame = ttk.Frame(remote_frame)
        remote_content_frame.pack(fill=tk.X, expand=True)
        
        # Image display area
        self.image_frame = ttk.Frame(remote_content_frame)
        self.image_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        # Placeholder for remote image
        self.remote_image_label = ttk.Label(self.image_frame, text="No Remote\nDetected", 
                                          background="lightgray", width=15, anchor="center")
        self.remote_image_label.pack(pady=5)
        
        # Remote info area
        remote_info_frame = ttk.Frame(remote_content_frame)
        remote_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.remote_type_var = tk.StringVar(value="Unknown")
        self.last_button_var = tk.StringVar(value="None")
        self.signal_count_var = tk.StringVar(value="0")
        
        ttk.Label(remote_info_frame, text="Remote Type:").pack(anchor="w")
        ttk.Label(remote_info_frame, textvariable=self.remote_type_var, 
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=(10, 0))
        
        ttk.Label(remote_info_frame, text="Last Button:").pack(anchor="w", pady=(5, 0))
        ttk.Label(remote_info_frame, textvariable=self.last_button_var, 
                 font=("Arial", 9)).pack(anchor="w", padx=(10, 0))
        
        ttk.Label(remote_info_frame, text="Signals Received:").pack(anchor="w", pady=(5, 0))
        ttk.Label(remote_info_frame, textvariable=self.signal_count_var, 
                 font=("Arial", 9)).pack(anchor="w", padx=(10, 0))
        
        # Initialize signal counter
        self.signal_count = 0
        
        # IR Monitor frame
        monitor_frame = ttk.LabelFrame(main_frame, text="IR Signal Monitor", padding="5")
        monitor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Enhanced Control Panel with centered layout
        control_panel = ttk.Frame(monitor_frame)
        control_panel.pack(fill=tk.X, pady=(0, 15))
        
        # Center container for both control panels
        center_container = ttk.Frame(control_panel)
        center_container.pack(expand=True)
        
        # IR Monitoring Controls (Left Section) - Larger size
        monitor_controls = ttk.LabelFrame(center_container, text="📡 IR Monitoring", 
                                        padding="15", style="Accent.TLabelframe")
        monitor_controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Start/Stop in same row with larger buttons
        listen_frame = ttk.Frame(monitor_controls)
        listen_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(listen_frame, text="🎧 Start Listening", 
                                   command=self.start_listening, state=tk.DISABLED, 
                                   width=18, style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.stop_btn = ttk.Button(listen_frame, text="⏹️ Stop Listening", 
                                  command=self.stop_listening, state=tk.DISABLED, 
                                  width=18, style="Accent.TButton")
        self.stop_btn.pack(side=tk.LEFT)
        
        # Clear log button below - larger
        self.clear_btn = ttk.Button(monitor_controls, text="🗑️ Clear Log", 
                                   command=self.clear_log, width=38)
        self.clear_btn.pack(pady=(8, 0))
        
        # QC Testing Controls (Right Section) - Larger size
        test_controls = ttk.LabelFrame(center_container, text="🧪 Quality Control Testing", 
                                     padding="15", style="Accent.TLabelframe")
        test_controls.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        # Test buttons in rows with larger buttons
        test_frame1 = ttk.Frame(test_controls)
        test_frame1.pack(fill=tk.X, pady=5)
        
        self.test_mode_btn = ttk.Button(test_frame1, text="🚀 Start QC Test", 
                                       command=self.start_test_mode, width=18)
        self.test_mode_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.reset_test_btn = ttk.Button(test_frame1, text="🔄 Reset Test", 
                                        command=self.reset_test_mode, state=tk.DISABLED, width=18)
        self.reset_test_btn.pack(side=tk.LEFT)
        
        # Export results button - larger
        self.export_btn = ttk.Button(test_controls, text="📊 Export Results", 
                                    command=self.export_test_results, state=tk.DISABLED, width=38)
        self.export_btn.pack(pady=(8, 0))
        
        # Test Progress frame
        self.test_frame = ttk.LabelFrame(monitor_frame, text="Remote QC Test Progress", padding="5")
        # Initially hidden, will be shown when test mode starts
        
        # Initialize test mode variables
        self.test_mode_active = False
        self.current_remote_type = None
        self.test_results = {}
        self.expected_buttons = {}
        self.setup_test_definitions()
        
        # Enhanced IR log with styling
        log_frame = ttk.Frame(monitor_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ir_text = tk.Text(log_frame, height=20, width=100, 
                              bg="#1e1e1e", fg="#ffffff", 
                              font=("Consolas", 10), 
                              wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.ir_text.yview)
        self.ir_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure text tags for fancy formatting
        self.setup_text_styles()
        
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
            # Auto-connect to the first VIRC device found
            self.auto_connect()
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
    
    def auto_connect(self):
        """Automatically connect to the first VIRC device found"""
        if self.device:  # Already connected
            return
            
        selected_index = self.device_combo.current()
        if selected_index == -1:
            return
            
        devices = list(hid.enumerate(USB_VID))
        if not devices:
            return
            
        try:
            self.device = hid.device()
            self.device.open(USB_VID, devices[selected_index]['product_id'])
            self.log_message("✓ Automatically connected to VIRC device", "success")
            self.log_message(f"Manufacturer: {devices[selected_index]['manufacturer_string']}")
            self.log_message(f"Product: {devices[selected_index]['product_string']}")
            
            # Update UI - remove connect_btn reference, keep start_btn enabled
            self.disconnect_btn.config(state=tk.NORMAL)
            self.get_info_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
            
            # Update device info
            self.device_info['manufacturer'].set(devices[selected_index]['manufacturer_string'] or 'Unknown')
            self.device_info['product'].set(devices[selected_index]['product_string'] or 'Unknown')
            self.device_info['serial'].set(devices[selected_index]['serial_number'] or 'N/A')
            
            self.status_var.set("Auto-connected")
            
            # Automatically get device info
            self.get_device_info()
            
        except Exception as e:
            self.log_message(f"Auto-connection failed: {e}")
            self.status_var.set("Auto-connection failed")
        
    def disconnect_device(self):
        """Disconnect from device"""
        if self.device:
            self.stop_listening()
            self.device.close()
            self.device = None
            
            # Update UI
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
        
        self.log_message("Waiting for IR signals... (Press Stop to exit)", "instruction")
        self.log_message("Press any button on your remote to detect remote type...", "instruction")
        
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
                    
                    # Update remote display
                    self.update_remote_display(remote_type, name)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    self.log_message(f"\n[{timestamp}] Received IR signal:", "ir_signal")
                    self.log_message(f"Raw bytes: {[hex(x) for x in response[:6]]}")
                    self.log_message(f"IR Code: 0x{ir_code:08X} : {name}", "ir_signal")
                    self.log_message(f"Detected remote type: {remote_type}", "test")
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
        
    def setup_text_styles(self):
        """Setup fancy text styles for different message types"""
        # Header styles
        self.ir_text.tag_configure("header", foreground="#00ff00", font=("Consolas", 12, "bold"), 
                                  background="#2d2d2d", relief="raised", borderwidth=1)
        
        # Success messages
        self.ir_text.tag_configure("success", foreground="#00ff88", font=("Consolas", 10, "bold"))
        
        # Error messages
        self.ir_text.tag_configure("error", foreground="#ff4444", font=("Consolas", 10, "bold"))
        
        # Warning messages
        self.ir_text.tag_configure("warning", foreground="#ffaa00", font=("Consolas", 10, "bold"))
        
        # Test mode messages
        self.ir_text.tag_configure("test", foreground="#88aaff", font=("Consolas", 10, "bold"),
                                  background="#1a1a2e")
        
        # IR signal messages
        self.ir_text.tag_configure("ir_signal", foreground="#ff88ff", font=("Consolas", 10, "bold"))
        
        # Instructions
        self.ir_text.tag_configure("instruction", foreground="#ffff88", font=("Consolas", 10))
        
        # Timestamp
        self.ir_text.tag_configure("timestamp", foreground="#888888", font=("Consolas", 9))
        
        # Separator lines
        self.ir_text.tag_configure("separator", foreground="#444444", font=("Consolas", 10))
    
    def log_message(self, message, style="normal"):
        """Add a fancy formatted message to the IR log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Insert timestamp with special formatting
        self.ir_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Determine style based on message content if not specified
        if style == "normal":
            if "🧪 QC TEST MODE" in message or "🏁 QC TEST RESULTS" in message:
                style = "header"
            elif "✅" in message or "PASS" in message:
                style = "success"
            elif "❌" in message or "FAIL" in message:
                style = "error"
            elif "❓" in message or "WARNING" in message:
                style = "warning"
            elif "🎯" in message or "📝" in message or "📊" in message:
                style = "test"
            elif "Received IR signal" in message or "IR Code:" in message:
                style = "ir_signal"
            elif "Instructions:" in message or message.startswith(("1.", "2.", "3.", "4.")):
                style = "instruction"
            elif message.startswith("-" * 10) or message.startswith("=" * 10):
                style = "separator"
        
        # Insert message with appropriate style
        self.ir_text.insert(tk.END, f"{message}\n", style)
        self.ir_text.see(tk.END)
    
    def load_remote_image(self, image_path, size=(100, 160)):
        """Load and resize remote image"""
        if not PIL_AVAILABLE:
            return None
        try:
            image = Image.open(image_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            self.log_message(f"Error loading image {image_path}: {e}")
            return None
    
    def update_remote_display(self, remote_type, button_name):
        """Update the remote display with current remote type and button"""
        # Update remote type
        self.remote_type_var.set(remote_type)
        
        # Update last button
        self.last_button_var.set(button_name)
        
        # Update signal count
        self.signal_count += 1
        self.signal_count_var.set(str(self.signal_count))
        
        # Update remote image based on type
        if "White Remote" in remote_type:
            self.show_white_remote_image()
        elif "Black Remote" in remote_type:
            self.show_black_remote_image()
        else:
            self.show_unknown_remote()
        
        # Test mode logic
        if self.test_mode_active:
            self.handle_test_button_press(remote_type, button_name)
    
    def show_white_remote_image(self):
        """Display white remote image"""
        if PIL_AVAILABLE:
            try:
                # Try to load white remote image
                white_image = self.load_remote_image("white_remote.png")
                if white_image:
                    self.remote_image_label.configure(image=white_image, text="")
                    self.remote_image_label.image = white_image  # Keep a reference
                    return
            except:
                pass
        
        # Fallback to text display
        self.remote_image_label.configure(image="", text="White Remote\n📱", 
                                        font=("Arial", 12), background="white")
    
    def show_black_remote_image(self):
        """Display black remote image"""
        if PIL_AVAILABLE:
            try:
                # Try to load actual black remote image (JPEG)
                black_image = self.load_remote_image("black_remote.jpeg")
                if black_image:
                    self.remote_image_label.configure(image=black_image, text="")
                    self.remote_image_label.image = black_image  # Keep a reference
                    return
                # Fallback to PNG version
                black_image = self.load_remote_image("black_remote.png")
                if black_image:
                    self.remote_image_label.configure(image=black_image, text="")
                    self.remote_image_label.image = black_image  # Keep a reference
                    return
            except:
                pass
        
        # Fallback to text display
        self.remote_image_label.configure(image="", text="Black Remote\n📱", 
                                        font=("Arial", 12), background="black", foreground="white")
    
    def show_unknown_remote(self):
        """Display unknown remote placeholder"""
        self.remote_image_label.configure(image="", text="Unknown Remote\n❓", 
                                        font=("Arial", 12), background="lightgray")
    
    def setup_test_definitions(self):
        """Define expected buttons for each remote type"""
        self.expected_buttons = {
            "White Remote (Scanmode 1)": {
                0xFE017F80: "Short Pause",
                0xFC037F80: "Long Pause", 
                0xFB047F80: "Bed Mode",
                0xF9067F80: "Chair Mode",
                0xF8077F80: "Square Button",
                0xF6097F80: "Triangle Button"
            },
            "Black Remote (Scanmode 2)": {
                0xFE01FF00: "Short Pause",
                0xFC03FF00: "Long Pause",
                0xFB04FF00: "Bed Mode", 
                0xF906FF00: "Chair Mode",
                0xF807FF00: "Square Button",
                0xF609FF00: "Triangle Button"
            }
        }
    
    def start_test_mode(self):
        """Start the QC test mode"""
        if not self.device:
            messagebox.showwarning("Warning", "Please connect a device first")
            return
            
        self.test_mode_active = True
        self.current_remote_type = None
        self.test_results = {}
                
        # Enable/disable appropriate buttons
        self.test_mode_btn.config(state=tk.DISABLED)
        self.reset_test_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.DISABLED)
        
        # Show test frame
        self.test_frame.pack(fill=tk.X, pady=(10, 0))
        self.setup_test_ui()
        
        # Start listening automatically
        if not self.is_listening:
            self.start_listening()
        
        self.log_message("🧪 QC TEST MODE STARTED", "header")
        self.log_message("📋 Instructions:", "instruction")
        self.log_message("1. Point remote at VIRC receiver", "instruction")
        self.log_message("2. Press each button listed in the test checklist", "instruction")
        self.log_message("3. Watch for ✅ (PASS) or ❌ (FAIL) indicators", "instruction")
        self.log_message("4. Test will auto-detect remote type on first button press", "instruction")
        self.log_message("-" * 60, "separator")
    
    def setup_test_ui(self):
        """Create the test progress UI"""
        # Clear any existing content
        for widget in self.test_frame.winfo_children():
            widget.destroy()
        
        # Instructions label
        instructions = ttk.Label(self.test_frame, text="🎯 Press each button on your remote to test. Test will auto-detect remote type.", 
                               font=("Arial", 10, "bold"))
        instructions.pack(pady=(0, 10))
        
        # Create frame for test progress
        self.progress_frame = ttk.Frame(self.test_frame)
        self.progress_frame.pack(fill=tk.X)
        
        # Test status labels will be created when remote type is detected
        self.button_status_labels = {}
        
        # Overall progress
        self.progress_label = ttk.Label(self.test_frame, text="🟡 Waiting for first button press to detect remote type...", 
                                      font=("Arial", 10))
        self.progress_label.pack(pady=(10, 0))
    
    def create_button_checklist(self, remote_type):
        """Create checklist for detected remote type"""
        # Clear existing checklist
        for widget in self.progress_frame.winfo_children():
            widget.destroy()
        
        self.button_status_labels = {}
        expected_buttons = self.expected_buttons.get(remote_type, {})
        
        # Create two columns
        left_frame = ttk.Frame(self.progress_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(self.progress_frame) 
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Split buttons into two columns
        button_list = list(expected_buttons.items())
        mid_point = len(button_list) // 2
        
        for i, (code, name) in enumerate(button_list):
            target_frame = left_frame if i < mid_point else right_frame
            
            frame = ttk.Frame(target_frame)
            frame.pack(fill=tk.X, pady=2)
            
            status_label = ttk.Label(frame, text="⏳", font=("Arial", 12))
            status_label.pack(side=tk.LEFT, padx=(0, 5))
            
            name_label = ttk.Label(frame, text=name, font=("Arial", 10))
            name_label.pack(side=tk.LEFT)
            
            self.button_status_labels[code] = status_label
            self.test_results[code] = "pending"
    

    
    def handle_test_button_press(self, remote_type, button_name):
        """Handle button press in test mode"""
        # Set up test UI for this remote type if not already done
        if self.current_remote_type != remote_type:
            self.current_remote_type = remote_type
            self.create_button_checklist(remote_type)
            self.log_message(f"🎯 Detected: {remote_type}", "test")
            self.log_message(f"📝 Testing {len(self.expected_buttons.get(remote_type, {}))} buttons...", "test")
        
        # Find the button code that was pressed
        expected_buttons = self.expected_buttons.get(remote_type, {})
        pressed_code = None
        
        for code, name in expected_buttons.items():
            if name == button_name:
                pressed_code = code
                break
        
        if pressed_code and pressed_code in self.button_status_labels:
            if self.test_results[pressed_code] == "pending":
                # Mark as passed
                self.test_results[pressed_code] = "pass"
                self.button_status_labels[pressed_code].config(text="✅", foreground="green")
                self.log_message(f"✅ PASS: {button_name}", "success")
                
                # Check if all tests are complete
                self.check_test_completion()
            else:
                # Already tested
                self.log_message(f"🔄 REPEAT: {button_name} (already tested)", "warning")
        else:
            # Unexpected button or remote type
            self.log_message(f"❓ UNEXPECTED: {button_name} - Not in expected test list", "warning")
    
    def check_test_completion(self):
        """Check if all buttons have been tested"""
        if not self.test_results:
            return
            
        pending_count = sum(1 for status in self.test_results.values() if status == "pending")
        total_count = len(self.test_results)
        passed_count = sum(1 for status in self.test_results.values() if status == "pass")
        
        progress_text = f"📊 Progress: {passed_count}/{total_count} buttons tested"
        
        if pending_count == 0:
            # All tests complete!
            progress_text += " - 🎉 ALL TESTS COMPLETE!"
            self.progress_label.config(text=progress_text, foreground="green")
            self.show_test_results()
        else:
            self.progress_label.config(text=progress_text, foreground="blue")
    
    def show_test_results(self):
        """Show final test results"""
        if not self.test_results:
            return
            
        total_tests = len(self.test_results)
        passed_tests = sum(1 for status in self.test_results.values() if status == "pass")
        
        self.log_message("=" * 60, "separator")
        self.log_message("🏁 QC TEST RESULTS", "header")
        self.log_message(f"Remote Type: {self.current_remote_type}", "test")
        self.log_message(f"Tests Passed: {passed_tests}/{total_tests}", "test")
        
        if passed_tests == total_tests:
            self.log_message("✅ RESULT: PASS - All buttons working correctly", "success")
            result_msg = f"QC Test PASSED!\n\nRemote: {self.current_remote_type}\nAll {total_tests} buttons working correctly."
            messagebox.showinfo("QC Test Complete", result_msg)
        else:
            failed_buttons = [name for code, name in self.expected_buttons.get(self.current_remote_type, {}).items() 
                            if self.test_results.get(code) != "pass"]
            self.log_message("❌ RESULT: FAIL - Some buttons not working", "error")
            self.log_message(f"Failed buttons: {', '.join(failed_buttons)}", "error")
            result_msg = f"QC Test FAILED!\n\nRemote: {self.current_remote_type}\nFailed: {', '.join(failed_buttons)}"
            messagebox.showerror("QC Test Failed", result_msg)
        
        self.log_message("=" * 60, "separator")
        
        # Enable export button after test completion
        self.export_btn.config(state=tk.NORMAL)
    
    def reset_test_mode(self):
        """Reset the test mode for testing another remote"""
        self.test_mode_active = False
        self.current_remote_type = None
        self.test_results = {}
        self.signal_count = 0
        self.signal_count_var.set("0")
        
        # Reset UI
        self.test_mode_btn.config(state=tk.NORMAL)
        self.reset_test_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.test_frame.pack_forget()
        
        # Clear log
        self.clear_log()
        
        self.log_message("🔄 Test mode reset - Ready for next remote")
    
    def export_test_results(self):
        """Export test results to a file"""
        if not self.test_results or not self.current_remote_type:
            messagebox.showwarning("Warning", "No test results to export")
            return
        
        from datetime import datetime
        import os
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"QC_Test_Results_{timestamp}.txt"
        
        try:
            total_tests = len(self.test_results)
            passed_tests = sum(1 for status in self.test_results.values() if status == "pass")
            failed_tests = total_tests - passed_tests
            
            # Generate report content
            report_content = f"""
VIRC REMOTE QUALITY CONTROL TEST REPORT
{'=' * 50}

Test Date/Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Remote Type: {self.current_remote_type}
Test Status: {"PASSED" if failed_tests == 0 else "FAILED"}

SUMMARY:
--------
Total Buttons Tested: {total_tests}
Buttons Passed: {passed_tests}
Buttons Failed: {failed_tests}
Success Rate: {(passed_tests/total_tests*100):.1f}%

DETAILED RESULTS:
-----------------
"""
            
            # Add detailed button results
            expected_buttons = self.expected_buttons.get(self.current_remote_type, {})
            for code, name in expected_buttons.items():
                status = self.test_results.get(code, "not_tested")
                status_symbol = "✅ PASS" if status == "pass" else "❌ FAIL" if status == "fail" else "⏳ NOT TESTED"
                report_content += f"{name:20} : {status_symbol}\n"
            
            report_content += f"""
{'=' * 50}
Generated by VIRC QC Testing Station
"""
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # Show success message
            success_msg = f"Test results exported successfully!\n\nFile: {filename}\nLocation: {os.path.abspath(filename)}"
            messagebox.showinfo("Export Complete", success_msg)
            self.log_message(f"📁 Results exported to: {filename}")
            
        except Exception as e:
            error_msg = f"Failed to export test results:\n{str(e)}"
            messagebox.showerror("Export Error", error_msg)
            self.log_message(f"❌ Export failed: {str(e)}")

def main():
    root = tk.Tk()
    app = VIRCCompleteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
