import serial
#import logging
import time
import datetime

    
    
#FILENAME = '/home/pi/Desktop/TestData/' + str(datetime.datetime.now()) + '.log'
#logging.basicConfig(filename=FILENAME,
#                    level=logging.DEBUG,
#                    format='%(asctime)s %(message)s',
#                    datefmt='%m-%d %H:%M:%S',
#                    filemode='a')
                    
    #master to arduino conn.
                    
#ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)
#print(ser.name)

with serial.Serial('/dev/ttyACM0', timeout=1) as ser:
    ser.baudrate = 115200
    

ser.open()
time.sleep(2)

ser.write(b'$X\n')
time.sleep(2)


ser.write(b'M7\n')
    
#ser.write('$hx'.encode())
#time.sleep(1/1000)

ser.write(b'X30\n')
time.sleep(1/1000)

#ser.write('$hy')
#line = ser.readline().decode('utf-8').rstrip() 
#print(line)

time.sleep(5)
ser.write(b'M9\n')

ser.close()

    

    
