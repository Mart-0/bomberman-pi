#!/usr/bin/env python3
from sense_hat import SenseHat

import config
import asyncio
import logging
import websockets
import json
import time
import threading
from multiprocessing import Process

sense = SenseHat()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)


player = {"position": {"x": 4, "y": 4}}

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


class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        asyncio.new_event_loop().run_until_complete(incoming_socket())


async def incoming_socket():
    global chunks, bombs
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
                logging.info("%s", data)
            elif data["type"] == "chunks":
                chunks = data["data"]
                # logging.info("%s", data["data"])
                # logging.info("%s", chunks[0]["grid"])
                # build_world(data["data"])
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
    if r == 1:
        if player["position"][dir] < 7:
            player["position"][dir] += 1
    else:
        if player["position"][dir] > 0:
            player["position"][dir] -= 1


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


def stop(event):
    global running
    running = 0


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = stop


def build_world():
    global chunks
    print(chunks)

    
    # flat_chunk_data
    # O = (0, 0, 0)
    # TW = (140, 140, 200)
    # PW = (100, 48, 48)

    # dic = {2: PW, 1: TW, 0: O}
    # pixels = [dic.get(n, n) for n in flat_chunk_data]
    # sense.set_pixels(pixels)


server = WebsocketThread()
server.start()


def game_loop():
    while running:
        draw_player()
        build_world()
        time.sleep(0.05)
        sense.clear(0, 0, 0)


game_loop()