#!/usr/bin/env python3
from sense_hat import SenseHat
from multiprocessing import Process

import config
import asyncio
import logging
import websockets
import json
import time
import threading
import sys

sense = SenseHat()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)


player = {"position": {"X": 0, "Y": 0, "x": 2, "y": 2}, "id": 0}
players = set()

StartTime = time.time()

inter = ""
playerSpeed = 0.4
playerKeys = {"u": 0, "d": 0, "l": 0, "r": 0}
anti_spam = 0
running = 1

users = set()
bombs = set()
chunks = []


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        global playerKeys
        nextTime = time.time()
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


# class UpdateThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def player(self):
#         asyncio.new_event_loop().run_until_complete(update_player())


# update_thread = UpdateThread()


# async def update_player():
#     global player

#     uri = config.server["host"]
#     async with websockets.connect(uri) as websocket:
#         json_player = json.dumps({"action": "update_player", "data": player})
#         await websocket.send(json_player)


# class SendThread(threading.Thread):
#     global chunks, bombs, player, players, running

#     def __init__(self):
#         threading.Thread.__init__(self)

#     def player(self):
#         while True:
#             print("d")


# class RecvThread(threading.Thread):
#     def __init__(self, websocket):
#         threading.Thread.__init__(self)
#         self.websocket = websocket

#     def run(self):
#         recv_loop(self.websocket)
        


# def recv_loop(websocket):
#     global chunks, bombs, player, players, running

#     while True:
#         message = await websocket.recv()
#         data = json.loads(message)

#         if data["type"] == "users":
#             player["id"] = data["count"]
#             players = data["data"]
#             logging.info("players connected: %s", data["count"])
#         elif data["type"] == "bombs":
#             bombs = data["data"]
#             logging.info("%s", "boms(s) loaded!")
#         elif data["type"] == "players":
#             players = data["data"]
#             logging.info("%s", "players loaded!")
#         elif data["type"] == "chunks":
#             chunks = data["data"]
#             logging.info("%s", "chunks loaded!")
#         else:
#             logging.error("unsupported event: %s", data)

class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            asyncio.new_event_loop().run_until_complete(incoming_socket())
        finally:
            stop()
            logging.error("%s", "The server is closed or not connected!")
            sys.exit()


async def incoming_socket():
    global chunks, bombs, player, players, running
    uri = config.server["host"]
    async with websockets.connect(uri) as websocket:
        logging.info("%s", "The server is conneced!")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data["type"] == "users":
                player["id"] = data["count"]
                players = data["data"]
                logging.info("players connected: %s", data["count"])
            elif data["type"] == "bombs":
                bombs = data["data"]
                logging.info("%s", "boms(s) loaded!")
            elif data["type"] == "players":
                players = data["data"]
                logging.info("%s", "players loaded!")
            elif data["type"] == "chunks":
                chunks = data["data"]
                logging.info("%s", "chunks loaded!")
            else:
                logging.error("unsupported event: %s", data)


def draw_player():
    sense.set_pixel(player["position"]["x"], player["position"]["y"], G)


def start_move(dir):
    global playerKeys, anti_spam
    playerKeys[dir] = 1
    set_interval()
    anti_spam = 1


def move_player(dir, r):
    global player

    new_position = player["position"].copy()

    if r == 1:
        if player["position"][dir] < 7:
            new_position[dir] += 1
    else:
        if player["position"][dir] > 0:
            new_position[dir] -= 1
    s = check_position(new_position["x"], new_position["y"])

    if s == 0 or s == 1:
        player["position"] = new_position
        # update_thread.player()


def check_position(x, y):
    global chunks

    index = ((y) * 8) + x

    i = 0
    for chunk in chunks:
        if i == 0:
            grid = chunk["grid"]
        i += 1

    return grid[index]


def check_keys():
    global inter, playerKeys, anti_spam

    if playerKeys == {"u": 0, "d": 0, "l": 0, "r": 0}:
        anti_spam = 0
        inter.cancel()

    if playerKeys["u"] == 1:
        move_player("y", 0)
    if playerKeys["d"] == 1:
        move_player("y", 1)
    if playerKeys["l"] == 1:
        move_player("x", 0)
    if playerKeys["r"] == 1:
        move_player("x", 1)


def set_interval():
    global inter, playerKeys, anti_spam
    if anti_spam == 0:
        inter = setInterval(playerSpeed, check_keys)


def move_up(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["y"] > 0:
        start_move("u")
    elif event.action == "released":
        playerKeys["u"] = 0


def move_down(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["y"] < 7:
        start_move("d")
    elif event.action == "released":
        playerKeys["d"] = 0


def move_left(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["x"] > 0:
        start_move("l")
    elif event.action == "released":
        playerKeys["l"] = 0


def move_right(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["x"] < 7:
        start_move("r")
    elif event.action == "released":
        playerKeys["r"] = 0


def stop():
    global running
    running = 0


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = stop


def show_bombs():
    for bomb in bombs:
        sense.set_pixel(bomb["position"]["x"], bomb["position"]["y"], R)


def show_players():
    for player in players:
        sense.set_pixel(
            player["position"]["x"], player["position"]["y"], player["color"]
        )


def build_world():
    global chunks
    grid = 0
    i = 0
    for chunk in chunks:
        if i == 0:
            grid = chunk["grid"]
        i += 1

    if grid:
        O = (0, 0, 0)
        PW = (140, 140, 200)
        TW = (100, 48, 48)

        dic = {0: O, 1: O, 2: TW, 3: PW}
        pixels = [dic.get(n, n) for n in grid]
        sense.set_pixels(pixels)


server = WebsocketThread()
server.start()


def game_loop():
    while running:
        build_world()
        show_players()
        show_bombs()
        draw_player()
        time.sleep(0.1)
        sense.clear(0, 0, 0)


game_loop()