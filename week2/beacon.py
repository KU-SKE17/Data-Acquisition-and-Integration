from machine import Pin
from time import sleep
 
led = Pin(12, Pin.OUT)

while True:
    print("Turning IoT LED on for 0.1 seconds...")
    led.value(0)
    sleep(0.1)
    print("Turning IoT LED off for 0.9 seconds...")
    led.value(1)
    sleep(0.9)
