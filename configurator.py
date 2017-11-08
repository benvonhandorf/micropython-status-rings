import json
import network

class Configurator:
  def configure(self):
    if hasattr(self, "wlan") and self.wlan is not None and self.wlan.isconnected():
      return

    if not hasattr(self, "wlan") or self.wlan is None:
      self.wlan = network.WLAN(network.STA_IF) # create station interface

    self.wlan.active(True)       # activate the interface
    availableNetworks = self.wlan.scan()             # scan for access points

    with open("config.json") as cfgFile:
      self.config = json.load(cfgFile)

    if self.config["networks"] is not None:
      for availNetwork in availableNetworks:
        if self.wlan.isconnected():
          for configuredNetwork in self.config["networks"]:
            if not self.wlan.isconnected() and configuredNetwork["ssid"].lower() == availNetwork[0].decode("utf-8").lower:
              print("Attempting connection to network {0}".format(configuredNetwork["ssid"]))
              self.wlan.connect(configuredNetwork["ssid"], configuredNetwork["psk"])
              break

  def __getitem__(self, key):
    return self.config[key]


