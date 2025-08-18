#include <iostream>
#include <hidapi/hidapi.h>
#include <cstdio>
#include <cstring>
#include <cstdlib>

#define MAX_STR 255;

void print_device(struct hid_device_info *cur_dev) {
    printf("Device Found\n  type: %04hx %04hx\n  path: %s\n  serial_number: %ls", cur_dev->vendor_id, cur_dev->product_id, cur_dev->path, cur_dev->serial_number);
    printf("\n");
    printf("  Manufacturer: %ls\n", cur_dev->manufacturer_string);
    printf("  Product:      %ls\n", cur_dev->product_string);
    printf("  Release:      %hx\n", cur_dev->release_number);
    printf("  Interface:    %d\n",  cur_dev->interface_number);
    printf("  Usage (page): 0x%hx (0x%hx)\n", cur_dev->usage, cur_dev->usage_page);
    printf("\n");
}

void print_devices(struct hid_device_info *cur_dev) {
    while (cur_dev) {
        print_device(cur_dev);
        cur_dev = cur_dev->next;
    }
}

void print_buf(uint8_t buf[], int len){
    printf("Data read:\n   ");
    // Print out the returned buffer.
    for (int i = 0; i < len; i++) {
        printf("0x%x ", buf[i]);
    }
    printf("\n");
}

int main() {
    hid_device *handle;
    struct hid_device_info *devs;
    if(hid_init()!=0){
        std::cout << "Error initializing hid" << std::endl;
        return -1;
    }
    // Raspberry PICO VID = 0x2e8a
    devs = hid_enumerate(0x2e8a, 0x0);
    print_devices(devs);
    hid_free_enumeration(devs);
    handle = hid_open(0x2e8a, 0x000a, NULL);

    if (!handle) {
        printf("unable to open device\n");
        return 1;
    }
    int res;
    uint8_t buf[65] = {0};

    memset(buf, 0, sizeof(buf));
    buf[0] = 0x00; // not part of 64 byte report, dummy reportID needed by hidapi
    // get device type
    buf[1] = 01;
    res = hid_write(handle, buf, 2); // length should include first-byte report id
    if(res<0){
        printf("Unable to write(): %ls\n", hid_error(handle));
    }
    memset(buf, 0, sizeof(buf));
    // blocking read (by default)
    res = hid_read(handle, buf, 64); // for reading res will have number of bytes read. <= 64
//    if (res < 0) {
//        printf("Unable to read(): %ls\n", hid_error(handle));
//    }
    if (res > 0) {
        print_buf(buf, res);
    }

    memset(buf, 0, sizeof(buf));

    // listen to IR code
    while(true) {
        res = hid_read(handle, buf, 64);
        if (res > 0) {
            print_buf(buf, res);
        }
    }

    return 0;
}
