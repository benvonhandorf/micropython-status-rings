from machine import Pin
from apa102 import APA102
from apa102ring import APA102Ring
from machine import Timer
import urandom
import math

class PictureFrame:


  def pushrand(cycleCount, ringIndex, ring):
    h = (urandom.getrandbits(4) - 8) / 1024
    s = (urandom.getrandbits(8) - 127) / 1024
    v = (urandom.getrandbits(8) - 127) / 1024
    ring.pushOffsetHSV((h, s, v))

  def baseAndWhite(cycleCount, ringIndex, ring):
    baseHSV = ring.baseHSV

    for counter in range(0, ring.count):
      if (counter + ringIndex + cycleCount) % 2 == 0:
        ring.pushOffsetHSV((0, 0, 0))
      else:
        ring.pushOffsetHSV((0.0, -baseHSV[1], 1.0 - baseHSV[2]))

  def flashWhite(cycleCount, ringIndex, ring):
    baseHSV = ring.baseHSV

    for counter in range(0, ring.count):
      if cycleCount % 2 == 0:
        ring.pushOffsetHSV((0, 0, 0))
      else:
        ring.pushOffsetHSV((0.0, -baseHSV[1], 1.0 - baseHSV[2]))

  def slowFadeToWhite(cycleCount, ringIndex, ring):
    baseHSV = ring.baseHSV

    for counter in range(0, ring.count):
      fraction = math.sin(((counter + ringIndex + cycleCount) / 15) * 1.57)

      if (counter + ringIndex + cycleCount) % 2 == 0:
        ring.pushOffsetHSV((0, 0, 0))
      else:
        ring.pushOffsetHSV((0.0, -baseHSV[1] * fraction , (1.0 - baseHSV[2]) * fraction))

  def fill(cycleCount, ringIndex, ring):
    for counter in range(0, ring.count):
      ring.pushOffsetHSV((0, 0, 0))

  configurations = [
    ((12, 25), [((0.0, 1.0, 0.5), baseAndWhite), #Christmas
      ((0.0, 1.0, 0.5), baseAndWhite),
      ((0.0, 1.0, 0.5), baseAndWhite),
      ((0.0, 1.0, 0.5), baseAndWhite),
      ((0.0, 1.0, 0.5), baseAndWhite)]),
    ((1, 1), [((0.11, 0.8, 0.5), baseAndWhite), #New Years Day
      ((0.11, 0.8, 0.5), fill),
      ((0.11, 0.8, 0.5), slowFadeToWhite),
      ((0.11, 0.8, 0.5), fill),
      ((0.11, 0.8, 0.5), slowFadeToWhite)]),
    ((2, 14), [((0.0, 0.75, 0.5), flashWhite), #Feb 14
      ((0.65, 1.0, 0.4), pushrand),
      ((0.33, 0.9, 0.3), pushrand),
      ((0.16, 0.8, 0.4), pushrand),
      ((0.55, 0.8, 0.4), slowFadeToWhite)]),
    ((8, 12), [((0.0, 0.75, 0.5), pushrand), #August 12
      ((0.65, 1.0, 0.4), flashWhite),
      ((0.33, 0.9, 0.3), pushrand),
      ((0.16, 0.8, 0.4), pushrand),
      ((0.55, 0.8, 0.4), pushrand)]),
    ((8, 17), [((0.0, 0.75, 0.5), pushrand), #August 17
      ((0.65, 1.0, 0.4), pushrand),
      ((0.33, 0.9, 0.3), flashWhite),
      ((0.16, 0.8, 0.4), pushrand),
      ((0.55, 0.8, 0.4), pushrand)]),
    ((12, 14), [((0.0, 0.75, 0.5), pushrand), #Oct 13
      ((0.65, 1.0, 0.4), pushrand),
      ((0.33, 0.9, 0.3), pushrand),
      ((0.16, 0.8, 0.4), flashWhite),
      ((0.55, 0.8, 0.4), pushrand)]),
    ((12, 14), [((0.0, 0.75, 0.5), pushrand), #Dec 14
      ((0.65, 1.0, 0.4), pushrand),
      ((0.33, 0.9, 0.3), pushrand),
      ((0.16, 0.8, 0.4), pushrand),
      ((0.55, 0.8, 0.4), flashWhite)]),
    ((-1, -1), [((0.0, 0.75, 0.5), pushrand),
      ((0.65, 1.0, 0.4), baseAndWhite),
      ((0.33, 0.9, 0.3), pushrand),
      ((0.16, 0.8, 0.4), pushrand),
      ((0.55, 0.8, 0.8), slowFadeToWhite)])
    ]

  def __init__(self):
    clockPin = Pin(5, Pin.OUT)
    dataPin = Pin(4, Pin.OUT)

    self.currentConfiguration = None
    self.cycleCount = 0
    self.ledStrip = APA102(clockPin, dataPin, 40)
    self.rings = []
    for ringId in range(0, 5):
      self.rings.append(APA102Ring(self.ledStrip, ringId * 8, 8))

    self.rings[0].setBaseHSV((0.0, 0.75, 0.5))
    self.rings[1].setBaseHSV((0.5, 0.5, 0.8))
    self.rings[2].setBaseHSV((0.7, 0.5, 0.3))
    self.rings[3].setBaseHSV((0.2, 0.2, 0.4))
    self.rings[4].setBaseHSV((0.8, 0.8, 0.8))

    self.readingTimer = Timer(-1)

    self.runTimer()

  def status(self, status):
    self.rings[0].set(status, (255, 0, 0))
    self.rings[0].write()
    self.rings[0].write()

  def initialize(self, now):
    hour = now[3]
    brightness = 5

    if 9 <= hour <= 16:
      brightness = 20
    elif 6 <= hour <= 19:
      brightness = 10

    print("Brightness: {}".format(brightness))

    for config in PictureFrame.configurations:
      configDate = config[0]

      if (now[1] == configDate[0] or configDate[0] == -1) and (now[2] == configDate[1] or configDate[1] == -1):
        self.currentConfiguration = config
        break

    if self.currentConfiguration is not None:
      for ringIndex in range(0, len(self.rings)):
        ring = self.rings[ringIndex]
        ring.brightness = brightness
        baseHSV = self.currentConfiguration[1][ringIndex][0]

        ring.setBaseHSV(baseHSV)

      return self.currentConfiguration

  def runTimer(self):
    self.readingTimer.init(period=150, mode=Timer.PERIODIC, callback=self.timerCallback)

  def timerCallback(self, timer):
    anyAnimation = False
    for r in self.rings:
      anyAnimation = r.animate() or anyAnimation
    self.rings[0].write()

    if not anyAnimation:
      self.cycleRings()

  def cycleRings(self):
    self.cycleCount = self.cycleCount + 1

    if self.currentConfiguration is None:
      return False

    for ringIndex in range(0, len(self.rings)):
      ring = self.rings[ringIndex]
      fn = self.currentConfiguration[1][ringIndex][1]
      fn(self.cycleCount, ringIndex, ring)

    self.rings[0].write()

    return True

  def pushRandomColor(self):
    for r in self.rings:
      PictureFrame.pushrand(r)
