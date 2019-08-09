import asyncio
import atexit
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, thread, CancelledError
import signal

import websockets

logger = logging.getLogger("websockets")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def client(loop, executor, url: str):
    async with websockets.connect(url) as websocket:
        while True:
            message = await loop.run_in_executor(executor, input, "> ")
            if message:
                await websocket.send(message)
                response = await websocket.recv()
                print(response)
            else:
                await asyncio.sleep(1)


def shutdown(executor: ThreadPoolExecutor):
    for task in asyncio.all_tasks():
        if not task.done():
            task.cancel()
    executor.shutdown(wait=False)


def main(url: str):
    loop = asyncio.get_event_loop()
    try:
        executor = ThreadPoolExecutor()
        loop.add_signal_handler(signal.SIGINT, shutdown, executor)
        loop.run_until_complete(client(loop, executor, url))
    except CancelledError:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    # See: https://gist.github.com/yeraydiazdiaz/b8c059c6dcfaf3255c65806de39175a7
    atexit.unregister(thread._python_exit)  # pylint: disable=protected-access

    main(sys.argv[1])
