# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()

import network
import time
import max7219
from machine import Pin, SPI
from micropyserver import MicroPyServer
import utils
import ujson

# WiFi Details
ssid = "Change This"
password = "Change This"

# Setup Display
## Grey - DIN - D2 - 5
## Purp - CS - D3 - 6
## Blue - CLK - D4 - 7
data = 5
load = 6
clk = 7
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(clk), mosi=Pin(data))
ss = Pin(load, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 8)
display.brightness(1)

def clearScreen():
    display.fill(0)
    display.show()

def msgPrint(message):
    clearScreen()
    display.text(message,0,0,1)
    display.show()

def msgScroll(message: str, repeat: int, speed=0.04):
    clearScreen()
    length = len(message)
    column = (length * 8)
    rep = repeat
    while rep > 0:
        rep -= 1
        for m in range(64, -column, -1):
            display.fill(0)
            display.text(message ,m,0,1)
            display.show()
            time.sleep(speed)

# Setup Network
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(ssid, password)
if not nic.isconnected():
    print('WiFi connection has failed.')
    msgPrint("Offline")
else:
    conn_state = nic.ifconfig()
    print('Wifi connected at ' + conn_state[0])
    msgScroll(nic.ifconfig()[0], 2)

def default(request):
    server.send("HTTP/1.0 200 OK\r\n")
    msgPrint(" SPACEX")

def msg_handler(request):
    if (utils.get_request_method(request), "POST"):
        req = utils.get_request_post_params(request)
        jd = ujson.loads(ujson.dumps(req))
        try:
            message = jd['message']
        except:
            server.send("HTTP/1.0 400 OK\r\n")
        try:
            brightness = int(jd['brightness'])
        except:
            brightness = 1
        try:
            scroll = eval(jd['scroll'])
        except:
            scroll = True
        try:
            repeat = int(jd['repeat'])
        except:
            repeat = 1
        try:
            speed = float(jd['speed'])
        except:
            speed = 0.03
        display.brightness(brightness)
        if (scroll):
            msgScroll(message, repeat, speed)
        else:
            msgPrint(message)
        server.send("HTTP/1.0 200 OK\r\n")


server = MicroPyServer(host="0.0.0.0", port=80)
server.add_route("/", default)
server.add_route("/message", msg_handler, method="POST")
server.start()
