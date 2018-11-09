import machine, neopixel, ws2812ring, utime
from machine import Timer
import time
from umqtt.robust import MQTTClient
import json
import ubinascii
import sys

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

class StatusLight:
  def __init__(self, segmentDescriptors, brightnessReduction):

    self.rings = []

    totalPixels = 0

    for segmentCount in segmentDescriptors:
      totalPixels = totalPixels + segmentCount

    print("Configuring {0} total pixels".format(totalPixels))

    self.neopixel_strand = neopixel.NeoPixel(machine.Pin(4), totalPixels)

    currentOffset = 0

    for segmentCount in segmentDescriptors:
      print("Configuring ring from {} with {} pixels".format(currentOffset, segmentCount))
      ring = RingState(ws2812ring.WS2812Ring(self.neopixel_strand, currentOffset, segmentCount, brightnessReduction))
      currentOffset = currentOffset + segmentCount
      self.rings.append(ring)

    self.neopixel_strand.write()

    self.readingTimer = Timer(-1)

    self.readingTimer.init(period=100, mode=Timer.PERIODIC, callback=self.timerCallback)

  def stop(self):
    self.readingTimer.deinit()

  def initializing(self, initState):
    ring = self.rings[initState % len(self.rings)]

    if initState < 3:
      ring.set_animation("red-pulse")
    else:
      ring.set_animation("green-pulse")

    self.neopixel_strand.write()

  def timerCallback(self, timer):
    for ring in self.rings:
      ring.update()

    self.neopixel_strand.write()

  def setup(self, server, user, password, topic):
    self.baseTopic = topic

    self.mqtt_client = MQTTClient("status_light", server, user=user, password=password)
    self.mqtt_client.set_callback(self.topic_update)
    print("Last will topic: " "{0}/connected".format(self.baseTopic))
    self.mqtt_client.set_last_will(bytes("{0}/connected".format(self.baseTopic), 'utf-8'), b"0")
    self.mqtt_client.connect()
    self.mqtt_client.subscribe(bytes("{0}/0".format(self.baseTopic), 'utf-8'))
    self.mqtt_client.subscribe(bytes("{0}/1".format(self.baseTopic), 'utf-8'))
    self.mqtt_client.subscribe(bytes("{0}/2".format(self.baseTopic), 'utf-8'))
    self.mqtt_client.publish(bytes("{0}/connected".format(self.baseTopic), 'utf-8'), b"1")


  def topic_update(self, topic, msg):
    print((topic, msg))
    
    topic = bytes.decode(topic)
    msg = bytes.decode(msg)

    ring_index = int(topic.split("/")[-1])

    ring = self.rings[ring_index]

    ring.set_animation(msg)

    self.neopixel_strand.write()

  def main(self):

    while True:
        if True:
          print("waiting for message")

          # Blocking wait for message
          self.mqtt_client.wait_msg()  
        else:
          # Non-blocking wait for message
          self.mqtt_client.check_msg()
          # Then need to sleep to avoid 100% CPU usage (in a real
          # app other useful actions would be performed instead)
          time.sleep(1)

    self.mqtt_client.disconnect()

if __name__ == "__main__":
  setup("192.168.10.105")
  main()  
