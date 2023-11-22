from time import sleep, time

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

startTime = time()

while time() < startTime + 5:
	kit.stepper1.onestep(
		style=stepper.DOUBLE,
		direction=stepper.BACKWARD if time() < startTime + 2.5 else stepper.FORWARD
	)

