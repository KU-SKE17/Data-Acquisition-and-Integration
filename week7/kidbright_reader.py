import time
import kidbright as kb

kb.init()
while True:
    print("light = {}, temperature = {}".format(kb.light(), kb.temperature()))
    time.sleep(1)