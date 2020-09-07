from sense_hat import SenseHat
import time, threading

sense = SenseHat()

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)

Player_1 = {"position": {"x": 4, "y": 4}}


StartTime = time.time()

inter = ""
playerSpeed = 0.4


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        self.action()
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def draw_player1():
    sense.set_pixel(Player_1["position"]["x"], Player_1["position"]["y"], G)


def move_player_up():
    global Player_1
    if Player_1["position"]["y"] > 0:
        Player_1["position"]["y"] -= 1


def move_player_down():
    global Player_1
    if Player_1["position"]["y"] < 7:
        Player_1["position"]["y"] += 1


def move_player_left():
    global Player_1
    if Player_1["position"]["x"] > 0:
        Player_1["position"]["x"] -= 1


def move_player_right():
    global Player_1
    if Player_1["position"]["x"] < 7:
        Player_1["position"]["x"] += 1


def move_up(event):
    global Player_1
    global inter
    if event.action == "pressed" and Player_1["position"]["y"] > 0:
        inter = setInterval(playerSpeed, move_player_up)
    elif event.action == "released":
        inter.cancel()


def move_down(event):
    global Player_1
    global inter
    if event.action == "pressed" and Player_1["position"]["y"] < 7:
        inter = setInterval(playerSpeed, move_player_down)
    elif event.action == "released":
        inter.cancel()


def move_left(event):
    global Player_1
    global inter
    if event.action == "pressed" and Player_1["position"]["x"] > 0:
        inter = setInterval(playerSpeed, move_player_left)
    elif event.action == "released":
        inter.cancel()


def move_right(event):
    global Player_1
    global inter
    if event.action == "pressed" and Player_1["position"]["x"] < 7:
        inter = setInterval(playerSpeed, move_player_right)
    elif event.action == "released":
        inter.cancel()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right

while True:
    draw_player1()
    time.sleep(0.10)
    sense.clear(0, 0, 0)