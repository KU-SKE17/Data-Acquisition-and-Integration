import imu
import time

while True:
    imu.update()  # read data from sensor
    acc = imu.acc  # array of (x, y, z, total)
    mag = imu.mag  # array of (x, y, z)
    print("Acceleration:", acc)
    print("Compass:", mag)
    time.sleep(1)