import time
import kidbright as kb

kb.init()
while True:
    kb.matrix.fill(0)  # clear the framebuffer
    kb.matrix.text(str(kb.temperature()), 0, 0)
    kb.matrix.show()
    time.sleep(1)