from .hardware.cameras import Cameras
from .hardware.motor import Motor
from .hardware.servos import Servos


class CoinBot:
    """
    The main interface for the coin sorting bot.

    attributes:
        servos: Instance of Servos class containing all servos connected to bot.
        motor: Instance of Motor class containing the motor connected to bot.
    """

    def __init__(self, servos: bool = True, motor: bool = True, cameras: bool = True):
        """
        Initialize the CoinBot class.
        """
        self.servos = None
        self.motor = None
        self.cameras = None

    async def setup(self, servos: bool = True, motor: bool = True, cameras: bool = True):
        if servos:
            self._setup_servos()

        if motor:
            self._setup_motor()

        if cameras:
            self._setup_cameras()

    def _setup_servos(self):
        """
        Setup the servos.
        """
        self.servos = Servos(
            active_angle=150,
            neutral_angle=0,
            connections=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            address=0x41,
        )

    def _setup_motor(self):
        """
        Setup the motor.
        """
        self.motor = Motor(
            port=1,
            released=True,
            address=0x60,
        )

    def _setup_cameras(self):
        """
        Setup the cameras.
        """
        self.cameras = Cameras()
        self.cameras.mount()
