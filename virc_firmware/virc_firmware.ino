/*
 * Arduino config
 * Tools > USB Stack > Adafruit tinyUSB
 * Tools > Board > RaspberryPi Pico 
*/

#include "Adafruit_TinyUSB.h" //https://github.com/adafruit/Adafruit_TinyUSB_Arduino/tree/1.14.3
#define DECODE_NEC  // Includes Apple and Onkyo
#include <Arduino.h> // Arduino 1.8.19
#include "PinDefinitionsAndMore.h" //Define macros for input and output pin etc.
#include <IRremote.hpp> //https://github.com/Arduino-IRremote/Arduino-IRremote/tree/v3.6.1

#define API_VERSION_MAJOR 1
#define API_VERSION_MINOR 0
#define FW_VERSION_MAJOR 1
#define FW_VERSION_MINOR 1
#define DEVICE_TYPE 1

// HID report descriptor using TinyUSB's template
// Generic In Out with 64 bytes report (max)
uint8_t const desc_hid_report[] =
{
  TUD_HID_REPORT_DESC_GENERIC_INOUT(64)
};

// Before the HID object declaration, add:
#define USB_VID 0x239a  // Adafruit VID
#define USB_PID 0xcafe  // Default PID

// USB HID object
Adafruit_USBD_HID usb_hid(desc_hid_report, sizeof(desc_hid_report), HID_ITF_PROTOCOL_NONE, 2, true);


void setup() {
#if defined(ARDUINO_ARCH_MBED) && defined(ARDUINO_ARCH_RP2040)
  // Manual begin() is required on core without built-in support for TinyUSB such as mbed rp2040
  TinyUSB_Device_Init(0);
#endif
  
  // Set USB device info
  TinyUSBDevice.setID(USB_VID, USB_PID);
  TinyUSBDevice.setManufacturerDescriptor("Raspberry Pi");
  TinyUSBDevice.setProductDescriptor("VIRC Controller");
  
  // Initialize HID
  usb_hid.setPollInterval(1);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  usb_hid.setReportCallback(get_report_callback, set_report_callback);
  usb_hid.begin();

  // Serial port for debugging
  Serial.begin(115200);
  Serial.println("Starting VIRC...");
  
  // wait until device mounted
  while( !TinyUSBDevice.mounted() ) delay(1);
  // Start the receiver and if not 3. parameter specified, take LED_BUILTIN pin from the internal boards definition as default feedback LED
  IrReceiver.begin(IR_RECEIVE_PIN, false);
  Serial.println("IR Receiver initialized");
}

void loop() {
  if (IrReceiver.decode()) {
    uint32_t ir_raw = IrReceiver.decodedIRData.decodedRawData;
    
    if(ir_raw != 0){
      Serial.print("IR Code Received: 0x");
      Serial.println(ir_raw, HEX);
      
      uint8_t ir_buffer[64] = {0}; 
      ir_buffer[0] = 7;  // Report ID
      // Store raw IR code in little-endian format
      for(int i = 0; i < 4; i++){
        ir_buffer[2+i] = (uint8_t)((ir_raw >> (8*i)) & 0xFF);
      }
      bool sent = usb_hid.sendReport(0, ir_buffer, 64);  // Send full buffer
      Serial.print("HID Report sent: ");
      Serial.println(sent);
    }
    
    IrReceiver.resume();
  }

}

// Invoked when received GET_REPORT control request
// Application must fill buffer report's content and return its length.
// Return zero will cause the stack to STALL request
uint16_t get_report_callback (uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{
  // not used
  (void) report_id;
  (void) report_type;
  (void) buffer;
  (void) reqlen;
  return 0;
}

// Invoked when received SET_REPORT control request or
// received data on OUT endpoint ( Report ID = 0, Type = 0 )
void set_report_callback(uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize)
{
  uint8_t out_buffer[64]={0}; 
  // check 1st byte for data_type
  switch (buffer[0]) {
    case 1: // Host asking for device type
      out_buffer[0] = 2;
      out_buffer[2] = DEVICE_TYPE;
      usb_hid.sendReport(0, out_buffer, 3);
      break;
    case 3: // Host asking for API version
      out_buffer[0] = 4;
      out_buffer[2] = API_VERSION_MAJOR;
      out_buffer[3] = API_VERSION_MINOR;
      usb_hid.sendReport(0, out_buffer, 4);
      break;
    case 5: //Host asking for firmware version
      out_buffer[0] = 6;
      out_buffer[2] = FW_VERSION_MAJOR;
      out_buffer[3] = FW_VERSION_MINOR;
      usb_hid.sendReport(0, out_buffer, 4);
      break;
    default:
      out_buffer[0] = 0;
      out_buffer[2] = 3;
      usb_hid.sendReport(0, out_buffer, 3); 
  }
}
    case 5: //Host asking for firmware version
      out_buffer[0] = 6;
      out_buffer[2] = FW_VERSION_MAJOR;
      out_buffer[3] = FW_VERSION_MINOR;
      usb_hid.sendReport(0, out_buffer, 4);
      break;
    default:
      out_buffer[0] = 0;
      out_buffer[2] = 3;
      usb_hid.sendReport(0, out_buffer, 3); 
  }
}
