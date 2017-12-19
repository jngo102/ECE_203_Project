from Tkinter import *
import random
import pickle

playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
for player in playerData:
    if player[2] == 1:
        playerName = player[0]

class resource_quest:
    ####write the __init__ here
    def __init__(self,root):
        self.root = root
        x_axis = 800
        y_axis = 600
        global last_location

        last_location = [467, 301]
        root.title("The Resource Quest")
        self.c = Canvas(root, width=x_axis, height=y_axis, bg="beige")
        self.planet_map_image = PhotoImage(file="images/Slide1.gif")
        self.space_ship_image = PhotoImage(file="images/Slide2.gif")
        self.alien_image = PhotoImage(file="images/Slide3.gif")
        self.c.create_image(0, 0, image=self.planet_map_image, anchor=NW)
        self.c.grid(row=1, column=0, columnspan=2)
        self.imageID = self.c.create_image(400, 320, image=self.space_ship_image, anchor=NW)
        self.alien = self.c.create_image(500, 400, image=self.alien_image, anchor=NW)

        print "The dimensions of the map image are:", self.planet_map_image.width(), self.planet_map_image.height()

        # create a display which will keep track of the user's remaining fuel,
        # resources collected and available space.
        statistics_display = Frame(root, bg='beige')
        statistics_display.grid(row=0, column=5, columnspan=3, rowspan=4, sticky=NS)

        self.fuel = Label(statistics_display, text="Fuel", width=20)
        self.fuel.grid(row=0, column=1)
        self.fuel_display = Entry(statistics_display, width=15, justify=CENTER)
        self.fuel_display.grid(row=0, column=2)
        self.fuel_display.insert(0, 0)

        self.resources = Label(statistics_display, text="Resources", width=20)
        self.resources.grid(row=1, column=1)
        self.resources_display = Entry(statistics_display, width=15, justify=CENTER)
        self.resources_display.grid(row=1, column=2)
        self.resources_display.insert(0, 0)

        self.space = Label(statistics_display, text="Space", width=20)
        self.space.grid(row=2, column=1)
        self.space_display = Entry(statistics_display, width=15, justify=CENTER)
        self.space_display.grid(row=2, column=2)
        self.space_display.insert(0,0)

        self.target = Label(statistics_display, text="Required Resources", width=20)
        self.target.grid(row=6, column=1)
        self.target_resources_display = Entry(statistics_display, width=15, justify=CENTER)
        self.target_resources_display.grid(row=6, column=2)
        #self.target_resources_display.delete(0, END)
        #self.target_resources_display.insert(0,target_resources)

        self.feedback = Label(statistics_display, text="Feedback", width=20)
        self.feedback.grid(row=7, column=1)
        self.feedback_display = Entry(statistics_display, width=15, justify=CENTER)
        self.feedback_display.grid(row=7, column=2)
        self.feedback_display.delete(0, END)

        self.mission = Label(statistics_display,text="\n\nPlanet Earth is running out of usable energy.\n "
                                                     "Soon the human race will suffer the consequences!!\n"
                                                     " You must save us by gathering resources from nearby planets!!\n "
                                                     "Save Earth!!! Save the human race!!\n\n"
                                                     "If you return before collecting the required resources,\n"
                                                     "the crisis will prevail. Do not return unless you prosper!")
        self.mission.grid(row=8,columnspan=5)


    ###put the basics here
        # create the start playing button and display it to the user
        self.start_button = Button(statistics_display, text="START GAME", command=self.start_game)  # command = play_level1
        self.start_button.grid(row=3, column=0, columnspan=4)

        self.reset_button = Button(statistics_display, text="RESET GAME", command=self.reset_game)  # command = reset_function
        self.reset_button.grid(row=4, column=0, columnspan=4)

        self.quit_button = Button(statistics_display, text="QUIT GAME", command=self.quit_game)  # command = quit_game
        self.quit_button.grid(row=5, column=0, columnspan=4)


        ####put the functions here

    def quit_game(self):
        print "See ya!!"
        exit()


    def start_game(self):
        global bind_button
        global fuel_available
        global space_available
        global target_resources
        global points
        fuel_available = random.randint(9000, 100000)
        space_available = random.randint(10000, 100000)
        bind_button = self.c.bind("<Button-1>", self.navigation)
        target_resources = random.randint(1000, 20000)
        points = 0

        self.fuel_display.delete(0, END)
        self.fuel_display.insert(0, fuel_available)
        self.space_display.delete(0, END)
        self.space_display.insert(0, space_available)
        self.target_resources_display.delete(0, END)
        self.target_resources_display.insert(0, target_resources)

    def reset_game(self):
        global target_resources
        global fuel_available
        global space_available
        global bind_button
        global points
        global last_location

        last_location = [467, 301]
        fuel_available = random.randint(10000, 100000)
        space_available = random.randint(10000, 100000)
        target_resources = random.randint(1000, 50000)
        bind_button = self.c.bind("<Button-1>", self.navigation)
        points = 0

        self.c.delete(self.imageID)
        self.imageID = self.c.create_image(400, 320, image=self.space_ship_image, anchor=NW)

        self.fuel_display.delete(0, END)
        self.fuel_display.insert(0,fuel_available)
        self.space_display.delete(0, END)
        self.space_display.insert(0, space_available)

        self.resources_display.delete(0, END)
        self.resources_display.insert(0, 0)


        self.target_resources_display.delete(0, END)
        self.target_resources_display.insert(0, target_resources)

        self.feedback_display.delete(0,END)
        self.feedback_display.insert(0,"Explore!!")

        self.start_game()
        self.start_button.configure(state=NORMAL)



        print "Reset game initiated....play now!!"

    def you_lose(self):
        global playerName
        print "game over!!"
        self.feedback_display.delete(0, END)
        self.feedback_display.insert(0, "Game Over!!")
        self.fuel_display.delete(0, END)
        self.fuel_display.insert(0, str(fuel_available))
        self.space_display.delete(0, END)
        self.space_display.insert(0, 0)
        self.resources_display.delete(0, END)
        self.resources_display.insert(0, str(points))
        self.c.unbind("<Button-1>", bind_button)
        self.start_button.configure(state=DISABLED)

    def display(self):
        self.fuel_display.delete(0, END)
        self.fuel_display.insert(0, str(fuel_available))
        self.space_display.delete(0, END)
        self.space_display.insert(0, str(space_available))
        self.resources_display.delete(0, END)
        self.resources_display.insert(0, str(points))
        print "Space available: ", space_available
        print "Fuel available: ", fuel_available

    def navigation(self,event):
        global points
        global fuel_available
        global space_available
        global x1
        global y1

        x1, y1 = event.x, event.y
        print "Location", x1, y1

        self.c.delete(self.imageID)  # deletes the previoous icon everytime a new event occures
        self.imageID = self.c.create_image(x1, y1, image=self.space_ship_image, anchor=NW)
        #####Mercury-Venus####
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            points += random.randint(300,500)
            fuel_available -= random.randint(3000,5000)
            space_available -= random.randint(30000,50000)
            print "Last location---Venus from Mercury: ", last_location
            self.display()

        #####Mercury-Mars####
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            points += random.randint(100,200)
            fuel_available -= random.randint(100,2000)
            space_available -= random.randint(1000,2000)
            print "Last location---Mars from Mercury: ", last_location
            self.display()

        ######Mercury-Jupiter#####
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            points += random.randint(0,440)
            fuel_available -= random.randint(47,480)
            space_available -= random.randint(40,9000)
            print "Last location---Jupiter from Mercury: ", last_location
            self.display()

        #########Mercury--Saturn######
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((460 < x1 < 550) and (0 < y1 < 40)):
            last_location.extend((x1, y1))
            points += random.randint(0,8500)
            fuel_available -= random.randint(850,1000)
            space_available -= random.randint(850,2900)
            print "Last location--- Saturn from Mercury: ", last_location
            self.display()

            n = random.randint(0,100)
            if n < 90:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

        #########Mercury--Uranus######
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(0,17500)
            fuel_available -= random.randint(175,1750)
            space_available -= random.randint(1740,175000)
            print "Last location---Uranus from Mercury: ", last_location
            self.display()

        ######Venus--Mercury#####BONUS FUEL###
        if ((760 < last_location[len(last_location) - 2] < 800) and (
                        280 < last_location[len(last_location) - 1] < 360)) and ((300 < x1 < 420) and (60 < y1 < 140)):
            last_location.extend((x1, y1))
            points += random.randint(310,900)
            add_fuel = random.randint(0, 400)
            fuel_available += add_fuel
            space_available -= random.randint(300,9000)
            print "You've got bonus %d fuel!!", add_fuel
            print "Last location---Mercury from Venus: ", last_location
            self.display()

        #####Venus--Mars######
        if ((760 < last_location[len(last_location) - 2] < 800) and (
                        280 < last_location[len(last_location) - 1] < 360)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            points += random.randint(500,1000)
            fuel_available -= random.randint(50,200)
            space_available -= random.randint(400,7400)
            print "Last location---Mars from Venus: ", last_location
            self.display()

            n = random.randint(0, 100)
            if n < 60:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

        ######Venus--Jupiter#####
        if ((760 < last_location[len(last_location) - 2] < 800) and (
                        280 < last_location[len(last_location) - 1] < 360)) and (
                    (100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            points += random.randint(3000,5000)
            fuel_available -= random.randint(400,700)
            space_available -= random.randint(400,50000)
            print "Last location---Jupiter from Venus: ", last_location
            self.display()

        ######Venus--Saturn######
        if ((760 < last_location[len(last_location) - 2] < 800) and (
                        280 < last_location[len(last_location) - 1] < 360)) and (
                    (460 < x1 < 550) and (0 < y1 < 40)):
            last_location.extend((x1, y1))
            points += random.randint(8000,10000)
            fuel_available -= random.randint(800,1000)
            space_available -= random.randint(8000,90000)
            print "Last location---Saturn from Venus: ", last_location
            self.display()

        #######Venus--Uranus#####
        if ((760 < last_location[len(last_location) - 2] < 800) and (
                        280 < last_location[len(last_location) - 1] < 360)) and (
                    (670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(160,1800)
            fuel_available -= random.randint(100,1900)
            space_available -= random.randint(17200,19000)
            print "Last location---Uranus from Venus: ", last_location
            self.display()

        ######Mars--Mercury######(670 < x1 < 800) and (390 < y1 < 520)
        if ((670 < last_location[len(last_location) - 2] < 800) and (
                        390 < last_location[len(last_location) - 1] < 520)) and (
                    (670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(1000,2000)
            fuel_available -= random.randint(100,2000)
            space_available -= random.randint(100,2000)
            print "Last location---Mercury to Mars: ", last_location
            self.display()

        ######Mars--Venus######
        if ((670 < last_location[len(last_location) - 2] < 800) and (
                        390 < last_location[len(last_location) - 1] < 520)) and (
                    (760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            points += random.randint(700,900)
            fuel_available -= random.randint(70,900)
            space_available -= random.randint(700,9000)
            print "Last location---Venus from Mars: ", last_location
            self.display()
        ######Mars---Jupiter######
        if ((670 < last_location[len(last_location) - 2] < 800) and (
                        390 < last_location[len(last_location) - 1] < 520)) and (
                    (100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            points += random.randint(4000,5000)
            fuel_available -= random.randint(40,5000)
            space_available -= random.randint(400,5000)
            print "Last location---Jupiter from Mars: ", last_location
            self.display()

        ######Mars--Saturn###########
        if ((670 < last_location[len(last_location) - 2] < 800) and (
                        390 < last_location[len(last_location) - 1] < 520)) and (
                    (460 < x1 < 550) and (0 < y1 < 40)):
            last_location.extend((x1, y1))
            points += random.randint(700,8000)
            fuel_available -= random.randint(700,800)
            space_available -= random.randint(7000,8000)
            print "Last location---Saturn from Mars: ", last_location
            self.display()

        #######Mars--Uranus######
        if ((670 < last_location[len(last_location) - 2] < 800) and (
                        390 < last_location[len(last_location) - 1] < 520)) and (
                    (670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(1000,2000)
            fuel_available -= random.randint(1600,2000)
            space_available -= random.randint(1600,20000)
            print "Space available: ", space_available
            print "Fuel available: ", fuel_available
            print "Last location---Uranus from Mars: ", last_location
            print "command Mars--Uranus executed"

            self.fuel_display.delete(0, END)
            self.fuel_display.insert(0, str(fuel_available))
            self.space_display.delete(0, END)
            self.space_display.insert(0, str(space_available))
            self.resources_display.delete(0, END)
            self.resources_display.insert(0, str(points))

        ##### Saturn to Mercury ###########
        if ((460 < last_location[len(last_location) - 2] < 550) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((300 < x1 < 420) and (60 < y1 < 140)):
            last_location.extend((x1, y1))
            points += random.randint(800,900)
            fuel_available -= random.randint(800,900)
            space_available -= random.randint(800,1000)
            print "Last location---Mercury from Saturn: ", last_location
            self.display()


        ###### Saturn to Venus $$$$$$$$$$$
        if ((460 < last_location[len(last_location) - 2] < 550) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            points += random.randint(800,900)
            fuel_available -= random.randint(800,900)
            space_available -= random.randint(800,1000)
            print "Last location--- Venus from Saturn: ", last_location
            self.display()

        ###### Saturn to Mars $$$$$$$$$$$
        if ((460 < last_location[len(last_location) - 2] < 550) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            points += random.randint(70,800)
            fuel_available -= random.randint(700,800)
            space_available -= random.randint(100,800)
            print "Last location--- Mars from Saturn: ", last_location
            self.display()

        ###### Saturn to Jupiter $$$$$$$$$$$
        if ((460 < last_location[len(last_location) - 2] < 550) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            points += random.randint(400,500)
            fuel_available -= random.randint(400,5000)
            space_available -= random.randint(400,5000)
            print "Last location---Jupiter from Saturn: ", last_location
            self.display()
        ###### Saturn to Uranus$$$$$$$$$$$
        if ((460 < last_location[len(last_location) - 2] < 550) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(700,9000)
            fuel_available -= random.randint(700,90000)
            space_available -= random.randint(700,9000)
            print "Last location---Uranus from Saturn: ", last_location
            self.display()

        ####Uranus to Mars###
        if ((670 < last_location[len(last_location) - 2] < 760) and (
                        40 < last_location[len(last_location) - 1] < 120)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            points += random.randint(160,2000)
            fuel_available -= random.randint(160,2000)
            space_available -= random.randint(100,2000)
            print "Last location---Jupiter from Uranus: ", last_location
            self.display()

        ####Uranus to Mercury###
        if ((670 < last_location[len(last_location) - 2] < 760) and (
                        40 < last_location[len(last_location) - 1] < 120)) and ((300 < x1 < 420) and (60 < y1 < 140)):
            last_location.extend((x1, y1))
            points += random.randint(160,20000)
            fuel_available -= random.randint(160,2000)
            space_available -= random.randint(10,2000)
            print "Last location---Mercury from Uranus: ", last_location
            self.display()

            n = random.randint(0, 100)
            if n < 60:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

         ####Uranus to Venus###
        if ((670 < last_location[len(last_location) - 2] < 760) and (
                        40 < last_location[len(last_location) - 1] < 120)) and ((760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            points += random.randint(1600,2000)
            fuel_available -= random.randint(1600,2000)
            space_available -= random.randint(100,2000)
            print "Last location---Venus from Uranus: ", last_location
            self.display()

        ####Uranus to Saturn
        if ((670 < last_location[len(last_location) - 2] < 760) and (
                        40 < last_location[len(last_location) - 1] < 120)) and ((460 < x1 < 550) and (0 < y1 < 40)):
            points += random.randint(0,2000)
            fuel_available -= random.randint(900,2000)
            space_available -= random.randint(900,2000)
            print "Last Location was : ", str(last_location)
            self.display()

       ####Uranus to Jupiter###
        if ((670 < last_location[len(last_location) - 2] < 760) and (
                        40 < last_location[len(last_location) - 1] < 120)) and ((100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            points += random.randint(400,2000)
            fuel_available -= random.randint(100,2000)
            space_available -= random.randint(1300,2000)
            print "Last location---Jupiter from Uranus: ", last_location
            self.display()
        ####Jupiter to Saturn###
        if (100 < last_location[len(last_location) - 2] < 260) and (
                        200 < last_location[len(last_location) - 1] < 420) and (460 < x1 < 550) and (0 < y1 < 40):
            last_location.extend((x1, y1))
            points += random.randint(400,2000)
            fuel_available -= random.randint(400,2000)
            space_available -= random.randint(40,2000)
            print "Last Location---Saturn from Jupiter : ", last_location
            self.display()


        ####Jupipter to Mercury########
        if (100 < last_location[len(last_location) - 2] < 260) and (
                        200 < last_location[len(last_location) - 1] < 420) and ((300 < x1 < 420) and (60 < y1 < 140)):
            last_location.extend((x1, y1))
            points += random.randint(10,2000)
            fuel_available -= random.randint(10,2000)
            space_available -= random.randint(10,2000)
            print "Last Location--Saturn from Jupiter: ", last_location
            self.display()

        ####Jupiter to Uranus #####
        if (100 < last_location[len(last_location) - 2] < 260) and (
                        200 < last_location[len(last_location) - 1] < 420) and ((670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            points += random.randint(13000,30000)
            fuel_available -= random.randint(130,300000)
            space_available -= random.randint(1300,30000)
            print "Location--Uranu: ", last_location
            self.display()


        ######Jupiter to Mars####
        if ((100 < last_location[len(last_location) - 2] < 260) and (
                        200 < last_location[len(last_location) - 1] < 420)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            points += random.randint(900,2000)
            fuel_available -= random.randint(160,2000)
            space_available -= random.randint(160,2000)
            print "Last Location--Mars from Jupiter : ", last_location
            self.display()


        ######Jupiter to Venus####
        if ((100 < last_location[len(last_location) - 2] < 260) and (
                        200 < last_location[len(last_location) - 1] < 420)) and ((760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            points += random.randint(4000,78000)
            fuel_available -= random.randint(40,2000)
            space_available -= random.randint(4000,20000)
            print "Last Location--Venus from Jupiter : ", last_location
            self.display()
            n = random.randint(0, 100)
            if n < 40:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

        #############This is for Jupiter##########################
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((100 < x1 < 260) and (200 < y1 < 420)):
            last_location.extend((x1, y1))
            print "Last Location--Jupiter from Earth: ", last_location
            points += random.randint(390,3900)
            fuel_available -= random.randint(30,3900)
            space_available -= random.randint(39,3000)
            self.display()

        ############# This is for Uranus####################
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((670 < x1 < 760) and (40 < y1 < 120)):
            last_location.extend((x1, y1))
            print "Last Location-- Uranus from Earth: ", last_location
            points += random.randint(160,2000)
            fuel_available -= random.randint(10,2000)
            space_available -= random.randint(1600,2000)
            self.display()
        ###Mercuty--Earth###
        if ((300 < last_location[len(last_location) - 2] < 420) and (
                        60 < last_location[len(last_location) - 1] < 140)) and ((390 < x1 < 530) and (240 < y1 < 370)):
            last_location.extend((x1, y1))
            print "Last Location-- Earth from Mercury: ", last_location
            fuel_available -= random.randint(5000,10000)
            self.display()
            n = random.randint(0, 100)
            if n < 50:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()


        ######Earth--Mercury#####
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((300 < x1 < 420) and (60 < y1 < 140)):
            last_location.extend((x1, y1))
            print "Last Location-- Mercury from Earth: ", last_location
            points += random.randint(100,2000)
            fuel_available -= random.randint(600,2000)
            space_available -= random.randint(100,3000)
            self.display()

        #####Earth--Venus#####
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((760 < x1 < 800) and (280 < y1 < 360)):
            last_location.extend((x1, y1))
            print "Last Location-- Venus from Earth: ", last_location
            points += random.randint(100,2000)
            fuel_available -= random.randint(100,2000)
            space_available -= random.randint(100,2000)
            self.display()
        #####Earth--Mars#####
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((670 < x1 < 800) and (390 < y1 < 520)):
            last_location.extend((x1, y1))
            print "Last Location-- Mars from Earth: ", last_location
            points += random.randint(0,20000)
            fuel_available -= random.randint(16000,200000)
            space_available -= random.randint(1000,2000000)
            print "Space available: ", space_available
            print "Fuel available: ", fuel_available

            self.fuel_display.delete(0, END)
            self.fuel_display.insert(0, str(fuel_available))
            self.space_display.delete(0, END)
            self.space_display.insert(0, str(space_available))
            self.resources_display.delete(0, END)
            self.resources_display.insert(0, str(points))

        #####Earth--Saturn#####
        if ((390 < last_location[len(last_location) - 2] < 530) and (
                        240 < last_location[len(last_location) - 1] < 370)) and ((460 < x1 < 550) and (0 < y1 < 40)):
            last_location.extend((x1, y1))
            print "Last Location-- Saturn from Earth: ", last_location
            points += random.randint(160,2000)
            fuel_available -= random.randint(160,200)
            space_available -= random.randint(100,9000)
            self.display()
            n = random.randint(0, 100)
            if n < 50:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

        ##Saturn to Earth!!######
        if ((460 < last_location[len(last_location) - 2] < 560) and (
                        0 < last_location[len(last_location) - 1] < 40)) and ((390 < x1 < 530) and (240 < y1 < 370)):
            last_location.extend((x1, y1))
            print "Last Location-- Earth from Saturn: ", last_location
            fuel_available -= random.randint(160,2000)
            self.display()
            n = random.randint(0, 100)
            if n < 20:
                print "You have been attacked by aliens!!"
                self.c.delete(self.alien)
                self.alien = self.c.create_image(x1 + 50, y1 + 20, image=self.alien_image, anchor=NW)
                self.you_lose()

        ###Hitting the SUN!!!!
        if (450 < x1 < 670) and (70 < y1 < 280):
            print "You went to the Sun!! Burn!!!"
            self.you_lose()
            self.fuel_display.delete(0, END)
            self.fuel_display.insert(0, "Burn!!!")


        ####Losing conditions####
        if (fuel_available <= 0) or (space_available <= 0) or ((points < target_resources) and (
                    (390 < x1 < 530) and (240 < y1 < 370))):
            self.display()
            self.you_lose()

        ####Winning conditions#####
        if (points >= target_resources) and ((390 < x1 < 530) and (240 < y1 < 370)):
            print "You Win!!"
            self.feedback_display.delete(0, END)
            self.feedback_display.insert(0, "You Win!!")

            self.display()

            self.c.unbind("<Button-1>", bind_button)
            self.start_button.configure(state=DISABLED)

            playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
            for player in playerData:
                if player[0] == playerName:
                    player[1] += 5000
            pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))


root = Tk()

my_game = resource_quest(root)

root.mainloop()
