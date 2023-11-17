import logging

from adafruit_servokit import ServoKit
from adafruit_servokit import Servo as AdafruitServo

logger = logging.getLogger(__name__)


class Servo:
    """
    A container for a servo object.
    """

    def __init__(
        self,
        id_: int,
        servo: AdafruitServo,
        actuation_range: tuple[int, int] = (0, 180),
    ):
        """
        Initialize the servo.

        Arguments:
            id_: An identifier for the servo.
            servo: The Adafruit servo object.
            actuation_range: The range of angles the servo can be set to.
        """
        self.id = id
        self.servo = servo
        servo.actuation_range = actuation_range
        logger.debug(
            "Instantiated servo %s with activation range %s", self.id, actuation_range
        )

    def set(self, angle: int):
        """
        Set the angle of the servo.
        """
        self.servo.angle = angle
        logger.debug("Set angle of servo %s to %sdeg", self.id, angle)

    def current_angle(self) -> float:
        return self.servo.angle

    class InvalidAngle(Exception):
        """
        An exception for when an invalid angle is given to a servo.
        """

        def __init__(self, angle: int, servo: "Servo"):
            self.angle = angle
            self.servo = servo
            super().__init__(f"Angle {angle} is invalid for servo {servo}")


class Servos:
    def __init__(
        self,
        active_angle: int,
        neutral_angle: int,
        connections: list[int],
        address: int,
        actuation_range: tuple[int, int] = (0, 180),
    ):
        """
        A class to represent all servos connected to the bot.

        Attributes:
            active_angle: The angle the servo should be at when toggled.
            neutral_angle: The angle the servo should be at rest.
            connections: A list of the pins the servos are connected to. For example, if
                the servos are connected to pins 0, 1, and 2, then connections should be
                [0, 1, 2].
            address: The address of the servo hat. This is a hexadecimal number.
            actuation_range: The range of angles the servo can be set to.
        """
        self.kit = ServoKit(channels=16, address=address)
        self.active_angle = active_angle
        self.neutral_angle = neutral_angle
        self.actuation_range = actuation_range

        # Map ports servos are connected to to servo instances, and if there are any
        # invalid mappings throw an exception.
        self.servos = {}
        for i in connections:
            if i > 15:
                raise self.ServoDoesntExist(
                    f"Port for servo {i} doesn't exist. The maximum servo port is 15."
                )
            if i in self.servos:
                raise ValueError(
                    f"Servo {i} already docked. Current servos are {self.servos.keys()}"
                )
            self.servos[i] = Servo(id_=i, servo=self.kit.servo[i])
            logger.debug("Connected servo %s to respective port", i)

    async def toggle_servo(self, servo: int, angle: int = None):
        """
        Toggle a servo between the active angle and the neutral angle.
        """
        # If the servo is not a valid servo that is connected throw an error
        if servo not in self.servos:
            raise self.ServoDoesntExist(
                f"Servo {servo} not docked. Current servos are {self.servos.keys()}"
            )

        # If the user did not set an angle then toggle the servo to its opposite state. If
        # it is neither in a neutral state nor a toggled state then switch the servo to a
        # neutral state.
        if angle is None:
            if self.servos[servo].servo.angle == self.neutral_angle:
                angle = self.active_angle
            else:
                if self.servos[servo].servo.angle != self.active_angle:
                    logger.warning(
                        "Servo was in a custom angle state and was toggled. Resetting to "
                        "default neutral state."
                    )
                angle = self.neutral_angle

        # If the angle that the servo is to be moved to is not valid throw an error
        if angle < self.actuation_range[0] or angle > self.actuation_range[1]:
            raise Servo.InvalidAngle(angle, self.servos[servo])

        logger.info("Set servo %s to angle %sdeg", servo, angle)
        self.servos[servo].set(angle)

    class ServoDoesntExist(Exception):
        """An exception for trying to manipulate a servo that does not exist."""

    class PortDoesntExist(Exception):
        """An exception for trying to use a port that has nothing attached to it."""
