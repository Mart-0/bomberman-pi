#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import numpy
import random
import data_config

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)


class Chunk:
    def __init__(self, position, grid):
        self.position = position
        self.grid = grid


players = data_config.players.copy()
users = set()
bombs = [
    {"position": {"X": 1, "Y": 1, "x": 2, "y": 2}},
    {"position": {"X": 1, "Y": 1, "x": 2, "y": 4}},
]
chunks = data_config.chunks.copy()

i = 0
for chunk in chunks:
    flat_chunk_data = []
    for sublist in chunk["grid"]:
        for item in sublist:
            flat_chunk_data.append(item)

    a = 0
    for x in flat_chunk_data:
        if x == 1:
            flat_chunk_data[a] = random.randint(1, 2)
        a += 1

    chunks[i]["grid"] = flat_chunk_data
    i += 1


def users_event():
    return json.dumps({"type": "users", "count": len(users), "data": players})


def bombs_event():
    return json.dumps({"type": "bombs", "data": bombs})


def chunks_event():
    return json.dumps({"type": "chunks", "data": chunks})


def players_event():
    return json.dumps({"type": "players", "data": players})


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


async def notify_players():
    if chunks:
        message = players_event()
        await asyncio.wait([user.send(message) for user in users])


async def register(websocket):
    users.add(websocket)
    logging.info("players connected: %s", len(users))
    await notify_users()
    await notify_chunks()
    # await notify_bombs()
    # await notify_players()


async def unregister(websocket):
    users.remove(websocket)
    logging.info("players connected: %s", len(users))
    await notify_users()


async def incoming_socket(websocket, path):
    # register(websocket) sends user_event() to websocket

    await register(websocket)
    try:
        await websocket.send(chunks_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "update_player":
                logging.info("%s", data)
                await notify_players()
            else:
                logging.error("unsupported event: %s", data)
    finally:
        await unregister(websocket)

start_server = websockets.serve(incoming_socket, "192.168.2.10", 8765)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    logging.info("server running!")
    asyncio.get_event_loop().run_forever()
finally:
    logging.error("server can't start!")
