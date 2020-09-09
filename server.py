#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import numpy
import random
import data_config
import sys
import datetime
import time
import threading

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
web_users = set()
bombs = []
chunks = data_config.chunks.copy()

id = 1


i = 0
for chunk in chunks:
    flat_chunk_data = []
    for sublist in chunk["grid"]:
        for item in sublist:
            flat_chunk_data.append(item)

    # a = 0
    # for x in flat_chunk_data:
    #     if x == 1:
    #         flat_chunk_data[a] = random.randint(1, 2)
    #     a += 1

    chunks[i]["grid"] = flat_chunk_data
    i += 1


def users_event():
    global id

    json_users = json.dumps(
        {"type": "users", "count": len(users), "data": get_user(id)}
    )
    id += 1
    return json_users


def get_user(id):
    global players
    i = 0
    for player in players:
        if player["id"]:
            if player["id"] == id:
                break
            else:
                i += 1

    return players[i]


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
    if players:
        message = players_event()
        await asyncio.wait([user.send(message) for user in users])


async def web_notify_users():
    if users:
        message = users_event()
        await asyncio.wait([user.send(message) for user in web_users])


async def web_notify_bombs():
    if bombs:
        message = bombs_event()
        await asyncio.wait([user.send(message) for user in web_users])


async def web_notify_chunks():
    if chunks:
        message = chunks_event()
        await asyncio.wait([user.send(message) for user in web_users])


async def web_notify_players():
    if players:
        message = players_event()
        await asyncio.wait([user.send(message) for user in web_users])


async def register(websocket):
    users.add(websocket)
    logging.info("players connected: %s", len(users))
    await notify_users()
    await notify_chunks()
    await notify_bombs()
    await notify_players()


async def unregister(websocket):
    users.remove(websocket)
    logging.info("players connected: %s", len(users))
    await notify_users()


async def register_dashboard(websocket):
    web_users.add(websocket)
    logging.info("web users connected: %s", len(web_users))
    await web_notify_users()
    await web_notify_chunks()
    await web_notify_players()


async def unregister_dashboard(websocket):
    web_users.remove(websocket)
    logging.info("web users connected: %s", len(web_users))


def update_player(data):
    global players
    i = 0
    for player in players:
        if player["id"]:
            if player["id"] == data["data"]["id"]:
                break
            else:
                i += 1

    players[i]["position"] = data["data"]["position"]


async def place_bomb(data):
    bomb = {"position": data["data"]["position"], "time": 2000}
    bombs.append(bomb)
    await notify_bombs()


async def incoming_socket(websocket, path):
    # register(websocket) sends user_event() to websocket

    await register(websocket)
    try:
        await websocket.send(chunks_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "update_player":
                logging.info("%s", data)
                update_player(data)
                await notify_players()
            elif data["action"] == "place_bomb":
                logging.info("%s", data)
                await place_bomb(data)
            else:
                logging.error("unsupported event: %s", data)
    except Exception as e:
        logging.error("error: %s", e)
        logging.error("conection closed!")
        await unregister(websocket)


async def website_socket(websocket, path):
    await register_dashboard(websocket)
    try:
        await websocket.send(chunks_event())

        async for message in websocket:
            data = json.loads(message)
            print(data)
    except Exception as e:
        logging.error("error: %s", e)
        logging.error("conection closed!")
        await unregister_dashboard(websocket)


class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("d")
        # 145.44.96.127
        # 192.168.2.10

        start_server = websockets.serve(incoming_socket, "192.168.2.10", 8765)
        start_web_server = websockets.serve(website_socket, "192.168.2.10", 8766)

        try:
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_until_complete(start_web_server)

            logging.info("server running!")
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            logging.error("error: %s", e)
            logging.error("server can't start!")
            sys.exit()


server = WebsocketThread()
server.start()

print("sd")


class BombTimer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.run()

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.bomb_timer())

    async def bomb_timer(self):
        global bombs
        start_time = time.time()
        seconds = 0.1
        print("ik draai")

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            await asyncio.sleep(1)

            for bomb in bombs:
                bomb["time"] -= 1
                if sqrt(bomb["current_time"]) - sqrt(bomb["time"]) > 1:
                    bomb["current_time"] = bomb["time"]
                    bomb["flicker"] = not bomb["flicker"]
                    print("flicker")

                if bomb["time"] <= 0:
                    break


BombTimer()
