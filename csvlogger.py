import sys
import serial
import os
import datetime
import time
import tkinter

comport = sys.argv[1]
linetimeout = 1000	#If this is too short the whole line won't be read.
					#Espec

if len(sys.argv) < 2:
	print("Specify COM port")
	exit(1)


ser = None


os.makedirs('data', exist_ok=True)
header = ''
lastdatafilename = ''

def readline():
	global ser, header, lsatdatafilename
	line = None
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
				
			try:
				line = ser.readline(linetimeout).decode('utf-8').strip()
			except UnicodeDecodeError:
				print(f'Unicode decode error.')
			break
			
		except serial.serialutil.SerialException as e:	#If the serial port is not available
			#print("Serial port error.")
			time.sleep(1)
			ser.close()
			
	return line


while 1:	#Main loop
	timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
	
	datafilename = f'{timestamp[:13]}.csv'
	
	
	if not datafilename == lastdatafilename:	#If the filename changed, write the header to it then continue.
		#if header is None or len(header) == 0:
			#print(f'Cannot write header to new file: header is None')
			
		print(f'New file! Writing header to {datafilename}: {header}')
		
		lastdatafilename = datafilename
		writesuccess = False	#Retry in case of file lock
		
		while not writesuccess:
			try:
				with open(f'data/{datafilename}', 'a+') as file:	#This may cause a high write frequency. Don't use on a computer with a mechanical HDD!
					file.write(header)
					file.close()
					writesuccess = True
			except:
				print(f'Could not open file for writing header: {datafilename}')
				time.sleep(.05)
				
	line = readline()	#Get a line or None from serial port
	
	
	dataline = f'{timestamp},{line}\n'
		
	writesuccess = False
	while not writesuccess:
		try:
			with open(f'data/{datafilename}', 'a+') as file:	#This may cause a high write frequency. Don't use on a computer with a mechanical HDD!
				file.write(dataline)
				file.close()
				writesuccess = True
		except:
			print('Could not open file for writing')
			time.sleep(.05)
		
		
	#Find the header so we can print it pretty
	if line.startswith('HEADER'):
		header = dataline
	
	prettyprintstring = ''
	
	prettyprintstring += '\n'
	prettyprintstring += '\t'.join(header.split(','))
	prettyprintstring += '\t'.join(dataline.split(','))
	
	#sys.stdout.write(prettyprintstring)
