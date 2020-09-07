from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)

Player_1 = {"x": 4, "y": 4}

#Functions

def draw_player1():
    sense.set_pixel(Player_1.x, Player_1.y , G)

        
def move_up(event):
    global Player_1
    if event.action == 'pressed' and Player_1.x > 0:
        Player_1.x -= 1

def move_down(event):
    global Player_1
    if event.action == 'pressed' and Player_1.x < 7:
        Player_1.x += 1
        
def move_right(event):
    global Player_1
    if event.action == 'pressed' and Player_1.y < 0:
        Player_1.y -= (1)
        
#Player movement

sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_right = move_right 

while True:
    draw_player1()
    sleep(0.10)
    sense.clear(0, 0, 0)


