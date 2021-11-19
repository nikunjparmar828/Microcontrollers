time.sleep(2)
    
    #master to pico conn.
    
ser1=serial.Serial('/dev/ttyACM1', 115200, timeout=1)
ser1.flush()
    
    # a = offset value calculation
    # b = data aquisition
    # c = data dumping
try:
    ser1.write(b'a\n')
    time.sleep(1/1000)
        
    ser1.write(b'b\n')
    time.sleep(1/1000)
        
    data_array = ser1.write(b'c\n')
    time.sleep(1/1000)
        
    print(data_array)    
    #for i in data_array:
    #    logging.info(i + '\n')
    #    time.sleep(1/1000)
        
        #with open("dataencoder.txt", "w") as txt_file:
            #for line in data_array:
                #txt_file.write(line)
except IOError:
    print("port is used by another application")
    exit()
        
finally:
    ser1.close()
    
    
    