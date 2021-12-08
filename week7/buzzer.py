import buzzer
import time

# make a tone of 1500 Hz for 1/2 second, blocking
buzzer.tone(freq=1500, duration=0.5)

# turn on the buzzer with 2000 Hz generated; wait 1 second; then turn it off
buzzer.on(freq=2000)
time.sleep(1)
buzzer.off()

# play some musical notes
buzzer.note("C4 C4 G4 G4 A4 A4 G4", duration=1)