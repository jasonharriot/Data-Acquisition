import sys
import serial
import os
import datetime
import time

comport = sys.argv[1]
linetimeout = 1000	#If this is too short the whole line won't be read.
					#Espec

if len(sys.argv) < 2:
	print("Specify COM port")
	exit(1)


ser = None


os.makedirs('data', exist_ok=True)
header = ''


while 1:
	
		
	while 1:	#Read a line from serial or re-open the port.
		try:	#If the serial port is available
			if ser is None or not ser.isOpen():
				#print(f'Opening serial port {sys.argv[1]}')
				try:
					ser = serial.Serial(comport, 115200)
				
				except serial.serialutil.SerialException as sererr:
					print("Couldn't open serial port.")
					
					if ser is None:
						print("Serial port couldn't be opened on first run. Exiting.")
						exit(1)
				
			if not ser.in_waiting:
				time.sleep(.1)
				continue
				
			line = ser.readline(linetimeout).decode('utf-8').strip()
			break
			
		except serial.serialutil.SerialException as e:	#If the serial port is not available
			#print("Serial port error.")
			time.sleep(1)
			ser.close()
			
	outStr = ''
	timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
	datafilename = f'{timestamp[:13]}.csv'
	
	dataline = f'{timestamp},{line}\n'
	outStr += dataline
		
	writesuccess = False
	while not writesuccess:
		try:
			with open(f'data/{datafilename}', 'a+') as file:	#This may cause a high write frequency. Don't use on a computer with a mechanical HDD!
				file.write(outStr)
				file.close()
				writesuccess = True
		except:
			print('Could not open file for writing')
			
		time.sleep(.05)
		
		
	#Find the header so we can print it pretty
	if line.startswith('HEADER'):
		header = dataline.split(',')
	
	out = outStr.split(',')
	
	prettyprintstring = ''
	
	prettyprintstring += '\n'
	prettyprintstring += '\t'.join(header)
	prettyprintstring += '\t'.join(out)
	
	sys.stdout.write(prettyprintstring)
