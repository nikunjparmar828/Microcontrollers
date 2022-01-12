import serial
import time
import datetime
import logging
  
FILENAME = '/home/pi/Desktop/' + str(datetime.datetime.now()) + '.log'
logging.basicConfig(filename=FILENAME,
                    level=logging.DEBUG,
                    format='%(message)s',
                    datefmt='%m-%d %H:%M:%S',
                   filemode='a')
    
#%(asctime)s     
with serial.Serial('/dev/ttyACM0', timeout=1) as ser:
    ser.baudrate = 115200
    
with serial.Serial('/dev/ttyACM1', timeout=1) as ser1:
    ser1.baudrate = 115200    

ser.open()
time.sleep(2)

ser.write(b'$X\n') # Turn on the machine 
time.sleep(2)

ser.write(b'M7\n') # Initialization of the machine 
time.sleep(2)

ser1.open()
time.sleep(1)
ser.write(b'$HX\n') 
time.sleep(10)

ser1.write(b'a\n')
time.sleep(2)

ser1.write(b'b\n')
ser.write(b'X168\n')

ser1.write(b'c\n')

for i in range(0,20000):
    logging.info(ser1.readline())
    time.sleep(1/1000)
    
ser.write(b'M9\n')

ser.close()
ser1.close()
    

    
