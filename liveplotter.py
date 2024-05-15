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

decimation = 1

livestartdate = True
livedatewindow_min = 60	#How much data to show if life date is enabled. Minutes.
startdate = datetime.datetime.strptime('2024-04-30T13-00-00', "%Y-%m-%dT%H-%M-%S")	#Data with timestamp prior to this will be ignored. Set to experiment start time.

#enddate = datetime.datetime.strptime('2024-03-04T15-00-00', "%Y-%m-%dT%H-%M-%S")
#enddate = None	#

timelabelinterval = 10	#Minutes, whole numbers only

phase1='1-Base'
phase2='2-Acid'
phase3='3-Brine'

colors = ['black', 'blue', 'green', 'red', 'pink', 'orange', 'grey']




#numfields = len(fieldnames)
stopflag = False

lastdrawtime = 0


fig, ((ax11, ax12), (ax21, ax22), (ax31, ax32)) = plt.subplots(3, 2)


bottomaxes = [ax31, ax32]
nonbottomaxes = [ax11, ax12, ax21, ax22]
allaxes = [ax11, ax12, ax21, ax22, ax31, ax32]

axpressure = ax11
axflow = ax21
axtemp = ax31
axcurrent = ax32
axdiffcurrent = ax22




def rollingaverage(a, window):
	#values = []
	#for i in range(0, len(a)):
	#	startindex = max(0, i-int(window/2))
	#	stopindex = min(len(a)-1, i+int(window/2))
	#	dist = (stopindex-startindex) + 1
		
	#	valuesum = 0
	#	for i in range(startindex, stopindex):
	#		valuesum += a[i]
			
	#	if dist > window/2:
	#		value = valuesum / dist
	#	else:
	#		value = a[i]
	#	
	#	values.append(value)
	
	
	#return np.rolling(a, window)
	
	
	ret = np.convolve(a, np.ones(window), 'valid')/window	#Apply rolling average. Mode handles edge condition. Divide by window.
	while len(ret) < len(a):
		ret = np.append(ret, 0)
		
	return ret
	
	#return values


def onpress(event):
	global stopflag
	sys.stdout.flush()
	if event.key == 'q':
		stopflag = True
		

def readesdataarray():	#Modified copy of readdataarray() which reads the ES data file
	datadir = 'esdata'
	
	#startfile = startdate.strftime("%Y-%m-%dT%H.csv")
	#startfile = startdate.strftime("%Y-%m-%dT%H-%M.csv")
	#print(f'First file is: {startfile}')

	fileanddirlist = os.listdir(datadir)
	fileanddirlist = [os.path.join(datadir, file) for file in fileanddirlist]	#Make the full relative path from the directory list
	
	filelist = []
	for item in fileanddirlist:
		if not os.path.isdir(item):
			filelist.append(item)
		
		

	datastr = ''	#Holds all data
	atstartfile = False
	print(f'{len(filelist)} files available')
	#print(filelist)
	
	filequerylist = []
	querydate = startdate

	while(querydate < datetime.datetime.now()):
		filequerylist.append(querydate.strftime(os.path.join(datadir, "%Y-%m-%dT%H.csv")))
		querydate = querydate + datetime.timedelta(hours=1)	#Files are named by the hour. Get the next file. TODO: is this safe? What is the precision of 1-hour increments over time?

	#print(f'{len(filequerylist)} files of interest:')
	#print(filequerylist)
	
	
	
	
	for file in filelist:	#Iterate through files which DO appear in the data directory
		#if startfile in file:	#If the file path to be loaded contains the start date
		#	atstartfile = True
			
		#if not atstartfile:
		#	continue
			
		if file in filequerylist:	#If this file is also in the list of possible files which we would want to load
			print(f'Loading: {file}')
			datastr += open(file, 'r').read()
		
	print(f'Loaded {len(datastr)} characters')


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
			if row[0] == 'Time':
			
				#print(f'Row {rowindex} is header.')
				
				#Header row
				headerfound = True
				
				header = row
				
				datacolumns = len(header)
				#print(f'Header: {header}')
				#print(f'{datacolumns} columns.')
				
			rowindex+=1
			continue	#Ignore rows before first header line
			
		if row[0] == 'Time':	#Do not process header rows as data.
			rowindex+=1
			continue
			
		if not (rowindex%decimation)==0:
			rowindex+=1
			continue
			
		#print(f'Row {rowindex} is data.')
		
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
			
		#print(date)
		
		datarow = [date]
		
		for i in range(1, len(header)):
			value = row[i]
			
			#if value.isnumeric():
			value = float(value)
				
			#elif value == 'err':
			#	value = None
				
			#print(f'Including elemnt {i} ({row[i]})')
				
			datarow.append(value)
			
		if not len(datarow) == datacolumns:
			print(f'Data row invalid:')
			print(datarow)
			pass
		
		else:
			data.append(datarow)
			#print(f'Accepted row: {datarow}')
			
			
	print(f'Loaded {len(data)} rows')
		
	rowindex+=1
	return header, data


def readdataarray():
	datadir = 'data'
	
	#startfile = startdate.strftime("%Y-%m-%dT%H.csv")
	#startfile = startdate.strftime("%Y-%m-%dT%H-%M.csv")
	#print(f'First file is: {startfile}')

	fileanddirlist = os.listdir(datadir)
	fileanddirlist = [os.path.join(datadir, file) for file in fileanddirlist]	#Make the full relative path from the directory list
	
	filelist = []
	for item in fileanddirlist:
		if not os.path.isdir(item):
			filelist.append(item)
			
	filequerylist = []
	querydate = startdate
			
	while(querydate < datetime.datetime.now()):
		filequerylist.append(querydate.strftime(os.path.join(datadir, "%Y-%m-%dT%H.csv")))
		querydate = querydate + datetime.timedelta(hours=1)	#Files are named by the hour. Get the next file. TODO: is this safe? What is the precision of 1-hour increments over time?

	#print(f'{len(filequerylist)} files of interest:')
	#print(filequerylist)
	
	
	datastr = ''	#Holds all data
	print(f'{len(filelist)} files available')
	
	for file in filelist:	#Iterate through files which DO appear in the data directory
		#if startfile in file:	#If the file path to be loaded contains the start date
		#	atstartfile = True
			
		#if not atstartfile:
		#	continue
			
		if file in filequerylist:	#If this file is also in the list of possible files which we would want to load
			print(f'Loading: {file}')
			datastr += open(file, 'r').read()
		
		

	
		
	print(f'Loaded {len(datastr)} characters')


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
			
				#print(f'Header found at {rowindex}')
				
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
				#print(f'Header: {header}')
				#print(f'{datacolumns} columns.')
				
			rowindex+=1
			continue	#Ignore rows before first header line
		
			
			
		if not row[1] == 'DATA':
			rowindex+=1
			continue
			
		if not (rowindex%decimation)==0:
			rowindex+=1
			continue
			
		#print(f'Row {rowindex} is data.')
		
		
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


def loop():
	global stopflag, startdate
	
	if livestartdate:
		startdate = datetime.datetime.now() - datetime.timedelta(minutes=livedatewindow_min)
	
	#print(f'Draw!')
	lastdrawtime = time.time()
	
	#Fix plot memory leak
	#plt.cla()
	#plt.draw()
	#plt.pause(1)
	
	ax11.cla()
	ax21.cla()
	ax31.cla()
	ax12.cla()
	ax22.cla()
	ax32.cla()
	
	esheader, esdata = readesdataarray()
	
	if esheader is None or len(esdata)==0:
		print(f'No ES header/data available!')
		time.sleep(5)
		return
	
	esdf = pandas.DataFrame(esdata)
	esdf.columns = esheader
	
	esdf.set_index('Time')
	esdf.sort_values(by=['Time'])
	
	
	
		
	header, data = readdataarray()
	if header is None or len(data)==0:
		print(f'No header/data available!')
		time.sleep(5)
		return
		
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

	#fq1 = rollingaverage(df[f'1:14:Value']*1.8315-373.63, window)	#0-1500 mL/min from prior to 2024-05-09
	#fq2 = rollingaverage(df[f'1:13:Value']*1.8315-373.63, window)
	#fq3 = rollingaverage(df[f'1:12:Value']*1.8315-373.63, window)
	
	fq1 = rollingaverage(df[f'1:14:Value']*3.663-747.3, window)	#0-3000 mL/min
	fq2 = rollingaverage(df[f'1:13:Value']*3.663-747.3, window)
	fq3 = rollingaverage(df[f'1:12:Value']*3.663-747.3, window)

	pot = df[f'1:15:Value']/1024
	
	#v1 = esdf[f'V1']*1000*.53-.01		#2024-04-30 Calibration with CC PSU
	#v2 = esdf[f'V2']*1000*.5-1.13
	#v3 = esdf[f'V3']*1000*.63+.16
	#v4 = esdf[f'V4']*1000*.77-.02
	#v5 = esdf[f'V5']*1000*.58+.05
	#v6 = esdf[f'V6']*1000*.65-.06
	
	i1 = esdf[f'V1']*-1489.96952515665		#2024-05-09 BAC testing
	i2 = esdf[f'V2']*-1489.96952515665
	i3 = esdf[f'V3']*-1489.96952515665
	i4 = esdf[f'V4']*-1489.96952515665
	i5 = esdf[f'V5']*-1489.96952515665
	i6 = esdf[f'V6']*-1489.96952515665


	#tempdf = esdf[['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']]
	#didf = tempdf.diff()
	
	#print(esdf)
	diffcurrentaveragewindow = 1000
	di1 = np.gradient(esdf['V1'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	di2 = np.gradient(esdf['V2'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	di3 = np.gradient(esdf['V3'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	di4 = np.gradient(esdf['V4'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	di5 = np.gradient(esdf['V5'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	di6 = np.gradient(esdf['V6'].values, esdf['Time'].astype('int64').values / (1e9*60*60))
	
	di1 = rollingaverage(di1, diffcurrentaveragewindow)
	di2 = rollingaverage(di2, diffcurrentaveragewindow)
	di3 = rollingaverage(di3, diffcurrentaveragewindow)
	di4 = rollingaverage(di4, diffcurrentaveragewindow)
	di5 = rollingaverage(di5, diffcurrentaveragewindow)
	di6 = rollingaverage(di6, diffcurrentaveragewindow)
	
	
	
	
	axpressure.set_title('')
	axpressure.set_ylabel(r'Guage Pressure ($Lb-in^{-2}$)')
	axpressure.set_xlabel('Time')
	axpressure.set_ylim([-10, 30])
	axpressure.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(axpressure.xaxis.get_major_locator()))
	axpressure.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=timelabelinterval))

	axpressure.plot(df['Time'], pt1, linewidth=1, markersize=0, color=colors[0])
	axpressure.plot(df['Time'], pt2, linewidth=1, markersize=0, color=colors[1])
	axpressure.plot(df['Time'], pt3, linewidth=1, markersize=0, color=colors[2])
	axpressure.plot(df['Time'], pt4, linewidth=1, markersize=0, color=colors[3], linestyle=(0, (2, 10)))
	axpressure.plot(df['Time'], pt5, linewidth=1, markersize=0, color=colors[4], linestyle=(0, (2, 10)))
	axpressure.plot(df['Time'], pt6, linewidth=1, markersize=0, color=colors[5], linestyle=(0, (2, 10)))

	ptv1 = pt1[len(pt1)-1]
	ptv2 = pt2[len(pt2)-1]
	ptv3 = pt3[len(pt3)-1]
	ptv4 = pt4[len(pt4)-1]
	ptv5 = pt5[len(pt5)-1]
	ptv6 = pt6[len(pt6)-1]

	axpressure.legend([f'{phase1} pre {ptv1:.1f}', f'{phase2} pre {ptv2:.1f}', f'{phase3} pre {ptv3:.1f}', f'{phase1} post {ptv4:.1f}', f'{phase2} post {ptv5:.1f}', f'{phase3} post {ptv6:.1f}'], loc='upper left')

	#ax12 = axpressure.twinx()
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







	
	axflow.set_title('')
	axflow.set_ylim([0, 3100])
	axflow.set_ylabel(r'Flow ($mL-min^{-1}$)')
	axflow.set_xlabel('Time')
	axflow.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(axflow.xaxis.get_major_locator()))
	axflow.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=timelabelinterval))

	axflow.plot(df['Time'], fq1, linewidth=1, markersize=0, color=colors[0])
	axflow.plot(df['Time'], fq2, linewidth=1, markersize=0, color=colors[1])
	axflow.plot(df['Time'], fq3, linewidth=1, markersize=0, color=colors[2])

	axflow.legend([f'{phase1} {fq1[-1]:.0f}', f'{phase2} {fq2[-1]:.0f}', f'{phase3} {fq3[-1]:.0f}'], loc='upper left')

	
	
	
	axtemp.set_title('')
	axtemp.set_ylabel(r'Temperature ($\degree C$)')
	axtemp.set_ylim([10, 30])
	axtemp.set_xlabel('Time')
	axtemp.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(axtemp.xaxis.get_major_locator()))
	axtemp.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=timelabelinterval))

	axtemp.plot(df['Time'], rtd1, linewidth=1, markersize=0, color=colors[0])
	axtemp.plot(df['Time'], rtd2, linewidth=1, markersize=0, color=colors[1])
	axtemp.plot(df['Time'], rtd3, linewidth=1, markersize=0, color=colors[2])
	axtemp.plot(df['Time'], rtd4, linewidth=1, markersize=0, color=colors[3])

	axtemp.legend([f'{phase1} {rtd1[-1]:.1f}', f'{phase2} {rtd2[-1]:.1f}', f'{phase3} {rtd3[-1]:.1f}', f'Brine Supply {rtd4[-1]:.1f}'], loc='upper left')


	axcurrent.set_title('')
	axcurrent.set_ylabel(r'Current ($A$)')
	axcurrent.set_ylim([0, 25])
	axcurrent.set_xlabel('Time')
	axcurrent.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(axcurrent.xaxis.get_major_locator()))
	axcurrent.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=timelabelinterval))
	
	channels = [i1, i2, i3, i4, i5, i6]
	names = [f'I1 {i1[len(i1)-1]:.1f}', f'I2 {i2[len(i2)-1]:.1f}', f'I3 {i3[len(i3)-1]:.1f}', f'I4 {i4[len(i4)-1]:.1f}', f'I5 {i5[len(i5)-1]:.1f}', f'I6 {i6[len(i6)-1]:.1f}']

	for i in range(0, len(channels)):
		axcurrent.plot(esdf['Time'], channels[i], linewidth=1, markersize=0, color=colors[i])

	axcurrent.legend(names, loc='upper left')
	
	
	
	
	axdiffcurrent.set_title('')
	axdiffcurrent.set_ylabel(r'$dI/dt (mA-hr^{-1})$')
	#axdiffcurrent.set_ylim([-1, 1])
	axdiffcurrent.set_xlabel('Time')
	axdiffcurrent.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(axcurrent.xaxis.get_major_locator()))
	axdiffcurrent.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=timelabelinterval))
	
	channels = [di1, di2, di3, di4, di5, di6]
	#channels = [di1]
	#names = [f'dI1 {di1[len(di1)-1]:.1f}', f'dI2 {di2[len(di2)-1]:.1f}', f'dI3 {di3[len(di3)-1]:.1f}', f'dI4 {di4[len(di4)-1]:.1f}', f'dI5 {di5[len(di5)-1]:.1f}', f'dI6 {di6[len(di6)-1]:.1f}']
	names = []
	
	#croppedtime = esdf['Time']
	#sizedifference = len(esdf['Time']) - len(di1)
	#before = np.ceil(sizedifference/2)
	#after = np.floor(sizedifference/2)
	
	#croppedtime = croppedtime[before:-after]
	
	#print(f'Cropped time: {len(croppedtime)}')
	#print(f'Diff current: {len(di1)}')
	
	
	for i in range(0, len(channels)):
		names.append(f'dI{i} {np.mean(channels[i]):.2f}')
		
	for i in range(0, len(channels)):
		
		axdiffcurrent.plot(esdf['Time'], channels[i], linewidth=1, markersize=0, color=colors[i])

	axdiffcurrent.legend(names, loc='upper left')
	
	
	
	fig.tight_layout()

	#Turn on minor gridlines for the plots
	for a in allaxes:
		a.grid(True)
		a.grid(which='minor', color='grey', linestyle=':')
		a.minorticks_on()
	
	plt.draw()

if __name__ == '__main__':
	fig.canvas.mpl_connect('key_press_event', onpress)
	print(f'Press Q to quit at any time.')

	while not stopflag and plt.fignum_exists(fig.number):
		try:
			print(f'======== Draw! ========')
			loop()
			plt.pause(.1)
			
		except Exception as e:
			print(f'Error running plotter. Auto retry...')
			print(e)
			time.sleep(5)
		