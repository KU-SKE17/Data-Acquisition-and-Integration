from machine import Pin, ADC, PWM
from time import sleep

ain = ADC(Pin(36))
light_lamp = PWM(Pin(25), freq=5000)

# while True:
#     light_lamp.duty(4095 - ain.read())

# """
# explanation:
#     ain.read() can refer to the brightness from light senser its value is 0-4095, 0 mean it is actually dark and 4095 is mean to be brightest sunlight (my room could reach only ≈2200-2800)

#     since light_lamp.duty() can be set 0-1023, and if we set the value more than 1023 it will use only 1023 automatically. (0 mean to turn on brightest, 1023 mean to turn off)

#     so my code is to set light_lamp.duty() according to the 4095-ain.read(), so
#     if ain.read() == 0 (dark) -> lamp turn brightest on
#     if ain.read() in range(1, 3072) -> lamp turn on (get surrounding)
#     if ain.read() in range(3072, 4096) -> lamp turn off
# """


class LinearInterpolation:
    def __init__(self, x0, x1, y0, y1, clip=True):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.clip = clip

    def map(self, x):
        if self.clip:
            x = max(x, self.x0)
            x = min(x, self.x1)
        return (x - self.x0) / (self.x1 - self.x0) * (self.y1 - self.y0) + self.y0


"""
>>> lerp = LinearInterpolation(30,50,20,10)
>>> lerp.map(30)
20.0
>>> lerp.map(50)
10.0
>>> lerp.map(40)
15.0
"""
