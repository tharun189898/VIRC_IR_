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

// USB HID object
Adafruit_USBD_HID usb_hid(desc_hid_report, sizeof(desc_hid_report), HID_ITF_PROTOCOL_NONE, 2, true);

void setup() {
#if defined(ARDUINO_ARCH_MBED) && defined(ARDUINO_ARCH_RP2040)
  TinyUSB_Device_Init(0);
#endif
  usb_hid.setReportCallback(get_report_callback, set_report_callback);
  usb_hid.begin();

  // Serial port for debugging
  Serial.begin(115200);

  // wait until device mounted
  while( !TinyUSBDevice.mounted() ) delay(1);
  // Start the receiver and if not 3. parameter specified, take LED_BUILTIN pin from the internal boards definition as default feedback LED
  IrReceiver.begin(IR_RECEIVE_PIN, false);
  
  Serial.println("Finishing setup");


}

void loop() {
  /*
   * Check if received data is available and if yes, try to decode it.
   * Decoded result is in the IrReceiver.decodedIRData structure.
   *
   * E.g. command is in IrReceiver.decodedIRData.command
   * address is in command is in IrReceiver.decodedIRData.address
   * and up to 32 bit raw data in IrReceiver.decodedIRData.decodedRawData
   */
  if (IrReceiver.decode()) {
    uint32_t ir_raw = IrReceiver.decodedIRData.decodedRawData;

    // Always send the IR code, even if it's 0 (repeat code)
    uint8_t ir_buffer[64] = {0};
    ir_buffer[0] = 7;
    for (int i = 0; i < 4; i++) {
      ir_buffer[2 + i] = (uint8_t)((ir_raw >> (8 * i)) & 0xFF);
    }
    usb_hid.sendReport(0, ir_buffer, 6);
    Serial.println(ir_raw, HEX);

    IrReceiver.resume();
  }

}

// Invoked when received GET_REPORT control request
uint16_t get_report_callback (uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{
  // Fill buffer based on requested report
  switch (report_id) {
    case 0: // Only one report supported
      if (reqlen >= 3 && report_type == HID_REPORT_TYPE_INPUT) {
        // Example: return device type
        buffer[0] = 2; // Response ID for device type
        buffer[1] = 0; // Reserved
        buffer[2] = DEVICE_TYPE;
        return 3;
      }
      if (reqlen >= 4 && report_type == HID_REPORT_TYPE_INPUT) {
        // Example: return API version
        buffer[0] = 4; // Response ID for API version
        buffer[1] = 0; // Reserved
        buffer[2] = API_VERSION_MAJOR;
        buffer[3] = API_VERSION_MINOR;
        return 4;
      }
      if (reqlen >= 4 && report_type == HID_REPORT_TYPE_INPUT) {
        // Example: return FW version
        buffer[0] = 6; // Response ID for FW version
        buffer[1] = 0; // Reserved
        buffer[2] = FW_VERSION_MAJOR;
        buffer[3] = FW_VERSION_MINOR;
        return 4;
      }
      break;
    default:
      break;
  }
  return 0; // Return zero to stall if not handled
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
