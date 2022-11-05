#boot.py -- run on boot-up
import network
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('Connecting to Network...')
    sta_if.active(True)
    sta_if.connect('Network ID', 'Password')
    while not sta_if.isconnected():
        pass
print('Network Config:', sta_if.ifconfig())
