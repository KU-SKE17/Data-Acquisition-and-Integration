from machine import Timer, Pin
import time

led_red = Pin(2, Pin.OUT)
led_green = Pin(12, Pin.OUT)
sw1 = Pin(16, Pin.IN, Pin.PULL_UP)


def blink1(timer):
    led_red.value(0)  # turn LED on
    timer.init(period=100, mode=Timer.ONE_SHOT, callback=blink2)


def blink2(timer):
    led_red.value(1)  # turn LED off
    timer.init(period=1900, mode=Timer.ONE_SHOT, callback=blink1)


def switch_pressed(pin):
    # time.sleep_ms(10) -> block! don't do this
    led_green.value(1 - led_green.value())


# use Timer for corn #0
timer = Timer(0)

blink1(timer)
sw1.irq(trigger=Pin.IRQ_FALLING, handler=switch_pressed)

while True:
    time.sleep(1)
