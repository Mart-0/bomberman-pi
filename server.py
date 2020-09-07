#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)


class Chunk:
    def __init__(self, position, grid):
        self.position = position
        self.grid = grid


STATE = {"value": 0}

USERS = set()
BOMBS = set()
CHUNKS = {
    Chunk(
        {"x": 1, "y": 1},
        [
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
        ],
    )
}


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def bombs_event():
    return json.dumps({"type": "bombs", **BOMBS})


def chunks_event():
    return json.dumps({"type": "chunks", **CHUNKS})


async def notify_users():
    if USERS:
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_bombs():
    if BOMBS:
        message = bombs_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_chunks():
    if CHUNKS:
        message = chunks_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def incoming_socket(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(bombs_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_bombs()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_bombs()
            else:
                logging.error("unsupported event: %s", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(incoming_socket, "192.168.2.20", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
