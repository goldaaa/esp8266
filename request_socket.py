__author__ = "navid nasiri"
__github__ = "https://github.com/esp8266"
__gmail__ = "goldaaa.program@gmail.com"

import time
import network

class Wifi():
    def __init__(self, name):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.config(dhcp_hostname=name)

    def scan(self):
        return self.sta_if.scan()

    def isconnected(self):
        return self.sta_if.isconnected()

    def connect(self, essid, password, timeout=30000):
        self.sta_if.active(True)
        if not self.sta_if.isconnected():
            print("Connecting to WiFi network...")
            self.sta_if.connect(essid, password)
            t = time.ticks_ms()
            while not self.sta_if.isconnected():
                if time.ticks_diff(time.ticks_ms(), t) > timeout:
                    self.sta_if.disconnect()
                    print("Timeout. Could not connect.")
                    return False
            print("Successfully connected to " + essid)
            return True
        else:
            print("Already connected")
            return True

    def disconnect(self):
        self.sta_if.disconnect()

    def ipaddress(self):
        ip, subnetmask, gateway, dns = self.sta_if.ifconfig()
        return ip


class Hotspot:
    def __init__(self):
        self.ap_if = network.WLAN(network.AP_IF)

    def connect(self, essid, password):
        self.ap_if.active(True)
        self.ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

    def disconnect(self):
        self.ap_if.active(False)

    def ipaddress(self):
        ip, subnetmask, gateway, dns = self.ap_if.ifconfig()
        return ip, subnetmask, gateway, dns

#hotspot = Hotspot()
#hotspot.connect(essid="TP-Navid", password="123456789")
#hotspot.disconnect()

#wifi = Wifi("TestWifi")
#print(wifi.scan())
#print(wifi.isconnected())
#wifi.connect('navid', "'goldman&*****'")
#wifi.disconnect()
#print(wifi.ipaddress())


from machine import Pin
from time import sleep
def ControlePin(pin):
    try:
        if 'open' in pin:
            pin = int(pin.split('+')[1])
            print(pin)
            led = Pin(pin, Pin.OUT)
            led.value(1)
        elif 'close' in pin:
            pin = int(pin.split('+')[1])
            print(pin)
            led = Pin(pin, Pin.OUT)
            led.value(0)
        else:
            pin = int(pin)
            led = Pin(pin, Pin.OUT)
            led.value(not led.value())
    except:
        pass

def LoopControlePin(pin):
    led = Pin(pin, Pin.OUT)
    while True:
      led.value(not led.value())
      sleep(0.5)

#ControlePin(pin=16)
#LoopControlePin(pin=16)

try:
  import usocket as socket
except:
  import socket
import esp
esp.osdebug(None)
class Server:
    def run(self, ip='192.168.4.1', port=8266):
        hotspot = Hotspot()
        hotspot.connect(essid="TP-SERVER", password="123456789")
        # hotspot.ifconfig((ip, '255.255.255.0', ip, ip))
        print(hotspot.ipaddress())

        s = socket.socket()
        s.bind(('', port))
        s.listen(5)
        cliente, a = s.accept()

        while True:
            request = cliente.recv(8).decode('utf-8')
            print(request)
            ControlePin(pin=request)

server = Server()
server.run()
