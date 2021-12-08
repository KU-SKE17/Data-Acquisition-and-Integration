from config import WIFI_SSID, WIFI_PASS
from umqtt.robust import MQTTClient
from machine import Pin
from time import sleep
import kidbright as kb
import network
import json

led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)  # off

BROKER = "iot.cpe.ku.ac.th"
UNIQUE_ID = "ku/daq2021/6210545505/sensors"

# connect Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    sleep(0.5)
    print("connecting...")
led_wifi.value(0)
print("connected!")

# initial mqtt
mqtt = MQTTClient(UNIQUE_ID, BROKER)
mqtt.connect()
led_iot.value(0)

kb.init()
while True:
    data = {
        "light": kb.light(),
        "temperature": kb.temperature()
    }
    mqtt.publish(UNIQUE_ID, json.dumps(data))
    sleep(10)