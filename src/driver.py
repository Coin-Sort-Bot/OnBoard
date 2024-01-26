import asyncio

from main.coinbot import CoinBot
import logging

logging.basicConfig(level=logging.DEBUG)

async def main():
    coinbot = CoinBot()

    await coinbot.cameras.camera1.capture()

    # await coinbot.motor.start_spinning(100)
    # await asyncio.sleep(2)
    # await coinbot.motor.start_spinning(-100)
    # await asyncio.sleep(2)
    # await coinbot.motor.stop_spinning()
    #
    # await coinbot.servos.toggle_servos()
    # await asyncio.sleep(2)
    # await coinbot.servos.reset_servos()


if __name__ == "__main__":
    asyncio.run(main())
