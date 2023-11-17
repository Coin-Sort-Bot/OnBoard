import asyncio

from src.main.coinbot import CoinBot


async def main():
    coinbot = CoinBot()
    coinbot.motor.set_speed(100)
    await asyncio.sleep(5)
    coinbot.motor.set_speed(0)


if __name__ == "__main__":
    asyncio.run(main())
