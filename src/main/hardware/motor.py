import asyncio
import logging
from time import time
from typing import Literal

from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

logger = logging.getLogger(__name__)


motor_timeout_duration = 60 * 5


class Motor:
    """
    The central motor of the coinbot.
    """

    def __init__(
        self,
        address: int,
        port: int,
        released: bool,
        auto_unlock: bool = True,
        auto_unlock_duration: float = motor_timeout_duration
    ):
        """
        Initialize the motor.

        Arguments:
            address: The address of the motor hat. This is a hexadecimal number.
            port: The port the motor is connected to. Either 0 or 1 depending on the port
                the stepper motor is plugged in to.
            released: Whether to start the motor in released position.
            auto_unlock: Whether to automatically unlock the motor after a certain amount
                of time. Defaults to True.
            auto_unlock_duration: How long to wait before automatically unlocking the
                motor. Defaults to motor_timeout_duration, which is 5 minutes by default.
        """
        self._ongoing_active_timeout = None
        self._locked = None
        self._spinning_task = None
        self._auto_unlock = auto_unlock
        self._auto_unlock_duration = auto_unlock_duration
        self.kit = MotorKit(address=address)

        # Assign the motor port based on its address
        if address not in (0, 1):
            raise ValueError(
                f"Address {port} is invalid. The address must be either 0 or 1."
            )
        self.motor = getattr(self.kit, f"stepper{address}")

        # Set the initial lock state of the motor
        if released:
            self.release_motor()
        else:
            self.lock_motor()

    @property
    def locked(self):
        return self._locked

    async def set_active_timeout(
        self, duration: float = None, unlock: bool = None
    ):
        """
        Set a timeout to check and automatically unlock the motor if it is locked for
        too long to prevent overheating.

        Arguments:
            duration: How long to wait before checking locked status.
            unlock: Whether to unlock at the end of the interval (True) or just warn
                (False). Defaults to setting set at initialization of Servos.
        """
        # Use defaults set at initialization if no value is given
        if duration is None:
            duration = self._auto_unlock_duration
        if unlock is None:
            unlock = self._auto_unlock

        async def _active_timeout():
            await asyncio.sleep(duration)
            # Warn the user if the motor is currently locked after the timeout
            if self._locked:
                logger.warning(
                    "Motor has been in locked position for %s seconds",
                    duration
                )
            # Unlock the motor if it is locked and the user has set auto_unlock to True
            if unlock:
                await self.release_motor()

        if self._ongoing_active_timeout is not None:
            self._ongoing_active_timeout.cancel()
        self._ongoing_active_timeout = asyncio.create_task(_active_timeout())

    async def lock_motor(self, step_motor: bool = True):
        """Lock the motor so that it stays in place."""
        if step_motor:
            self.motor.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
            self.motor.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        self._locked = True
        await self.set_active_timeout()
        logger.info("Locked motor position")

    async def release_motor(self):
        """Release the motor to let it freely spin without consuming power."""
        self.motor.release_motor()
        self._locked = False
        logger.info("Released motor")

    async def step_motor(
        self,
        style: stepper.SINGLE
        | stepper.DOUBLE
        | stepper.MICROSTEP
        | stepper.INTERLEAVE = stepper.SINGLE,
        direction: stepper.FORWARD
        | stepper.BACKWARD
        | Literal["forward"]
        | Literal["backward"] = stepper.FORWARD,
        then_release: bool = False,
    ):
        """
        Step the motor forward or backward.

        Style: The style of step.
        Direction: The direction to step in.
        """
        await self.lock_motor()

        # If direction was set to a string, convert it to the appropriate stepper value
        if direction == "forward":
            direction = stepper.FORWARD
        elif direction == "backward":
            direction = stepper.BACKWARD

        self.motor.onestep(direction=direction, style=style)

        if then_release:
            await self.release_motor()

        logger.debug("Stepped motor forward")

    async def start_spinning(self, speed: float, duration: float = None):
        """
        Begin spinning the motor.

        Arguments:
            speed: The speed to spin the motor at. Negative values spin the motor
                counterclockwise, positive values spin the motor clockwise. This value
                should be between -100 and 100.
            duration: The amount of time to spin the motor for. If None, the motor will
                spin until stop_spinning is called. No matter what, the motor will stop
                spinning if stop_spinning is called.
        """
        if speed == 0:
            await self.stop_spinning()
            await self.lock_motor()

        sleep_amount = 1 - ((abs(speed) - 100) / 100)
        logger.debug("Sleep amount between steps set to %ss", sleep_amount)

        # Create a task to spin the motor in the background at the given speed.
        async def _spin():
            await self.lock_motor(step_motor=False)
            end = time() + duration if duration is not None else float("inf")
            while time() < end:
                await self.step_motor(
                    direction=stepper.FORWARD if speed > 0 else stepper.BACKWARD
                )
                await asyncio.sleep(sleep_amount)

        # If the motor is already spinning swap the current spin task with a new one with
        # the new speed.
        if self._spinning_task is not None:
            self._spinning_task.cancel()
        self._spinning_task = asyncio.create_task(_spin())
        logger.info("Beginning to spin motor at speed %s", speed)

    async def stop_spinning(self, release=False):
        """
        Stop the motor from spinning.

        Arguments:
            release: Whether to release the motor. If True, the motor will be released
                and will not hold its position. If False, the motor will hold its
                position.
        """
        if self._spinning_task is not None:
            self._spinning_task.cancel()
            self._spinning_task = None
            logger.info("Stopping motor from spinning")
        if release:
            self.motor.release()
