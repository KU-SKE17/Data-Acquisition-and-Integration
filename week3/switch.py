from machine import Pin
from time import sleep

red_led = Pin(2, Pin.OUT)
sw1 = Pin(16, Pin.IN)

while True:
    red_led.value(sw1.value())
