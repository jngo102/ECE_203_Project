from Tkinter import *
from random import randint, choice
import time
import pickle

playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
for player in playerData:
    if player[2] == 1:
        playerName = player[0]

class asteroid_game():
    def __init__(self, g):
        self.g = g

        g.title("ASTEROID NINJA")

        self.canvas_width = 959
        self.canvas_height = 639

        self.lifecount = 3
        self.clickx = []
        self.clicky = []
        self.score = 0

        self.frame = Canvas(g, width=200, height=self.canvas_height, bg='black')
        self.frame.grid(row=0, column=1)
        self.canvas = Canvas(g, width=self.canvas_width, height=self.canvas_height, bg="black", cursor="shuttle")
        self.starryNight = PhotoImage(file="images/night1.gif")

        self.canvas.grid(row=0, column=0)
        self.canvas.create_image(0, 0, image=self.starryNight, anchor=NW)

        self.asteroid_image = PhotoImage(file="images/moving_asteroid.gif")
        self.asteroids = []

        self.start_button = Button(g, text="START", command=self.start, width=20, height=2, relief=FLAT)
        self.start_button_window = self.frame.create_window(100, 50, anchor=CENTER, window=self.start_button)

        self.label1 = Label(g, text="SHUTTLES")
        self.label1_window = self.frame.create_window(100, 100, anchor=CENTER, window=self.label1)
        self.life_display = Entry(g, justify=CENTER)
        self.life_window = self.frame.create_window(100, 150, anchor=CENTER, window=self.life_display)

        self.label2 = Label(g, text="SCORE")
        self.label2_window = self.frame.create_window(100, 300, anchor=CENTER, window=self.label2)
        self.score_display = Entry(g, justify=CENTER)
        self.score_window = self.frame.create_window(100, 350, anchor=CENTER, window=self.score_display)

        self.restart_button = Button(g, text="RESTART", width=20, command=self.restart, relief=FLAT)
        self.restart_button_window = self.frame.create_window(100, 500, anchor=CENTER, window=self.restart_button)

        self.quit_button = Button(g, text="QUIT", width=20, command=self.exitgame, relief=FLAT)
        self.quit_button_window = self.frame.create_window(100, 600, anchor=CENTER, window=self.quit_button)

        g.bind("<Button-1>", self.destroy_asteroid)

    def restart(self):
        self.g.destroy()
        execfile("AsteroidClicker.py")

    def exitgame(self):
        global playerName
        playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
        for player in playerData:
            if player[0] == playerName:
                player[1] += self.score
        pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))

        quit()

    def start(self):
        self.life_display.delete(0, END)
        self.life_display.insert(0, self.lifecount)
        self.score_display.delete(0, END)
        self.score_display.insert(0, self.score)
        self.t = time.time()

        self.repeat()

    def repeat(self):
        if self.lifecount <= 0:
            print "GAME OVER ! START AGAIN"
            pass
        else:
            print self.asteroids
            self.create_asteroid()
            for asteroid in self.asteroids:
                asteroid[1], asteroid[2] = self.canvas.coords(asteroid[0])
                if asteroid[1] <= 80 or asteroid[1] >= self.canvas_width - 80:
                    asteroid[3] = -asteroid[3]
                elif asteroid[2] >= self.canvas_height + 100:
                    self.lifecount -= 1
                    self.life_display.delete(0, END)
                    self.life_display.insert(0, self.lifecount)
                    self.canvas.delete(asteroid[0])
                    i = self.asteroids.index(asteroid)
                    del self.asteroids[i]
                self.canvas.move(asteroid[0], asteroid[3], asteroid[4])

        g.after(1000 / 60, self.repeat)

    def destroy_asteroid(self,event):
        for asteroid in self.asteroids:
            if asteroid[1] - 100 <= event.x <= asteroid[1] + 100 and asteroid[2] - 175 <= event.y <= asteroid[2] + 175:
                self.score += 100
                self.score_display.delete(0, END)
                self.score_display.insert(0, self.score)
                self.canvas.delete(asteroid[0])
                i = self.asteroids.index(asteroid)
                del self.asteroids[i]

    def create_asteroid(self):
        if time.time() - self.t >= 2:
            self.t = time.time()
            x, y = randint(100, self.canvas_width - 100), -100
            asteroid = self.canvas.create_image(x, y, image=self.asteroid_image, anchor=N)
            xs = choice([randint(-10, -1), randint(1, 10)])
            ys = randint(1, 10)
            self.asteroids.append([asteroid, x, y, xs, ys])



g = Tk()
my_GUI = asteroid_game(g)
g.mainloop()
