from time import sleep, time

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

#for i in range(100):
#	kit.stepper1.onestep()
#	sleep(.1

startTime = time()

while time() < startTime + 5:
	kit.stepper1.onestep(
		style=stepper.DOUBLE,
		direction=stepper.BACKWARD if time() < startTime + 2.5 else stepper.FORWARD
	)

