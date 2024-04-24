import requests
import xml

ipaddress = '192.168.2.153'

while 1:
	try:
		x = requests.get(f'{ipaddress}/analoginput/all')
	except e:
		print f'Error making query'
		print e

	print x.status_code

	tree = xml.etree.ElementTree.parse(x.content)
	print(tree)