import requests
import xml.etree.ElementTree as ET
import time
import base64
import csv
import datetime
import os

ipaddress = '192.168.2.153'
username = 'root'
password = '00000000'

datadirectory = 'esdata'

header = f'Time,V1,V2,V3,V4,V5,V6\n'	#CSV header

channeldict = {
	1:2,	#Maps ES cell (1-6) to ADAM ADC input
	2:3,
	3:4,
	4:5,
	5:6,
	6:7}

adcscale = 150/1000	#150 mv. Make sure this is set to match the range of the ADAM ADC (on ALL channels used in this script!)


url = f'http://{ipaddress}/analoginput/all/value'
#payload = {'username': f'{username}', 'password': f'{password}'}
user_agent = r'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
authstring = base64.b64encode(f'{username}:{password}'.encode('ascii')).decode('utf-8')
headers = {'Content-Type': 'application/x-www-form-urlencoded',
	'Authorization': f'Basic {authstring}'}
x = requests.get(url, headers=headers)

lastdatafilename = None

def init():
	if not x.status_code == 200:
		print(f'You may need to set the password. Couldn\'t get a response from {ipaddress}.')
		raise Exception(f'Bad response ({x.status_code})')
		
	try:
		os.makedirs(f'{datadirectory}')
	except FileExistsError:
		print(f'{datadirectory} already exists (OK)')
		
def getVoltages():	#Get voltages in volts
	x = None
	try:
		url = f'http://{ipaddress}/analoginput/all/value'
		x = requests.get(url, headers = headers)
		
	except Exception as e:
		print(f'Error making query')
		print(e)
		
	if x is None:
		None
		
	#print(f'Status {x.status_code} ({type(x.status_code)})')
		
	if x.status_code == 403:
		print(f'403 error. You may need to log in to {ipaddress}.\nUser: root\nPass: 00000000')
		exit(1)
		
	if x.status_code == 404:
		print(f'Bad response: {x.status_code}')
		return None

	tree = ET.fromstring(x.content)
	#print(tree)
	
	values = {}
	
	for child in tree:
		id = int(child.find('ID').text)
		hexvalue = child.find('VALUE').text
		minSymbol = 0
		maxSymbol = (pow(16, 4))-1
		value = adcscale*(int(hexvalue, 16) - int(maxSymbol/2))/int(maxSymbol/2)
		
		if not id is None and not value is None:
			values[id] = value
		
	return values
	



def loop():
	global lastdatafilename
	timestamp = datetime.datetime.now().isoformat()[:22].replace(':', '-').replace('.', '_')
	values = getVoltages()
	
	if values is None:
		print(f'Error getting values from DAQ. Check {ipaddress} in a browser.')
		exit()
	

	lineStr = f'{timestamp},'
	for cellID in channeldict.keys():
		channelID = channeldict[cellID]
		print(f'Cell {cellID}, channel {channelID}, voltage={values[channelID]}')
		lineStr += f'{values[channelID]:.8f},'
	
	datafilename = f'{timestamp[:13]}.csv'
	
	#Check if the current file is a different file than the last one (and needs a header)
	if not datafilename == lastdatafilename:	#If the filename changed, write the header to it then continue.
		#print(f'New file! Writing header to {datafilename}: {header}')
		
		lastdatafilename = datafilename
		writesuccess = False	#Retry in case of file lock
		
		while not writesuccess:
			try:
				with open(f'{datadirectory}/{datafilename}', 'a+') as file:	#This may cause a high write frequency. Don't use on a computer with a mechanical HDD!
					file.write(header)
					file.close()
					writesuccess = True
			except:
				print(f'Could not open file for writing header: {datafilename}')
				time.sleep(1)
				
				
	#Write the line to file
	writesuccess = False
	while not writesuccess:
		try:
			with open(f'{datadirectory}/{datafilename}', 'a+') as file:
				file.write(lineStr)
				file.write('\n')
				file.close()
				writesuccess = True
		except:
			print('Could not open file for writing')
			time.sleep(1)
	
	#print(lineStr)
	
	
	
if __name__ == '__main__':
	while(1):
		try:
			init()
			
			while(1):	#Main loop
				loop()
				time.sleep(.1)
		except Exception as e:
			print(f'Error running ES power logger script. Check connections. Auto retry...')
			print(e)
			time.sleep(5)