#!/usr/bin/env python3
from sense_hat import SenseHat

import config
import asyncio
import logging
import websockets
import json
import time
import threading
import sys

sense = SenseHat()
sense.low_light = False

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
)

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)


player = 0
players = set()

StartTime = time.time()

inter = ""
playerSpeed = 0.3
playerKeys = {"u": 0, "d": 0, "l": 0, "r": 0}
anti_spam = 0
running = 1

users = set()
bombs = set()
chunks = []
explosions = []
server = set()


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


async def update_player():
    global server, player

    json_player = json.dumps({"action": "update_player", "data": player})
    await server.send(json_player)
    logging.info("%s", "player send")


def place_bomb():
    asyncio.new_event_loop().run_until_complete(send_bomb())


async def send_bomb():
    global server, bombs, player

    json_bomb = json.dumps(
        {"action": "place_bomb", "data": {"position": player["position"]}}
    )
    await server.send(json_bomb)
    logging.info("%s", "bomb send")


def draw_player():
    if player:
        sense.set_pixel(
            player["position"]["x"], player["position"]["y"], player["color"]
        )


def move_screen(dir, r):
    global player

    if r == 0:
        player["position"][dir.upper()] -= 1
        player["position"][dir] = 7
    else:
        player["position"][dir.upper()] += 1
        player["position"][dir] = 0

    asyncio.new_event_loop().run_until_complete(update_player())


def move_player(dir, r):
    global player

    new_position = player["position"].copy()

    if r == 1:
        if player["position"][dir] < 7:
            new_position[dir] += 1
        elif player["position"][dir] >= 7:
            return move_screen(dir, r)
    else:
        if player["position"][dir] > 0:
            new_position[dir] -= 1
        elif player["position"][dir] <= 0:
            return move_screen(dir, r)

    s = check_position(new_position)

    if s == 0 or s == 1:
        player["position"] = new_position
        asyncio.new_event_loop().run_until_complete(update_player())


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


def start_move(dir):
    global playerKeys, anti_spam
    playerKeys[dir] = 1
    set_interval()
    anti_spam = 1


def move_up(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["y"] >= 0:
        start_move("u")
    elif event.action == "released":
        playerKeys["u"] = 0


def move_down(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["y"] <= 7:
        start_move("d")
    elif event.action == "released":
        playerKeys["d"] = 0


def move_left(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["x"] >= 0:
        start_move("l")
    elif event.action == "released":
        playerKeys["l"] = 0


def move_right(event):
    global player, anti_spam, playerKeys
    if event.action == "pressed" and player["position"]["x"] <= 7:
        start_move("r")
    elif event.action == "released":
        playerKeys["r"] = 0


def stop():
    global running, server
    running = 0
    sys.exit()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = place_bomb


def show_bombs():
    global player

    if player:
        bombs_in_screen = []
        for bomb in bombs:
            if (
                bomb["position"]["X"] == player["position"]["X"]
                and bomb["position"]["Y"] == player["position"]["Y"]
            ):
                bombs_in_screen.append(bomb)

        for bomb in bombs_in_screen:
            sense.set_pixel(bomb["position"]["x"], bomb["position"]["y"], R)


def show_players():
    global player

    if player and players:
        enemy_players = []
        for enemy_player in players:
            if (
                enemy_player["position"]["X"] == player["position"]["X"]
                and enemy_player["position"]["Y"] == player["position"]["Y"]
                and enemy_player["alive"] == 1
            ):
                enemy_players.append(enemy_player)

        for enemy_player_2 in enemy_players:
            sense.set_pixel(
                enemy_player_2["position"]["x"],
                enemy_player_2["position"]["y"],
                enemy_player_2["color"],
            )


def build_world():
    global chunks
    grid = 0

    for chunk in chunks:
        if (
            chunk["position"]["x"] == player["position"]["X"]
            and chunk["position"]["y"] == player["position"]["Y"]
        ):
            grid = chunk["grid"]

    if grid:
        O = (0, 0, 0)
        PW = (180, 180, 255)
        TW = (150, 48, 48)

        dic = {0: O, 1: O, 2: TW, 3: PW}
        pixels = [dic.get(n, n) for n in grid]
        sense.set_pixels(pixels)


def explode_bom(data):
    global explosions
    data["time"] = 300
    explosions.append(data)


def show_explosion():
    for explosion in explosions:
        if explosion["time"] > 0:

            if (
                player["position"]["X"] == explosion["position"]["X"]
                and player["position"]["Y"] == explosion["position"]["Y"]
            ):

                x = 1
                while x < 6:
                    pos = explosion["position"].copy()
                    pos["x"] = pos["x"] + x - 3
                    if pos["x"] >= 0 and pos["x"] < 8:
                        sense.set_pixel(pos["x"], pos["y"], [255, 100, 0])
                    x += 1

                y = 1
                while y < 6:
                    pos = explosion["position"].copy()
                    pos["y"] = pos["y"] + y - 3
                    if pos["y"] >= 0 and pos["y"] < 8:
                        sense.set_pixel(pos["x"], pos["y"], [255, 100, 0])
                    y += 1

            explosion["time"] -= 50
        else:
            explosions.remove(explosion)


def check_dead():
    for active_player in players:
        if active_player["alive"] == 0 and active_player["id"] == player["id"]:
            stop()


class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            asyncio.new_event_loop().run_until_complete(incoming_socket())
        except Exception as e:
            logging.error("error: %s", e)
            logging.error(
                "%s",
                "The server is closed or not connected or there are no more players!",
            )
            stop()


async def incoming_socket():
    global chunks, bombs, player, players, running, server
    uri = config.server["host"]
    async with websockets.connect(uri) as websocket:
        logging.info("%s", "The server is conneced!")

        server = websocket
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data["type"] == "users":
                if player == 0:
                    player = data["data"]
                    logging.info("id: %s", data["data"]["id"])
                logging.info("players connected: %s", data["count"])
            elif data["type"] == "bombs":
                logging.info("%s", bombs)
                bombs = data["data"]
                logging.info("%s", "bombs loaded")
            elif data["type"] == "players":
                players = data["data"]
                check_dead()
                logging.info("%s", "players loaded")
            elif data["type"] == "chunks":
                chunks = data["data"]
                logging.info("%s", "chunks loaded")
            elif data["type"] == "bombs_explosion":
                explode_bom(data["data"])
                logging.info("%s", "bomb exploded")
            else:
                logging.error("unsupported event: %s", data)


server = WebsocketThread()
server.start()


def game_loop():
    while running:
        build_world()
        show_bombs()
        show_explosion()
        show_players()
        # draw_player()
        time.sleep(0.05)
        sense.clear(0, 0, 0)


game_loop()