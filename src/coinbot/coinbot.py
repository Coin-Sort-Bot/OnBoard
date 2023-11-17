from src.coinbot.hardware.motor import Motor
from src.coinbot.hardware.servos import Servos


class CoinBot:
    """
    The main interface for the coin sorting bot.

    attributes:
        servos: Instance of Servos class containing all servos connected to bot.
        motor: Instance of Motor class containing the motor connected to bot.
    """

    def __init__(self):
        self.servos = Servos(
            active_angle=150,
            neutral_angle=0,
            connections=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            address=0x41,
        )
        self.motor = Motor(
            port=1,
            address=0x40,
        )
