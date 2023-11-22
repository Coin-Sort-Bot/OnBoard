import asyncio

from main.coinbot import CoinBot


async def main():
    coinbot = CoinBot(servos=False)
    coinbot.motor.start_spinning(100)
    await asyncio.sleep(5)
    coinbot.motor.stop_spinning()


if __name__ == "__main__":
    asyncio.run(main())
