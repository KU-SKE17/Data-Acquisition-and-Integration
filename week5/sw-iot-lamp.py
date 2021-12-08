from machine import Pin, Timer, PWM
from umqtt.robust import MQTTClient
from config import WIFI_SSID, WIFI_PASS
from time import sleep
import uasyncio as asyncio
import network

HOST = "iot.cpe.ku.ac.th"
TOPIC = "ku/daq2021/6210545505/lamp/2"

led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)  # off
lamp = PWM(Pin(25), freq=5000)
sw1 = Pin(16, Pin.IN)


def switch_lamp_on():
    lamp.duty(0)


def switch_lamp_off():
    lamp.duty(1023)


def sub_callback(topic, payload):
    if topic == TOPIC.encode():
        try:
            if int(payload) == 0:
                switch_lamp_off()
            if int(payload) == 1:
                switch_lamp_on()
        except ValueError:
            print("ValueError!")


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
mqtt = MQTTClient(TOPIC, HOST)
mqtt.connect()
led_iot.value(0)

# subscribe
mqtt.set_callback(sub_callback)
mqtt.subscribe(TOPIC.encode())


async def check_mqtt():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)


async def check_switch():
    while True:
        # wait until sw is pressed
        while sw1.value() == 1:
            await asyncio.sleep_ms(0)

        # toggle LED
        if lamp.duty() == 1023:
            switch_lamp_on()
            mqtt.publish(TOPIC, "{}".format(1))
        else:
            switch_lamp_off()
            mqtt.publish(TOPIC, '0')

        # wait until sw1 is released
        while sw1.value() == 0:
            await asyncio.sleep_ms(0)


# create and run coroutines
loop = asyncio.get_event_loop()
loop.create_task(check_mqtt())
loop.create_task(check_switch())
loop.run_forever()