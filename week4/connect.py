from machine import Pin, ADC, PWM
from time import sleep
import network
from config import WIFI_SSID, WIFI_PASS
from umqtt.robust import MQTTClient

ldr = ADC(Pin(36))
led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)  # off

BROKER = "iot.cpe.ku.ac.th"
UNIQUE_ID = "ku/cpe/6210545505/light"

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

# # publish
# while True:
#     light = ldr.read()
#     print("Light value:", light)
#     mqtt.publish(UNIQUE_ID, str(light))
#     sleep(2)


# subscribe
def sub_callback(topic, payload):
    if topic == UNIQUE_ID.encode():
        try:
            print(payload)  # bytes
        except ValueError:
            print("ValueError!")


mqtt.set_callback(sub_callback)
mqtt.subscribe(UNIQUE_ID.encode())
while True:
    mqtt.check_msg()
