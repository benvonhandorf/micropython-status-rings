import configurator
import pictureframe
import machine
from machine import Timer
import time
import os

def clean():
  os.remove("main.py")

configurator = configurator.Configurator()
frame = pictureframe.PictureFrame()
rareTimer = Timer(-1)

def initializeFrame(timer):
  if not configurator.wlan.isconnected():
    print("Attempting network configuration")
    configurator.configureNetwork()

  now = time.localtime()

  frame.initialize(now)  

def main():
  print("Configuring...")
  frame.status(8)

  configurationAttempts = 8
  
  while not configurator.configureNetwork() and configurationAttempts > 0:
    machine.idle()
    time.sleep(5)
    machine.idle()
    print("Configuring... {}".format(configurationAttempts))
    configurationAttempts = configurationAttempts - 1
    frame.status(configurationAttempts)

  print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  frame.status(2)

  initializeFrame(None)

  rareTimer.init(period=1000*60*60, mode=Timer.PERIODIC, callback=initializeFrame)

if __name__ == "__main__":
  main()  