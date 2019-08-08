import asyncio
import logging
import sys
from contextlib import suppress

import websockets

logger = logging.getLogger("websockets")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def client(url: str):
    async with websockets.connect(url) as websocket:
        while True:
            message = input("> ")
            if message:
                await websocket.send(message)
                response = await websocket.recv()
                print(response)
            else:
                await asyncio.sleep(1)


with suppress(KeyboardInterrupt):
    asyncio.run(client(sys.argv[1]))
