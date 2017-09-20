import machine, neopixel, ws2812ring, utime
from machine import Timer
import time
from umqtt.robust import MQTTClient
import json
import ubinascii
import sys

global x

class RingState:
  def __init__(self, ring):
    self.ring = ring
    self.animation = None
    self.timer = 0
    self.frame = 0
    self.last_time = time.ticks_ms()

    self.ring.fill((0, 0, 0))

  def update(self):
    if self.animation is None:
      return

    frame_data = ubinascii.a2b_base64(self.animation[self.frame].get("f", None))

    if frame_data is None or len(frame_data) == 0:
      return

    if time.ticks_ms() - self.last_time < self.timer:
      return

    for position in range(0, self.ring.count):
      if position < len(frame_data):
        color = (frame_data[position * 3], frame_data[(position * 3) + 1], frame_data[(position * 3) + 2])
        self.ring.set(position, color)

    neopixel_strand.write()

    self.timer = self.animation[self.frame].get("d", 50) #Delay before next frame in ms
    self.frame = self.frame + 1

    if self.frame >= len(self.animation):
      self.frame = 0

  def get_animation_from_file(self, filename):
    try:
      with open(filename) as animation_file:
        return json.load(animation_file)
        
    except Exception as e:
      return None

  def set_animation(self,animation_name):
    filename = "{0}-{1}.json.c".format(self.ring.count, animation_name)

    animation = self.get_animation_from_file(filename)

    if animation is None:
      #Look for a general purpose animation, no LED number
      filename = "{1}.json.c".format(self.ring.count, animation_name)

      animation = self.get_animation_from_file(filename)

    if animation is None:
      print("Unable to find animation for {0}".format(animation_name))
      self.animation = None
    else:
      self.animation = animation
      self.frame = 0
      self.timer = 0

      print("Animation loaded from {0} with {1} frames".format(filename, len(self.animation)))

def timerCallback(timer):
  for ring in rings:
    ring.update()

def setup(server):
  global neopixel_strand
  global outer_ring
  global middle_ring
  global inner_ring

  global rings

  neopixel_strand = neopixel.NeoPixel(machine.Pin(4), 44)
  outer_ring = RingState(ws2812ring.Ring(neopixel_strand, 0, 24))
  middle_ring = RingState(ws2812ring.Ring(neopixel_strand, 24, 12))
  inner_ring = RingState(ws2812ring.Ring(neopixel_strand, 36, 8))

  rings = [inner_ring, middle_ring, outer_ring]

  neopixel_strand.write()

  global mqtt_client

  mqtt_client = MQTTClient("status_light", server, user="status_light", password="9o6J5tiF10Mm")
  mqtt_client.set_callback(topic_update)
  mqtt_client.set_last_will(b"/status/indicator/0/connected", b"0")
  mqtt_client.connect()
  mqtt_client.subscribe(b"/status/indicator/0/0")
  mqtt_client.subscribe(b"/status/indicator/0/1")
  mqtt_client.subscribe(b"/status/indicator/0/2")
  mqtt_client.publish(b"/status/indicator/0/connected", b"1")

  readingTimer = Timer(-1)

  readingTimer.init(period=100, mode=Timer.PERIODIC, callback=timerCallback)


def topic_update(topic, msg):
  print((topic, msg))
  
  topic = bytes.decode(topic)
  msg = bytes.decode(msg)

  ring_index = int(topic.split("/")[-1])

  ring = rings[ring_index]

  ring.set_animation(msg)

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
