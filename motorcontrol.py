import serial
import time
import datetime

with serial.Serial('/dev/ttyACM0', timeout=1) as ser:
    ser.baudrate = 115200
    
ser.open()
time.sleep(2)

ser.write(b'$X\n')
time.sleep(2)

ser.write(b'M7\n')

ser.write(b'X30\n')
time.sleep(1/1000)

time.sleep(5)
ser.write(b'M9\n')

ser.close()

    

    
