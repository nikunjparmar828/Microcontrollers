cmake_minimum_required(VERSION 3.12)
include(pico_sdk_import.cmake)
project(pico-spi)

pico_sdk_init()

add_executable(bmp280spi
    bmp280spi.c
)

target_link_libraries(bmp280spi
    pico_stdlib
    hardware_spi
)

pico_enable_stdio_usb(bmp280spi 1)
pico_enable_stdio_uart(bmp280spi 0)

pico_add_extra_outputs(bmp280spi)
