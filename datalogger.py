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
	lines = []
	while(ser.in_waiting):
		lines.append(ser.readline(50).decode('utf-8').strip())
		
	outStr = ''
	timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
	datafilename = f'{timestamp[:13]}.txt'
	
	for line in lines:
		dataline = f'{timestamp} {line}\n'
		outStr += dataline
		
	with open(f'data/{datafilename}', 'a+') as file:
		file.write(outStr)
		file.close()
	sys.stdout.write(outStr)
