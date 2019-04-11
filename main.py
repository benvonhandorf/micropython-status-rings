import configurator
import status_light
import machine
import time
import os

configurator = configurator.Configurator()

brightnessReduction = configurator["brightnessReduction"] or 0

statusLight = status_light.StatusLight(configurator["segments"], brightnessReduction)

def main():
  statusLight.initializing(0)

  print("Configuring...")
  
  while not configurator.configureNetwork():
    machine.idle()
    time.sleep(1)
    machine.idle()
    print("Configuring...")

  print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  statusLight.initializing(3)

  if configurator.wlan.isconnected():
    print("status light configuration {0} {1}".format(configurator["mqttServerIp"], configurator["mqttTopic"]))
    statusLight.setup(configurator["mqttServerIp"], configurator["mqttUser"], configurator["mqttPassword"], configurator["mqttTopic"])
    statusLight.main()

def restore() :
  os.rename("main_store.py", "main.py")
  print("Restoring main.py")
  machine.reset()

if __name__ == "__main__":
  skipBootPin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
  if(skipBootPin.value() == 0):
    os.rename("main.py", "main_store.py")
    print("Skipping initialization")
  else:
    main()  
