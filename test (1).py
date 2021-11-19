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

ser.write(b'$X\n')
time.sleep(2)


ser.write(b'M7\n')
time.sleep(2)


ser1.open()
time.sleep(1)

ser.write(b'$HZ\n')
time.sleep(10)
ser1.write(b'a\n')
time.sleep(2)
#ser1.write(b'b\n')
time.sleep(0.01)

#for i in range(10):
	   
ser.write(b'Z-1\n')
ser.write(b'Z0\n')
#ser.write(b'Y20\n')
ser1.write(b'b\n')
time.sleep(5)

ser1.write(b'c\n')

for i in range(0,30000):
    
    #print(ser1.readline())
    logging.info(ser1.readline())
    #arr = ser1.readline()
    #print(ser1.readline())
    time.sleep(1/1000)

#reverse motion data collection

#time.sleep(10)

#ser.write(b'Z-0\n')
#ser1.write(b'b\n')
#time.sleep(10)

#ser1.write(b'c\n')

#for i in range(0,10000):
    
    #print(ser1.readline())
 #   logging.info(ser1.readline())
  #  arr = ser1.readline()
 #   print(ser1.readline())
#    time.sleep(1/1000)
    
ser.write(b'M9\n')

ser.close()
ser1.close()
    

    
