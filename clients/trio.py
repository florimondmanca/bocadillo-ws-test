import logging
import sys

import trio
from trio_websocket import open_websocket_url

logger = logging.getLogger("trio-websocket")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def main(url: str):
    async with open_websocket_url(url) as ws:
        async with await trio.open_file("messages") as f:
            await f.seek(0, 2)  # go to end of file
            while True:
                line = await f.readline()
                if not line:
                    continue
                await ws.send_message(line.strip())
                message = await ws.get_message()
                print(message)


trio.run(main, sys.argv[1])
