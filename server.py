#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import numpy
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)


class Chunk:
    def __init__(self, position, grid):
        self.position = position
        self.grid = grid


users = set()
bombs = [{"position": {"X": 1, "Y": 1, "x": 2, "y": 2}}]
chunks = [
    {
        "position": {"x": 1, "y": 1},
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 0, 1],
        ],
    },
    {
        "position": {"x": 2, "y": 1},
        "grid": [
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
        ],
    },
]

i = 0
for chunk in chunks:
    flat_chunk_data = []
    for sublist in chunks[i]["grid"]:
        for item in sublist:
            flat_chunk_data.append(item)
    chunks[i]["grid"] = flat_chunk_data

print(chunks)

# arrvalspot = 0
# flat_chunk_data = numpy.array(flat_chunk_data)
# for x in flat_chunk_data:
#     if x == 0:
#         randnum = random.randint(1, 2)
#         if randnum == 1:
#             randnum = 0
#         flat_chunk_data[arrvalspot] = randnum
#     arrvalspot += 1

# print(flat_chunk_data)
# print(chunks)


def users_event():
    return json.dumps({"type": "users", "count": len(users)})


def bombs_event():
    return json.dumps({"type": "bombs", "data": bombs})


def chunks_event():
    return json.dumps({"type": "chunks", "data": chunks})


async def notify_users():
    if users:
        message = users_event()
        await asyncio.wait([user.send(message) for user in users])


async def notify_bombs():
    if bombs:
        message = bombs_event()
        await asyncio.wait([user.send(message) for user in users])


async def notify_chunks():
    if chunks:
        message = chunks_event()
        await asyncio.wait([user.send(message) for user in users])


async def register(websocket):
    users.add(websocket)
    await notify_chunks()


async def unregister(websocket):
    users.remove(websocket)
    await notify_users()


async def incoming_socket(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(chunks_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                USERS["count"] -= 1
                await notify_users()
            elif data["action"] == "plus":
                USERS["count"] += 1
                await notify_users()
            else:
                logging.error("unsupported event: %s", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(incoming_socket, "192.168.2.10", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
