import sys
import serial
import os
import datetime
import time



if len(sys.argv) < 2:
	print("Specify COM port")
	exit(1)


ser = serial.Serial(sys.argv[1], 115200)

def readPres(nodeid, sensorid, sensorVal,):
	minPres = 0
	maxPres = 50
	minVal = (1/5)*1024
	maxVal = 1024
	x = (sensorVal-minVal)/(maxVal-minVal)
	
	pres = x*(maxPres-minPres) + minPres
	
	prettyPressure = '{0:.3f}'.format(pres)
	print(f'Pressure {nodeid}:{sensorid}\t{prettyPressure} PSIG')

while(1):
	if not ser.in_waiting:
		continue
		
	line = ser.readline(50).decode('utf-8').strip()
		
	timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
	
	fields = line.split(',')
	
	if len(fields) < 5:
		continue
	
	tag = fields[0]
	nodeid = int(fields[1])
	sensorid = int(fields[2])
	sensortype = int(fields[3])
	sensorval = int(fields[4])
	
	
	if nodeid==1 and sensorid in [6, 7, 8]:
		readPres(nodeid, sensorid, sensorval)
