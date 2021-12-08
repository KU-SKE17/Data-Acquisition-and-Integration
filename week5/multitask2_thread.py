from machine import Timer, Pin
import time
import _thread

led_red = Pin(2, Pin.OUT)
led_green = Pin(12, Pin.OUT)
sw1 = Pin(16, Pin.IN, Pin.PULL_UP)


# Thread 1
def blink_led():
    while True:
        led_red.value(0)
        time.sleep_ms(100)
        led_red.value(1)
        time.sleep_ms(1900)


# Thread 2
def switch_toggle():
    while True:
        # wait until sw is pressed
        while sw1.value() == 1:
            pass

        # toggle LED
        led_green.value(1 - led_green.value())

        # wait until sw1 is released
        while sw1.value() == 0:
            pass


# create and run threads
_thread.start_new_thread(blink_led, [])
_thread.start_new_thread(switch_toggle, [])

while True:
    time.sleep(1)