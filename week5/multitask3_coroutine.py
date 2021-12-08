from machine import Pin
import uasyncio as asyncio

led_red = Pin(2, Pin.OUT)
led_green = Pin(12, Pin.OUT)
sw1 = Pin(16, Pin.IN, Pin.PULL_UP)


# Coroutine #1
async def blink_led():
    while True:
        led_red.value(0)
        await asyncio.sleep_ms(100)
        led_red.value(1)
        await asyncio.sleep_ms(1900)


# Coroutine #2
async def switch_toggle():
    while True:
        # wait until sw is pressed
        while sw1.value() == 1:
            await asyncio.sleep_ms(0)

        # toggle LED
        led_green.value(1 - led_green.value())

        # wait until sw1 is released
        while sw1.value() == 0:
            await asyncio.sleep_ms(0)


# create and run coroutines
loop = asyncio.get_event_loop()
loop.create_task(blink_led())
loop.create_task(switch_toggle())
loop.run_forever()