upload:
	ampy --port /dev/ttyUSB0 put micropython-ws2812ring/ws2812ring.py 
	ampy --port /dev/ttyUSB0 put micropython-configurator/configurator.py 
	ampy --port /dev/ttyUSB0 put status_light.py 
	ampy --port /dev/ttyUSB0 put config.json 
	ampy --port /dev/ttyUSB0 put main.py
