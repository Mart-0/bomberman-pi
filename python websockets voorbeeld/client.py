#!/usr/bin/env python3

import asyncio
import logging
import websockets

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)


async def incoming_socket():
    uri = "ws://192.168.2.10:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            logging.info("%s", message)


asyncio.get_event_loop().run_until_complete(incoming_socket())
