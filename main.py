import configurator
import status_light
import machine
import time

configurator = configurator.Configurator()
statusLight = status_light.StatusLight(configurator["segments"])

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
    statusLight.setup(configurator["mqttServerIp"], configurator["mqttTopic"])
    statusLight.main()

if __name__ == "__main__":
  main()  