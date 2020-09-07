#!/usr/bin/env python3
from sense_hat import SenseHat

import config
import asyncio
import logging
import websockets
import json

sense = SenseHat()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)

users = set()
bombs = set()
chunks = []


async def incoming_socket():
    uri = config.server["host"]
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data["type"] == "users":
                # USERS = data["data"]
                logging.info("%s", data["count"])
            elif data["type"] == "bombs":
                bombs = data["data"]
                # logging.info("%s", data)
            elif data["type"] == "chunks":
                chunks = data["data"]
                # logging.info("%s", data["data"])
                # logging.info("%s", chunks[0]["grid"])
                build_world(data["data"])
            else:
                logging.error("unsupported event: %s", data)


def build_world(chunks):
    flat_chunk_data = []
    for sublist in chunks[0]["grid"]:
        for item in sublist:
            flat_chunk_data.append(item)

    O = (0, 0, 0)
    TW = (140, 140, 200)
    PW = (100, 48, 48)
    
    dic = {2: PW, 1: TW, 0: O}
    pixels = [dic.get(n, n) for n in flat_chunk_data]
    sense.set_pixels(pixels)


asyncio.get_event_loop().run_until_complete(incoming_socket())
