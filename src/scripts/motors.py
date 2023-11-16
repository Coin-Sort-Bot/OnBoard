from time import sleep

from adafruit_motorkit import MotorKit

kit = MotorKit()

kit.motor1.throttle = 0.0
kit.motor1.throttle = 1.0
sleep(5)
kit.motor1.throttle = 0.0
kit.motor1.throttle = -1.0
sleep(5)

for i in range(100):
    kit.motor1.throttle = i/100
    sleep(.1)

