import configurator
import status_light

configurator = configurator.Configurator()
statusLight = status_light.StatusLight()

def main():
  statusLight.initializing(0)

  print("Configuring...")
  configurator.configure()
  print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  while not configurator.wlan.isconnected():
    print("Configuring...")
    configurator.configure()
    print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  statusLight.initializing(3)

  if configurator.wlan.isconnected():
    statusLight.setup(configurator["mqttServerIp"], configurator["mqttTopic"])
    statusLight.main()

if __name__ == "__main__":
  main()  