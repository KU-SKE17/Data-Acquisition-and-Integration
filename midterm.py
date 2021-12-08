from machine import Pin, Timer, PWM
from umqtt.robust import MQTTClient
from config import WIFI_SSID, WIFI_PASS
from time import sleep_ms
import uasyncio as asyncio
import network

HOST = "iot.cpe.ku.ac.th"
TOPIC1 = "daq2021/midterm/6210545505/blink"
TOPIC2 = "daq2021/midterm/6210545505/count"

led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)  # off
sw2 = Pin(14, Pin.IN)


def sub_callback(topic, payload):
    if topic == TOPIC1.encode():
        try:
            if int(payload) in range(1, 11):
                led_iot.value(0)  # turn LED on
                sleep_ms(250)
                led_iot.value(1)  # turn LED off
                sleep_ms(750)

        except ValueError:
            print("ValueError!")


# connect Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    sleep_ms(500)
    print("connecting...")
led_wifi.value(0)
print("connected!")

# initial mqtt
mqtt1 = MQTTClient(TOPIC1, HOST)
mqtt1.connect()
mqtt2 = MQTTClient(TOPIC2, HOST)
mqtt2.connect()

# subscribe
mqtt1.set_callback(sub_callback)
mqtt1.subscribe(TOPIC1.encode())


async def check_mqtt():
    while True:
        mqtt1.check_msg()
        await asyncio.sleep_ms(0)


async def check_switch():
    count = 0
    while True:
        # wait until sw2 is pressed
        while sw2.value() == 1:
            await asyncio.sleep_ms(0)

        # pub count
        count += 1
        mqtt2.publish(TOPIC2, str(count))

        # wait until sw2 is released
        while sw2.value() == 0:
            await asyncio.sleep_ms(0)


# create and run coroutines
loop = asyncio.get_event_loop()
loop.create_task(check_mqtt())
loop.create_task(check_switch())
loop.run_forever()