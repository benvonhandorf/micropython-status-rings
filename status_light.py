import machine, neopixel, ws2812ring, utime
from machine import Timer
import time
from umqtt.robust import MQTTClient

global x

def timerCallback(timer):
	if x == 6000:
		x = 0

	inner_ring.rotateCCW()

	if x % 2 == 0:
		middle_ring.rotateCW()

	if x % 3 == 0:
		outer_ring.rotateCCW()

	neopixel_strand.write()

	x = x + 1

# readingTimer = Timer(-1)

# readingTimer.init(period=100, mode=Timer.PERIODIC, callback=timerCallback)

def setup(server):
  global neopixel_strand
  global outer_ring
  global middle_ring
  global inner_ring

  global rings

  neopixel_strand = neopixel.NeoPixel(machine.Pin(4), 44)
  outer_ring = ws2812ring.Ring(neopixel_strand, 0, 24)
  middle_ring = ws2812ring.Ring(neopixel_strand, 24, 12)
  inner_ring = ws2812ring.Ring(neopixel_strand, 36, 8)

  rings = [inner_ring, middle_ring, outer_ring]

  outer_ring.fill((0, 0, 0))
  middle_ring.fill((0, 0, 0))
  inner_ring.fill((0, 0, 0))

  neopixel_strand.write()

  global mqtt_client

  mqtt_client = MQTTClient("status_light", server, user="status_light", password="9o6J5tiF10Mm")
  mqtt_client.set_callback(sub_cb)
  mqtt_client.set_last_will(b"/status/indicator/0/connected", b"0")
  mqtt_client.connect()
  mqtt_client.subscribe(b"/status/indicator/0/0")
  mqtt_client.subscribe(b"/status/indicator/0/1")
  mqtt_client.subscribe(b"/status/indicator/0/2")
  mqtt_client.publish(b"/status/indicator/0/connected", b"1")

def sub_cb(topic, msg):
  print((topic, msg))
  
  topic = bytes.decode(topic)
  msg = bytes.decode(msg)

  ring_index = int(topic.split("/")[-1])

  ring = rings[ring_index]

  if msg.find("red") != -1:
    ring.fill((255, 0, 0))
  elif msg.find("green") != -1:
    ring.fill((0, 255, 0))
  else:
    ring.fill((0, 0, 0))

  neopixel_strand.write()

def main():

  while True:
      if True:
        print("waiting for message")

        # Blocking wait for message
        mqtt_client.wait_msg()  
      else:
        # Non-blocking wait for message
        mqtt_client.check_msg()
        # Then need to sleep to avoid 100% CPU usage (in a real
        # app other useful actions would be performed instead)
        time.sleep(1)

  mqtt_client.disconnect()

if __name__ == "__main__":
  setup("192.168.10.105")
  main()  
