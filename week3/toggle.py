from machine import Pin
from time import sleep, sleep_ms

red_led = Pin(2, Pin.OUT)
sw1 = Pin(16, Pin.IN)

# while True:
#     # wait to pressed
#     while sw1.value() != 0:
#         continue

#     # toggle led
#     if red_led.value() == 1:
#         red_led.value(0)
#     else:
#         red_led.value(1)

#     # wait to released
#     while sw1.value() == 0:
#         sleep(0.1)

# Ans
while True:
    # wait to pressed
    while sw1.value() == 1:
        pass
    sleep_ms(100)

    # toggle led
    red_led.value(1 - red_led.value())

    # wait to released
    while sw1.value() == 0:
        pass
    sleep_ms(100)
