import sys
import serial
import os
import datetime
import time



if len(sys.argv) < 2:
    print("Specify COM port")
    exit(1)
    
    
ser = serial.Serial(sys.argv[1], 115200)


os.makedirs('data', exist_ok=True)



while(1):
    line = ser.readline(1000).decode('utf-8').strip()
    timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
    
    datafilename = f'{timestamp[:13]}.txt'
    
    dataline = f'{timestamp} {line}\n'
    with open(f'data/{datafilename}', 'a+') as file:
        file.write(dataline)
        file.close()
    sys.stdout.write(dataline)
    
    time.sleep(1)
