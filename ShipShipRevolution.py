from Tkinter import *
import random
import time
import pickle
import os

playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
for player in playerData:
    if player[2] == 1:
        playerName = player[0]

root = Tk()

w = Canvas(width=800, height=600)
w.pack()

backgroundDirectory = 'space'
backgroundFrame = 0
bg = PhotoImage(file='images/%s/%d.gif' % (backgroundDirectory, backgroundFrame))
background = w.create_image(400,300,image=bg)
numberOfFrames = len(os.listdir('images/%s' % backgroundDirectory))

ship_list = []
score = 0
spawnRate = 50
shipDirections = ["up", "down", "left", "right"]
lost = False

def keypress(event):
    global score
    key = event.char

    for ship in ship_list:
        shipSprite = ship[0]
        shipX, shipY = w.coords(shipSprite)
        if 0 <= shipX <= 100 and key == 'a':
            w.delete(shipSprite)
            del ship_list[ship_list.index(ship)]
            score += 100
        elif 700 <= shipX <= 800 and key == 'd':
            w.delete(shipSprite)
            del ship_list[ship_list.index(ship)]
            score += 100
        elif 0 <= shipY <= 100 and key == 'w':
            w.delete(shipSprite)
            del ship_list[ship_list.index(ship)]
            score += 100
        elif 500 <= shipY <= 600 and key == 's':
            w.delete(shipSprite)
            del ship_list[ship_list.index(ship)]
            score += 100

def create_ship(time_amount):
    global ship_spawn_start, ship_list, spawnRate
    if time.time() - ship_spawn_start >= time_amount:
        ship_spawn_start = time.time()

        spawnRate -= 1

        random_ship = random.randint(0,3)
        ss = PhotoImage(file='images/rocket%d.gif' % random_ship)
        direction = shipDirections[random_ship]
        ship = w.create_image(400, 300, image=ss)
        ship_list.append([ship, direction, ss])

def background_animate():
    global background, backgroundDirectory, backgroundFrame, nextFrame, numberOfFrames
    backgroundFrame += 1
    if backgroundFrame >= numberOfFrames - 1:
        backgroundFrame = 0
    nextFrame = PhotoImage(file="images/%s/%d.gif" % (backgroundDirectory, backgroundFrame))
    w.itemconfig(background, image=nextFrame)

def boundary_destroy():
    global lost

    for ship in ship_list:
        shipSprite = ship[0]
        shipX, shipY = w.coords(shipSprite)
        if shipX < -100 or shipX > 900 or shipY < -100 or shipY > 700:
            w.delete(shipSprite)
            del ship_list[ship_list.index(ship)]
            lost = True
            lose()

def lose():
    global playerName, score

    w.create_text(400, 300, text="YOU LOSE", fill='white', font=('30'))

    playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
    for player in playerData:
        if player[0] == playerName:
            player[1] += score
    pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))

def move_ships(ships):
    for ship in ships:
        shipSprite = ship[0]
        direction = ship[1]

        if direction == "up":
            w.move(shipSprite, 0, -20)
        elif direction == "down":
            w.move(shipSprite, 0, 20)
        elif direction == "left":
            w.move(shipSprite, -20, 0)
        elif direction == "right":
            w.move(shipSprite, 20, 0)

def loop():
    if lost:
        pass
    else:
        background_animate()
        create_ship(1)
        boundary_destroy()
        move_ships(ship_list)

    root.after(spawnRate, loop)

def start():
    global ship_spawn_start

    ship_spawn_start = time.time()

    loop()

Button(root, text="Press to Start", command=start).pack()

root.bind("<Key>", keypress)

root.mainloop()
