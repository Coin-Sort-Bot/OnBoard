from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16, address=1)

for i in range(16):
    kit.servo[i].angle = 0
    for ang in range(180):
        kit.servo[i].angle = ang
        sleep(0.05)
    kit.servo[i].angle = 0
    sleep(.1)

