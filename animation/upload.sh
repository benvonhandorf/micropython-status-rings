#/bin/bash

for animation in *.json
do
	python3 convert_animation.py $animation
	ampy --port /dev/ttyUSB0 put $animation.compressed
done