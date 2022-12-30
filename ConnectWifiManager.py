import network
import uasyncio
from network import WLAN

"""
ConnectWifiManager manages the connection to the wifi, using the network SDK for implementation
Uses a unique static var, in order to always has a only session for the internet connection
Should use uasyncio to run their methods
"""
class ConnectWifiManager:

    ## PROPERTIES
    wlanManager=WLAN(network.STA_IF)
    
    ## PUBLIC METHODS
    async def connectToInternet(self, ssid_name,
                                ssid_pass):
        await uasyncio.create_task(self.__processRequest(ssid_name,
                                                         ssid_pass))
    
    def isConnected(self):
        return ConnectWifiManager.wlanManager.isconnected()

        ## OWN METHODS
    async def __processRequest(self, ssid_name,
                               ssid_pass):
        print("Connectig...")
        if ConnectWifiManager.wlanManager.isconnected():
            print("Success connection to: " + ssid_name + " ...")
            return
        ConnectWifiManager.wlanManager.active(True)
        ConnectWifiManager.wlanManager.connect(ssid_name, ssid_pass)
        while not ConnectWifiManager.wlanManager.isconnected():
            pass
        print("Success connection to: " + ssid_name + " ...")
        return