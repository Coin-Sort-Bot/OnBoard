from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)

kit.servo[0].angle = 0
sleep(1)
kit.servo[0].angle = 40
sleep(1)
kit.servo[0].angle = 0
