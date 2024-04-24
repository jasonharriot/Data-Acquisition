import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import time
import datetime
import pandas
import timeit
import os
import scipy
import csv
import io

matplotlib.use("QtAgg")	#This prevents the plot from grabbing focus from other windows. Still grabs focus from console.



#setup
numsensors = 16
fieldnames = ['Node ID', 'Sensor ID', 'Type', 'Value']
numfields = len(fieldnames)

livestartdate = True
startdate = datetime.datetime.strptime('2024-03-04T12-00-00', "%Y-%m-%dT%H-%M-%S")	#Data with timestamp prior to this will be ignored. Set to experiment start time.


#enddate = datetime.datetime.strptime('2024-03-04T15-00-00', "%Y-%m-%dT%H-%M-%S")
enddate = None
	
docontinuous = False
stopflag = False
	

phase1='Base'
phase2='Acid'
phase3='Brine'
	
	
	
	
	

lastdrawtime = 0


#def getvalues(df, nodeid, sensorid):
	#return df.loc[(df['Node ID'] == nodeid) & (df['Sensor ID'] == sensorid)]

def rollingaverage(a, window):
	ret = np.convolve(a, np.ones(window), 'same')/window	#Apply rolling average. Mode handles edge condition. Divide by window.
	return ret



#if len(sys.argv) < 2:	#Data files should be specified as parameters. Single file, multiple files, or single directory of (only!) files
#	print("Specify files or directory.")
	


#arg1 = sys.argv[1]
arg1 = 'data'	#Data directory

def onpress(event):
	global stopflag
	sys.stdout.flush()
	if event.key == 'q':
		stopflag = True


def readdataarray():
	global startdate
	if livestartdate:
		startdate = datetime.datetime.now() - datetime.timedelta(minutes=2)
	
	startfile = startdate.strftime("%Y-%m-%dT%H.csv")
	#startfile = startdate.strftime("%Y-%m-%dT%H-%M.csv")
	print(f'First file is: {startfile}')
	
	
	if len(sys.argv) > 2:	#If multiple files
		filelist = sys.argv[1:]

	elif os.path.exists(arg1) and os.path.isdir(arg1):	#If the first argument is a directory
		fileanddirlist = os.listdir(arg1)
		fileanddirlist = [os.path.join(arg1, file) for file in fileanddirlist]	#Make the full relative path from the directory list
		
		filelist = []
		for item in fileanddirlist:
			if not os.path.isdir(item):
				filelist.append(item)
				
	else:
		filelist = [arg1]	#Single file
		
		

	datastr = ''	#Holds all data
	atstartfile = False
	print(f'{len(filelist)} files available')
	for file in filelist:
		if startfile in file:	#If the file path to be loaded contains the start date
			atstartfile = True
			
		if not atstartfile:
			continue
			
		print(f'Loading: {file}')
		datastr += open(file, 'r').read()


	data = []	#Array to hold all the data, in proper order. A dataframe will be made from this later on, but constructing the data as a simple array first is fastest.


	#print('Preparing fields')
	
	
	f = io.StringIO(datastr)
	reader = csv.reader(f, delimiter=',')
	headerfound = False
	datacolumns = 0	#Number of columns found in the header row. Check against data rows.

	header = None	#Header row for pandas dataframe


	rowindex = 0
	
	for row in reader:
		#print(f'Parsing: {row}')
		
		if len(row) < 3:
			rowindex+=1
			continue
			
		if not headerfound:
			if row[1] == 'HEADER':
			
				print(f'Header found at {rowindex}')
				
				#Header row
				headerfound = True
				
				header = ['Time']
				
				for i in range(2, len(row)):
					if len(row[i]) < 1:
						break
						
					indices = row[i].split(':')
					#print(indices)
					nodeid = 1	#node ID not implemented in header row yet.
					sensorid = int(indices[0])
					fieldname = fieldnames[int(indices[1])]
					header.append(f'{nodeid}:{sensorid}:{fieldname}')
				
				datacolumns = len(header)
				print(f'Header: {header}')
				print(f'{datacolumns} columns.')
				
			rowindex+=1
			continue	#Ignore rows before first header line
		
			
			
		if not row[1] == 'DATA':
			rowindex+=1
			continue
		
		date = None
		try:
			datestr = row[0]
			hundreths = datestr[20:]
			microseconds = int(hundreths)*10000
			datestr = datestr[:20]
			datestr += f'{microseconds:06d}'
			date = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H-%M-%S_%f")
		except:
			print("Couldn't parse timestamp:")
			print(row[0])
			rowindex+=1
			continue
			
		if date < startdate:
			rowindex+=1
			continue
			
		if not enddate is None and date > enddate:
			break
			
		#print(date)
		
		datarow = [date]
		
		for i in range(2, len(row)):
			if len(row[i]) < 1:
				rowindex+=1
				continue
				
			if row[i] == '' or row[i] is None:
				rowindex+=1
				continue
				
				
			value = row[i]
			if value.isnumeric():
				value = int(value)
				
			elif value == 'err':
				value = None
				
			#print(f'Including elemnt {i} ({row[i]})')
				
			datarow.append(value)
			
		if not len(datarow) == datacolumns:
			#print(f'Data row invalid:')
			#print(datarow)
			pass
		
		else:
			data.append(datarow)
			
			
	print(f'Loaded {len(data)} rows')
		
	rowindex+=1
	return header, data

#################
#fig1, ax11 = plt.subplots()
#fig2, ax21 = plt.subplots()
#fig3, ax31 = plt.subplots()

fig, (ax11, ax21, ax31) = plt.subplots(1, 3)


fig1 = fig
fig2 = fig
fig3 = fig

fig.canvas.mpl_connect('key_press_event', onpress)
print(f'Press Q to quit at any time.')

while not stopflag:
	#while 1:
		#time.sleep(.1)
		#plt.pause(1)
		
		#if time.time() - lastdrawtime > 2:
		#	break
		
	plt.pause(.2)
		
	print(f'Draw!')
		
	lastdrawtime = time.time()
	
	
		
	header, data = readdataarray()
	if header is None:
		print(f'No header available!')
		time.sleep(1)
		continue
		
	df = pandas.DataFrame(data)

	#Set header
	df.columns = header

	#print('Sorting...')
		 
	df.set_index('Time')
	df.sort_values(by=['Time'])
	#print(df)





	window = 1


	rtd1 = rollingaverage(df['1:0:Value']*.1221-24.908, window)
	rtd2 = rollingaverage(df['1:1:Value']*.1221-24.908, window)
	rtd3 = rollingaverage(df['1:2:Value']*.1221-24.908, window)
	rtd4 = rollingaverage(df['1:3:Value']*.1221-24.908, window)
	
	#rtd1d = derriva

	pt1 = rollingaverage(df[f'1:6:Value']*.061050-12.45, window)
	pt2 = rollingaverage(df[f'1:7:Value']*.061050-12.45, window)
	pt3 = rollingaverage(df[f'1:8:Value']*.061050-12.45, window)
	pt4 = rollingaverage(df[f'1:9:Value']*.061050-12.45, window)
	pt5 = rollingaverage(df[f'1:10:Value']*.061050-12.45, window)
	pt6 = rollingaverage(df[f'1:11:Value']*.061050-12.45, window)

	fq1 = rollingaverage(df[f'1:14:Value']*1.8315-373.63, window)
	fq2 = rollingaverage(df[f'1:13:Value']*1.8315-373.63, window)
	fq3 = rollingaverage(df[f'1:12:Value']*1.8315-373.63, window)

	pot = df[f'1:15:Value']/1024

	#if 0:	#Draw fft?
	#	# Number of samplepoints
	#	N = len(rtd0['tempvalue'])
	#	# sample spacing
	#	T = .1
	#	f=1/T
	#	yf = scipy.fftpack.fft(rtd0['tempvalue'].values)
	#	xf = np.linspace(0.0, f/2, N//2)

	#	figfft, axfft = plt.subplots()
	#	axfft.plot(xf, 2.0/N * np.abs(yf[:N//2]))
	#	axfft.set_yscale('log')
	#	plt.draw()



	ax11.cla()
	ax21.cla()
	ax31.cla()

	
	ax11.set_title('')
	ax11.set_ylabel(r'Guage Pressure ($Lb-in^{-2}$)')
	ax11.set_xlabel('Time')
	ax11.set_ylim([-5, 30])
	ax11.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(ax11.xaxis.get_major_locator()))
	ax11.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=60))

	ax11.plot(df['Time'], pt1, linewidth=1, markersize=0, color='black')
	ax11.plot(df['Time'], pt2, linewidth=1, markersize=0, color='blue')
	ax11.plot(df['Time'], pt3, linewidth=1, markersize=0, color='green')
	ax11.plot(df['Time'], pt4, linewidth=1, markersize=0, color='black', linestyle=(0, (2, 10)))
	ax11.plot(df['Time'], pt5, linewidth=1, markersize=0, color='blue', linestyle=(0, (2, 10)))
	ax11.plot(df['Time'], pt6, linewidth=1, markersize=0, color='green', linestyle=(0, (2, 10)))

	ax11.legend([f'{phase1} pre', f'{phase2} pre', f'{phase3} pre', f'{phase1} post', f'{phase2} post', f'{phase3} post'])

	#ax12 = ax11.twinx()
	#ax12.set_ylabel(r'Pump speed')
	#ax12.set_ylim([-.5, 1.5])
	#yticks = ax12.yaxis.get_major_ticks()
	#def fmtfunc(x, pos):
	#	if x >= 0 and x <= 1:
	#		return str(x)
			
	#	return ''
		
	#formatter = matplotlib.ticker.FuncFormatter(fmtfunc)
	#ax12.yaxis.set_major_formatter(formatter)

	#ax12.plot(df['Time'], pot, linewidth=1, markersize=0, color='black', linestyle=':')







	
	ax21.set_title('')
	ax21.set_ylim([-100, 1500])
	ax21.set_ylabel(r'Flow ($mL-min^{-1}$)')
	ax21.set_xlabel('Time')
	ax21.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(ax21.xaxis.get_major_locator()))
	ax21.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=60))

	ax21.plot(df['Time'], fq1, linewidth=1, markersize=0, color='black')
	ax21.plot(df['Time'], fq2, linewidth=1, markersize=0, color='blue')
	ax21.plot(df['Time'], fq3, linewidth=1, markersize=0, color='green')

	ax21.legend([f'{phase1}', f'{phase2}', f'{phase3}'])

	
	ax31.set_title('')
	ax31.set_ylabel(r'Temperature ($\degree C$)')
	ax31.set_ylim([10, 30])
	ax31.set_xlabel('Time')
	ax31.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(ax31.xaxis.get_major_locator()))
	ax31.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=60))

	ax31.plot(df['Time'], rtd1, linewidth=1, markersize=0, color='black')
	ax31.plot(df['Time'], rtd2, linewidth=1, markersize=0, color='blue')
	ax31.plot(df['Time'], rtd3, linewidth=1, markersize=0, color='green')
	ax31.plot(df['Time'], rtd4, linewidth=1, markersize=0, color='red')

	ax31.legend([f'{phase1}', f'{phase2}', f'{phase3}', f'Brine Supply'])

	plt.draw()

	#if not docontinuous:
	#	plt.show()
	#	break

