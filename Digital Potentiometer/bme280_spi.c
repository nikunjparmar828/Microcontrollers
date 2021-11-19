#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"


#define CS   17
#define SCLK 14
#define MOSI 12

#define SPI_PORT spi0

void send_val(){
    // uint8_t buffer[6], reg;

    // reg = 0x88 | 0x80;
    gpio_put(CS, 0);
    spi_write_blocking(SPI_PORT, 1);
    gpio_put(CS, 1);

    gpio_put(CS, 0);
    spi_write_blocking(SPI_PORT, 1);
    gpio_put(CS, 1);

}

int main(){
    stdio_init_all(); // Initialise I/O for USB Serial

    spi_init(SPI_PORT, 500000); // Initialise spi0 at 500kHz
    
    //Initialise GPIO pins for SPI communication
    gpio_set_function(SCLK, GPIO_FUNC_SPI);
    gpio_set_function(MOSI, GPIO_FUNC_SPI);

    // Configure Chip Select
    gpio_init(CS); // Initialise CS Pin
    gpio_set_dir(CS, GPIO_OUT); // Set CS as output
    gpio_put(CS, 1); // Set CS High to indicate no currect SPI communication

    send_val(); // Read factory calibration/compensation values

}