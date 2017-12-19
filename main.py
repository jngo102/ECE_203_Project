from Tkinter import *
import os
import pickle

# Class definition for main map
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Exploration")
        self.canvas = Canvas(self.root, width=1280, height=720)
        self.canvas.pack()

        # Booleans that will be toggled based on mouse cursor position
        self.BaofengGame = False
        self.JasonGame = False
        self.KathrinaGame = False
        self.MohammadGame = False
        self.RyanGame = False

        self.cursorPos = 500        # Position of cursor when entering player name
        self.playerName = []        # List of individual characters when entering player name
        self.playerNameCanvas = []  # List of letters on canvas when entering player name
        self.FPS = 60               # Number of frames per second that loop() function will run
        self.lastIndex = -1         # Initial value of index that changes as player enters/deletes characters in name entry

        # Initialization of background, background image, and background animation frame
        self.backgroundImage = PhotoImage(file="images/comet/0.gif")
        self.background = self.canvas.create_image(0, 0, image=self.backgroundImage, anchor='nw')
        self.backgroundFrame = 0

        # Initialization of Mercury, Mercury image, and Mercury animation frame
        self.MercuryImage = PhotoImage(file="images/Mercury/0.gif")
        self.Mercury = self.canvas.create_image(150, 150, image=self.MercuryImage)
        self.MercuryFrame = 0

        # Initialization of moons, moons image, and moons animation frame
        self.moonsImage = PhotoImage(file="images/moons/0.gif")
        self.moons = self.canvas.create_image(700, 250, image=self.moonsImage)
        self.moonsFrame = 0

        # Initialization of Neptune, Neptune image, and Neptune animation frame
        self.NeptuneImage = PhotoImage(file="images/Neptune/0.gif")
        self.Neptune = self.canvas.create_image(300, 500, image=self.NeptuneImage)
        self.NeptuneFrame = 0

        # Initialization of rocky, rocky image, and rocky animation frame
        self.rockyImage = PhotoImage(file="images/rocky/0.gif")
        self.rocky = self.canvas.create_image(1000, 550, image=self.rockyImage)
        self.rockyFrame = 0

        # Initialization of wormhole, wormhole image, and wormhole animation frame
        self.wormholeImage = PhotoImage(file="images/wormhole/0.gif")
        self.wormhole = self.canvas.create_image(1100, 200, image=self.wormholeImage)
        self.wormholeFrame = 0

        # Sets leaderboard text at bottom center of map; includes Boolean that toggles when mouse hovers over text
        self.leaderboardText = self.canvas.create_text(640, 700, text="Leaderboard", fill='white', font=('Roboto', 20))
        self.leaderboardOn = False

        # Warning text used to tell players if their name is too long or not long enough
        self.warningText = self.canvas.create_text(640, 500, text="", fill='white', font=('Roboto', 18))
        self.canvas.itemconfig(self.warningText, state=HIDDEN)

        # Text that tells player to enter name
        self.namePrompt = self.canvas.create_text(300, 360, text="Enter your name:", fill='white', font=('Roboto', 24))

        # Key bindings for entering/deleting characters when typing name and submitting it
        self.root.bind('<Key>', self.enter_name)
        self.root.bind('<BackSpace>', self.backspace)
        self.root.bind('<Return>', self.start)

    # Function bound to <BackSpace> event
    def backspace(self, event):
        if len(self.playerNameCanvas) > 0:
            self.canvas.delete(self.playerNameCanvas[self.lastIndex])
            del self.playerNameCanvas[self.lastIndex]
            del self.playerName[self.lastIndex]
            self.lastIndex -= 1
            self.cursorPos -= 25

    # Function bound to <Button-1> event
    def click(self, event):
        if os.name == 'nt':
            prefix = ''
        elif os.name == 'posix':
            prefix = 'python '
        if self.BaofengGame:
            os.system('%sShipShipRevolution.py' % prefix)
        elif self.JasonGame:
            os.system('%sSpaceShooter.py' % prefix)
        elif self.KathrinaGame:
            os.system('%sAsteroidClicker.py' % prefix)
        elif self.MohammadGame:
            os.system('%sResourceQuest.py' % prefix)
        elif self.RyanGame:
            os.system('%sMultipleChoiceQuestions.py' % prefix)
        elif self.leaderboardOn:
            self.display_leaderboard()

    # Leaderboard window opens when "Leaderboard" text on map is clicked on
    def display_leaderboard(self):
        self.leaderboard = Tk()
        self.leaderboard.title("Leaderboard")
        playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
        playerData.sort(key=lambda list: list[1], reverse=True)
        Label(self.leaderboard, text="Leaderboard").grid(row=0, columnspan=2)
        Label(self.leaderboard, text="Player").grid(row=1, column=0)
        Label(self.leaderboard, text="Score").grid(row=1, column=1)
        Label(self.leaderboard, text="-=-=-=-=-=-=-=-=-=-=-=-=-").grid(row=2, columnspan=2)
        for player in playerData:
            i = playerData.index(player)
            playerName = player[0]
            playerScore = player[1]
            nameLabel = Label(self.leaderboard, text=playerName)
            nameLabel.grid(row=i+3, column=0)
            scoreLabel = Label(self.leaderboard, text=playerScore)
            scoreLabel.grid(row=i+3, column=1)
            if playerName == self.playerName:
                nameLabel.config(font=('bold'))
                scoreLabel.config(font=('bold'))

    # Function bound to <Key> event
    def enter_name(self, event):
        if self.cursorPos >= 750:
            self.canvas.itemconfig(self.warningText, text="You've reached the character limit.", state=NORMAL)
        else:
            if event.char.isalnum():
                self.letter = self.canvas.create_text(self.cursorPos, 360, text=event.char, fill='white', font=('Roboto', 24))
                self.playerNameCanvas.append(self.letter)
                self.playerName.append(event.char)
                self.cursorPos += 25
                self.lastIndex += 1

    # Function that loops to animate canvas objects
    def loop(self):
        self.backgroundFrame += 1
        if self.backgroundFrame == len(os.listdir("images/comet")):
            self.backgroundFrame = 0
        self.backgroundImage = PhotoImage(file="images/comet/%d.gif" % self.backgroundFrame)
        self.canvas.itemconfig(self.background, image=self.backgroundImage)

        self.MercuryFrame += 1
        if self.MercuryFrame == len(os.listdir("images/Mercury")):
            self.MercuryFrame = 0
        self.MercuryImage = PhotoImage(file="images/Mercury/%d.gif" % self.MercuryFrame)
        self.canvas.itemconfig(self.Mercury, image=self.MercuryImage)

        self.moonsFrame += 1
        if self.moonsFrame == len(os.listdir("images/moons")):
            self.moonsFrame = 0
        self.moonsImage = PhotoImage(file="images/moons/%d.gif" % self.moonsFrame)
        self.canvas.itemconfig(self.moons, image=self.moonsImage)

        self.NeptuneFrame += 1
        if self.NeptuneFrame == len(os.listdir("images/Neptune")):
            self.NeptuneFrame = 0
        self.NeptuneImage = PhotoImage(file="images/Neptune/%d.gif" % self.NeptuneFrame)
        self.canvas.itemconfig(self.Neptune, image=self.NeptuneImage)

        self.rockyFrame += 1
        if self.rockyFrame == len(os.listdir("images/rocky")):
            self.rockyFrame = 0
        self.rockyImage = PhotoImage(file="images/rocky/%d.gif" % self.rockyFrame)
        self.canvas.itemconfig(self.rocky, image=self.rockyImage)

        self.wormholeFrame += 1
        if self.wormholeFrame == len(os.listdir("images/wormhole")):
            self.wormholeFrame = 0
        self.wormholeImage = PhotoImage(file="images/wormhole/%d.gif" % self.wormholeFrame)
        self.canvas.itemconfig(self.wormhole, image=self.wormholeImage)

        self.root.after(1000/self.FPS, self.loop)

    # Function bound to <Motion> event
    def navigate(self, event):
        if 40 <= event.x <= 260 and 35 <= event.y <= 265:
            self.BaofengGame = True
        elif 1020 <= event.x <= 1180 and 115 <= event.y <= 280:
            self.JasonGame = True
        elif 550 <= event.x <= 865 and 100 <= event.y <= 415:
            self.KathrinaGame = True
        elif 200 <= event.x <= 500 and 300 <= event.y <= 600:
            self.MohammadGame = True
        elif 920 <= event.x <= 1090 and 465 <= event.y <= 635:
            self.RyanGame = True
        elif 560 <= event.x <= 720 and 690 <= event.y <= 710:
            self.canvas.itemconfig(self.leaderboardText, fill='red', font=('Roboto', 24))
            self.leaderboardOn = True
        else:
            self.BaofengGame, self.JasonGame, self.KathrinaGame, self.MohammadGame,\
            self.RyanGame, self.leaderboardOn = False, False, False, False, False, False
            self.canvas.itemconfig(self.leaderboardText, fill='white', font=('Roboto', 20))

    # Configuration of various canvas objects and player variables
    def start(self, event):
        if len(self.playerName) == 0:
            self.canvas.itemconfig(self.warningText, text="You must have at least one character for your name.", state=NORMAL)
        else:
            try:
                playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
            except:
                playerData = []
            uniqueNames = 0
            playerName = ''.join(self.playerName)
            for player in playerData:
                player[2] = 0
                if playerName == player[0]:
                    pass
                else:
                    uniqueNames += 1
            if uniqueNames == len(playerData):
                self.canvas.itemconfig(self.namePrompt, state=HIDDEN)
                self.canvas.itemconfig(self.warningText, state=HIDDEN)
                for letter in self.playerNameCanvas:
                    self.canvas.itemconfig(letter, state=HIDDEN)
                self.root.unbind('<Key>')
                self.root.unbind('<Return>')
                self.root.bind('<Motion>', self.navigate)
                self.root.bind('<Button-1>', self.click)
                self.playerName = ''.join(self.playerName)

                playerData.append([self.playerName, 0, 1])
                pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))
                self.loop()
            else:
                self.canvas.itemconfig(self.warningText, text="Someone has already chosen that name.", state=NORMAL)

root = Tk()
Project = Game(root)

root.mainloop()
