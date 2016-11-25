import sys
import network
import utime
from machine import Pin, SPI
from umqtt import MQTTClient
from max7219 import Matrix8x8
import http_client

print('* start')

spi = SPI()
display = Matrix8x8(spi, Pin(15), 4)
display.fill(False)
display.show()

display.puts('start')
display.show()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("SSID", "WIFI_PASSWORD")
ip = '0.0.0.0'

while ip == '0.0.0.0':
	print('waiting for internet')
	ip = list(sta_if.ifconfig())[0]
	utime.sleep(3)

print(ip)
display.puts(ip[-5:])
display.show()
utime.sleep(3)

app_id = 'YOUR_APP_ID'
api_key = 'YOUR_APP_KEY'
md5_app_id = 'xxxxxxxxxxxxxxxxxxx'	# md5(app_id)
sensors_id = [32694]
headers = {'User-Agent': app_id}
data = {'cmd': 'sensorsValues', 'uuid': md5_app_id, 'api_key': api_key, 'sensors': sensors_id}

while True:
	try:
		r = http_client.post('http://narodmon.ru/api', headers=headers, json=data)
		print(r.text)
		d = r.json()
		temp = round(d['sensors'][0]['value'])
		sign = '+' if temp >= 0 else ''

		str_display = '%s%d' % (sign, temp)
		pos = int((4*8 - len(str_display)*5) / 2)
		
		display.fill(False)
		display.puts(str_display, pos)
		display.show()
	except Exception as e:
		sys.print_exception(e)
		display.fill(False)
		display.puts('error')
		display.show()

	utime.sleep(90)
