#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import numpy
import random
import data_config
import sys
import threading
import time

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
bomb_id = 0
bomb = 0
id = 0

i = 0
for chunk in chunks:
    flat_chunk_data = []
    for sublist in chunk["grid"]:
        for item in sublist:
            flat_chunk_data.append(item)

    a = 0
    for x in flat_chunk_data:
        if x == 1:
            random_int = random.randint(1, 60)
            if random_int > 2:
                flat_chunk_data[a] = 2
        a += 1

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
    # i = 0
    # for player in players:
    #     if player["id"]:
    #         if player["id"] == id:
    #             break
    #         else:
    #             i += 1

    return players[id]


def bombs_explosion_event():
    return json.dumps({"type": "bombs_explosion", "data": bomb})


def bombs_event():
    return json.dumps({"type": "bombs", "data": bombs})


def chunks_event():
    return json.dumps({"type": "chunks", "data": chunks})


def players_event():
    # alive_players = []
    # for player in players:
    #     if player["alive"] == 1:
    #         alive_players.append(player)

    return json.dumps({"type": "players", "data": players})


async def notify_users():
    if users:
        message = users_event()
        await asyncio.wait([user.send(message) for user in users])


async def notify_bombs_explosion():
    if bomb:
        message = bombs_explosion_event()
        await asyncio.wait([user.send(message) for user in users])


async def notify_bombs():
    if bombs or bombs == []:
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
    global bomb_id
    time = 2000
    bomb = {"id": bomb_id, "position": data["data"]["position"], "time": time}
    bomb_id += 1
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
    except Exception as e:
        logging.error("error: %s", e)
        logging.error("conection closed!")
        await unregister_dashboard(websocket)


def check_position(position):
    global chunks

    index = ((position["y"]) * 8) + position["x"]

    for chunk in chunks:
        if (
            chunk["position"]["x"] == position["X"]
            and chunk["position"]["y"] == position["Y"]
        ):
            grid = chunk["grid"]

    return grid[index]


def remove_wall(grid, position):
    wall = check_position(position)
    if wall == 2:
        index = ((position["y"]) * 8) + position["x"]
        del grid[index]
        grid.insert(index, 0)
    return grid


def kill_player(pos):
    global players, player
    players_in_chunk = []

    if players:
        for player in players:

            if (
                player["position"]["X"] == pos["X"]
                and player["position"]["Y"] == pos["Y"]
            ):
                players_in_chunk.append(player)

        for player in players_in_chunk:
            id = 0
            if (
                player["position"]["x"] == pos["x"]
                and player["position"]["y"] == pos["y"]
            ):
                id = player["id"]

            for player in players:
                if player["id"] == id:
                    player["alive"] = 0


async def explode_bom(data):
    global chunks

    for chunk in chunks:
        if (
            chunk["position"]["x"] == data["position"]["X"]
            and chunk["position"]["y"] == data["position"]["Y"]
        ):
            grid = chunk["grid"]

    if grid:
        x = 1
        while x < 6:
            pos = data["position"].copy()
            pos["x"] = pos["x"] + x - 3
            if pos["x"] >= 0 and pos["x"] < 8:
                kill_player(pos)
                grid = remove_wall(grid, pos)
            x += 1

        y = 1
        while y < 6:
            pos = data["position"].copy()
            pos["y"] = pos["y"] + y - 3
            if pos["y"] >= 0 and pos["y"] < 8:
                kill_player(pos)
                grid = remove_wall(grid, pos)
            y += 1

    for chunk in chunks:
        if (
            chunk["position"]["x"] == data["position"]["X"]
            and chunk["position"]["y"] == data["position"]["Y"]
        ):
            chunk["grid"] = grid

    await notify_chunks()
    await notify_players()


# 145.44.96.127
# 192.168.2.10


class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            start_server = websockets.serve(incoming_socket, "192.168.2.10", 8765)
            start_web_server = websockets.serve(website_socket, "192.168.2.10", 8766)
        except Exception as e:
            logging.error("error: %s", e)
            logging.error("server can't start!")
            sys.exit()

        try:
            loop.run_until_complete(start_server)
            loop.run_until_complete(start_web_server)

            logging.info("server running!")
            loop.run_forever()
        except Exception as e:
            logging.error("error: %s", e)
            logging.error("server can't start!")
            sys.exit()


websocket_thread = WebsocketThread()
websocket_thread.start()


class BombsTimer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.timer())
        loop.run_forever()

    async def timer(self):
        global bombs, bomb
        while True:
            time.sleep(0.1)
            for c_bomb in bombs:
                if c_bomb["time"] > 0:
                    c_bomb["time"] -= 100
                else:
                    bombs.remove(c_bomb)
                    bomb = c_bomb
                    await explode_bom(bomb)
                    await notify_bombs_explosion()
                    await notify_bombs()


bombs_timer = BombsTimer()
bombs_timer.start()
