#/bin/bash

for animation in *.json
do
	python3 convert_animation.py $animation
done


for animation in *.json.c
do
	ampy --port /dev/ttyUSB0 put $animation
done