import asyncio
import base64
from os import getenv
from pprint import pprint

from dotenv import load_dotenv
import logging
import aiohttp
from main import CoinBot

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
server = getenv("SERVER")


async def main():
    coinbot = CoinBot()
    await coinbot.setup()

    photo1 = await coinbot.cameras.camera1.capture()
    photo2 = await coinbot.cameras.camera2.capture()
    image1b64 = f"data:image/jpg;base64,{base64.b64encode(photo1).decode('ascii')}"
    image2b64 = f"data:image/jpg;base64,{base64.b64encode(photo2).decode('ascii')}"

    async with aiohttp.ClientSession() as session:
        for imageb64 in (image1b64, image2b64):
            logging.debug("Uploading image")
            logging.debug(imageb64)
            async with session.post(
                f"{server}/coin/images/",
                data={
                    "image": imageb64,
                },
            ) as response:
                pprint(response.status)
                pprint(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
