from sense_hat import SenseHat
import time, threading

sense = SenseHat()

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)

Player_1 = {"position": {"x": 4, "y": 4}}

playerKeys = {"u": 0, "d": 0, "l": 0, "r": 0}

# Functions


def draw_player1():
    sense.set_pixel(Player_1["position"]["x"], Player_1["position"]["y"], G)


# def move_up(event):
#     global Player_1
#     if event.action == "pressed" and Player_1["position"]["y"] > 0:
#         Player_1["position"]["y"] -= 1


# def move_down(event):
#     global Player_1
#     if event.action == "pressed" and Player_1["position"]["y"] < 7:
#         Player_1["position"]["y"] += 1


# def move_left(event):
#     global Player_1
#     if event.action == "pressed" and Player_1["position"]["x"] > 0:
#         Player_1["position"]["x"] -= 1


# def move_right(event):
#     global Player_1
#     if event.action == "pressed" and Player_1["position"]["x"] < 7:
#         Player_1["position"]["x"] += 1


def move_up(event):
    global Player_1
    global playerKeys
    if event.action == "pressed" and Player_1["position"]["y"] > 0:
        playerKeys["u"] = 1
    elif event.action == "released":
        playerKeys["u"] = 0


def move_down(event):
    global Player_1
    global playerKeys
    if event.action == "pressed" and Player_1["position"]["y"] < 7:
        playerKeys["d"] = 1
    elif event.action == "released":
        playerKeys["d"] = 0


def move_left(event):
    global Player_1
    global playerKeys
    if event.action == "pressed" and Player_1["position"]["x"] > 0:
        playerKeys["l"] = 1
    elif event.action == "released":
        playerKeys["l"] = 0


def move_right(event):
    global Player_1
    global playerKeys
    if event.action == "pressed" and Player_1["position"]["x"] < 7:
        playerKeys["r"] = 1
    elif event.action == "released":
        playerKeys["r"] = 0


def move_player(event):
    global Player_1
    global playerKeys


StartTime = time.time()


def action():
    print("action ! -> time : {:.1f}s".format(time.time() - StartTime))


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


# start action every 0.6s
inter = setInterval(0.6, action)
print("just after setInterval -> time : {:.1f}s".format(time.time() - StartTime))


t = threading.Timer(5, inter.cancel)

t.start()

# time.sleep(3)

t.cancel()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right

while True:
    draw_player1()
    time.sleep(0.10)
    sense.clear(0, 0, 0)
