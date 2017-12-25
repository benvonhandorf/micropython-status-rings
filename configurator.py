import json
import network
import ntptime

class Configurator:
  def __init__(self):
    with open("config.json") as cfgFile:
      self.config = json.load(cfgFile)

  def configureNetwork(self):
    if hasattr(self, "wlan") and self.wlan is not None and self.wlan.isconnected():
      ntptime.settime()
      return self.wlan.isconnected()

    if not hasattr(self, "wlan") or self.wlan is None:
      self.wlan = network.WLAN(network.STA_IF) # create station interface

    if not hasattr(self, "ap") or self.ap is None:
      self.ap = network.WLAN(network.AP_IF) # create station interface

    self.ap.active(False)
    self.wlan.active(True)       # activate the interface
    availableNetworks = self.wlan.scan()             # scan for access points

    if self.config["networks"] is not None:

      print("Available networks {0}".format(availableNetworks))
      for availNetwork in availableNetworks:
        if not self.wlan.isconnected():
          for configuredNetwork in self.config["networks"]:
            if not self.wlan.isconnected() and configuredNetwork["ssid"].lower() == availNetwork[0].decode("utf-8").lower():
              print("Attempting connection to network {0}".format(configuredNetwork["ssid"]))
              self.wlan.connect(configuredNetwork["ssid"], configuredNetwork["psk"])
              break
    else:
      print("No networks are configured")

    if self.wlan.isconnected():
      ntptime.settime()
      
    return self.wlan.isconnected()

  def __getitem__(self, key):
    return self.config[key]


