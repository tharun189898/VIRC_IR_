cmake_minimum_required(VERSION 3.23)
project(virc_usbhid)

set(CMAKE_CXX_STANDARD 14)

add_executable(virc_usbhid main.cpp)
target_include_directories(virc_usbhid PUBLIC "/home/hitheshr/git/hidapi/build/install/include")
target_link_libraries(virc_usbhid PUBLIC
        -L/home/hitheshr/git/hidapi/build/install/lib/
        hidapi-hidraw)

# hidapi library build instructions
# https://github.com/libusb/hidapi/blob/4e63d6dfc33132679605cf9f5a569e21cc2d44ee/BUILD.cmake.md#standalone-package-build


