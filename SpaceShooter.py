__author__ = 'Jason Ngo'
# A 2D arcade shooter for ECE 203 project

from classes import *
from random import *
import time
import pickle

playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
for player in playerData:
    if player[2] == 1:
        playerName = player[0]

root = Tk()
root.title("Space Shooter")

# Window for developer testing purposes
if DEVELOPER_MODE:
    def add_health():
        playerShip.health += 10

    def subtract_health():
        playerShip.health -= 10

    def add_speed():
        playerShip.movementSpeed += 5

    def subtract_speed():
        playerShip.movementSpeed -= 5

    def add_bullet_speed():
        playerWeapon.bulletSpeed += 5

    def subtract_bullet_speed():
        playerWeapon.bulletSpeed -= 5

    def add_damage():
        playerWeapon.damage += 10

    def subtract_damage():
        playerWeapon.damage -= 10

    def add_shot():
        playerWeapon.type = 'spread'
        playerWeapon.shots += 1
        playerWeapon.spreadAngle += 10

    def subtract_shot():
        playerWeapon.type = 'spread'
        playerWeapon.shots -= 1
        playerWeapon.spreadAngle -= 10

    def increase_fire_rate():
        playerWeapon.fireRate += .1

    def decrease_fire_rate():
        playerWeapon.fireRate -= .1

    def disable_piercing():
        playerWeapon.piercing = False

    def enable_piercing():
        playerWeapon.piercing = True

    def disable_tracking():
        playerWeapon.chase = False

    def enable_tracking():
        playerWeapon.chase = True

    devWindow = Tk()
    devWindow.title("Developer Mode")
    Button(devWindow, text="-10 Health", command=subtract_health, width=10).grid(row=0, column=0)
    Button(devWindow, text="+10 Health", command=add_health, width=10).grid(row=0, column=1)
    Button(devWindow, text="-5 Speed", command=subtract_speed, width=10).grid(row=1, column=0)
    Button(devWindow, text="+5 Speed", command=add_speed, width=10).grid(row=1, column=1)
    Button(devWindow, text="-5 Bullet Speed", command=subtract_bullet_speed, width=10).grid(row=1, column=0)
    Button(devWindow, text="+5 Bullet Speed", command=add_bullet_speed, width=10).grid(row=1, column=1)
    Button(devWindow, text="-10 Damage", command=subtract_damage, width=10).grid(row=2, column=0)
    Button(devWindow, text="+10 Damage", command=add_damage, width=10).grid(row=2, column=1)
    Button(devWindow, text="-1 Shot", command=subtract_shot, width=10).grid(row=3, column=0)
    Button(devWindow, text="+1 Shot", command=add_shot, width=10).grid(row=3, column=1)
    Button(devWindow, text="-.1 Fire Rate", command=decrease_fire_rate, width=10).grid(row=4, column=0)
    Button(devWindow, text="+.1 Fire Rate", command=increase_fire_rate, width=10).grid(row=4, column=1)
    Button(devWindow, text="Disable Piercing", command=disable_piercing, width=10).grid(row=5, column=0)
    Button(devWindow, text="Enable Piercing", command=enable_piercing, width=10).grid(row=5, column=1)
    Button(devWindow, text="Disable Tracking", command=disable_tracking, width=10).grid(row=6, column=0)
    Button(devWindow, text="Enable Tracking", command=enable_tracking, width=10).grid(row=6, column=1)

# Animates the background
def background_animate():
    global bgFrame, bgFrameIndex
    bgFrameIndex += 1
    if bgFrameIndex == NUMBER_OF_FRAMES:
        bgFrameIndex = 0
    c.itemconfig(background, image=BACKGROUND_FRAMES[bgFrameIndex])

# Provides a visual for the player getting hit by blinking ship
def blink(ship):
    if ship.blink == True:
        c.itemconfig(ship, state=HIDDEN)
    elif ship.blink == False:
        c.itemconfig(ship, state=NORMAL)

# Increases the level of difficulty after a certain period of time
def difficulty_spike(difficultyRate, levelsList):
    global levelStart, enemiesList, level, SPAWN_RATES, spawnRateMin, spawnRateMax
    if time.time() - levelStart >= difficultyRate and level < len(levelsList) - 1:
        levelStart = time.time()
        level += 1
        spawnRateMin, spawnRateMax = SPAWN_RATES[level][0], SPAWN_RATES[level][1]
        enemiesList = LEVELS[level]

# Describes the upgrades that each type of enemy loot provides to the player.
def drop_behavior():
    for drop in drops:
        drop.picked_up()
        if drop.pickedUp == True:
            drop.pickedUp = False
            if drop.dropType == 'health20': # Increases health by 20
                playerShip.health += 20
            elif drop.dropType == 'health50':   # Increases health by 50
                playerShip.health += 50
            elif drop.dropType == 'spreadShot30':   # Turns player weapon into a
                playerWeapon.type = 'spread'        # 3-shot spreadshot with a
                playerWeapon.piercing = False       # spread angle of 30 degrees
                playerWeapon.spreadAngle = 30
                playerWeapon.shots = 3
                playerWeapon.fireRate = .1
            elif drop.dropType == 'spreadShot60':   # Turns player weapon into a
                playerWeapon.type = 'spread'        # 6-shot spreadshot with a
                playerWeapon.piercing = False       # spread angle of 60 degrees
                playerWeapon.spreadAngle = 60
                playerWeapon.shots = 5
                playerWeapon.fireRate = .1
            elif drop.dropType == 'spreadShot90':  # Turns player weapon into a
                playerWeapon.type = 'spread'        # 12-shot spreadshot with a
                playerWeapon.piercing = False       # spread angle of 120 degrees
                playerWeapon.spreadAngle = 90
                playerWeapon.shots = 8
                playerWeapon.fireRate = .1
            elif drop.dropType == 'spreadShot120':  # Turns player weapon into an
                playerWeapon.type = 'spread'        # 18-shot spreadshot with a
                playerWeapon.piercing = False       # spread angle of 180 degrees
                playerWeapon.spreadAngle = 120
                playerWeapon.shots = 10
                playerWeapon.fireRate = .1
            elif drop.dropType == 'rapidFire':      # Turns player weapon into a
                playerWeapon.type = 'single'        # rapid-firing turret
                playerWeapon.fireRate = .05
                playerWeapon.piercing = False
            elif drop.dropType == 'piercing':       # Bullets don't disappear, allowing
                playerWeapon.piercing = True        # them to hit enemies behind others
            elif drop.dropType == 'damageIncrease1':    # Increases weapon damage by 1
                playerWeapon.damage += 1
            elif drop.dropType == 'damageIncrease2':    # Increases weapon damage by 2
                playerWeapon.damage += 2
            elif drop.dropType == 'speedUp':        # Increases player speed by 2
                playerShip.movementSpeed += 2
            elif drop.dropType == 'chase':          # Enables auto-targeting of enemies
                playerWeapon.chase = True

# Defines all enemies' movement, firing, and death; Also controls score count upon enemy kill
def enemy_ai(targetX, targetY):
    global score
    enemiesToDelete = []    # List where dead enemies are appended to
    for index in range( len(existingEnemies) ):
        enemy = existingEnemies[index]
        enemyWeapon = enemyWeapons[index]
        if enemy.health <= 0:
            if enemy.dropped == False:
                enemy.dropped = True
                enemy_drop(enemy)
            c.delete(enemy.sprite)
            enemyWeapon.move_bullet(CANVAS_WIDTH, CANVAS_HEIGHT, 'enemy')
            if str(enemyWeapon.bullets) == "(',')": # When every enemy bullet is gone, then the enemy's Weapon instance is removed
                enemiesToDelete.append(index)
                del enemyWeapons[index]
            if enemy.killed == False:
                score += enemy.score
                enemy.killed = True
        else:
            enemy.rotate(targetX, targetY)
            if enemy.shipName == 'enemyBouncer' and enemy.sprite in c.find_enclosed(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT):
                enemy.movement_pattern(targetX, targetY, 'bounce', False, randint(100, 300) )
            else:
                enemy.movement_pattern( targetX, targetY, 'toward', True, randint(100, 300) )
            enemyWeapon.move_bullet(CANVAS_WIDTH, CANVAS_HEIGHT, 'player')
            if playerWeapon.piercing == False:
                deletePlayerBullet = True
            elif playerWeapon.piercing == True:
                deletePlayerBullet = False
            enemy.hit_by('playerBullet', playerWeapon.damage, deletePlayerBullet)
            if enemy.shipName[:5] == 'enemy':
                enemyWeapon.fire(enemy.x, enemy.y, enemy.angle, 'enemyBullet')
            elif enemy.shipName[:5] == 'alien':
                enemyWeapon.fire(enemy.x, enemy.y, enemy.angle, 'alienBullet')
    for enemy in enemiesToDelete:
        del existingEnemies[enemy]

# Establishes drop rates of enemy types
def enemy_drop(ship):
    global drops, potentialDrops
    if ship.shipName == 'enemyBasic' or ship.shipName == 'enemyBouncer':
        chances = randint(0, 15)
    elif ship.shipName == 'enemyFighter':
        chances = randint(0, 13)
    elif ship.shipName == 'enemyCruiser':
        chances = randint(0, 12)
    elif ship.shipName == 'enemyWingship':
        chances = randint(0, 6)
    elif ship.shipName == 'alienShip':
        chances = randint(0, 5)
    elif ship.shipName == 'alienRevenant':
        chances = randint(0, 1)

    # If an enemy does drop an item, that item will be appended to a list
    if chances == 0:
        randomDrop = choice(potentialDrops)
        newDrop = Drop(c, randomDrop, ship.x, ship.y)
        drops.append(newDrop)

# Function bound to <Button-1> event
def fireon(event):
    global FIRING
    FIRING = True

# Function bound to <ButtonRelease-1> event
def fireoff(event):
    global FIRING
    FIRING = False

# Function bound to <KeyDown> event
def keydown(event):
    global UP, DOWN, LEFT, RIGHT
    if event.char == 'w':
        UP = True
    if event.char == 'a':
        LEFT = True
    if event.char == 's':
        DOWN = True
    if event.char == 'd':
        RIGHT = True

# Function bound to <KeyRelease> event
def keyup(event):
    global UP, DOWN, LEFT, RIGHT
    if event.char == 'w':
        UP = False
    if event.char == 'a':
        LEFT = False
    if event.char == 's':
        DOWN = False
    if event.char == 'd':
        RIGHT = False

# Block of code that loops during runtime
def loop():
    global bgFrameIndex, levelStart, playerShip, playerWeapon,\
    spawnRateMin, spawnRateMax, text
    playerX, playerY = c.coords(playerShip.sprite)

    # If the game is not paused, the game will proceed normally. Otherwise, everything will be frozen i.e. paused
    if text != 'Paused':
        playerWeapon.move_bullet(CANVAS_WIDTH, CANVAS_HEIGHT, 'enemy')
        playerShip.hit_by('enemyBullet', 10, True, True)
        playerShip.hit_by('alienBullet', 25, True, True)
        playerShip.hit_by('enemy', 10, False, True)
        update_gui()
        if playerShip.health <= 0:
            lose()
        else:
            player_move()
            playerShip.rotate(mouseX, mouseY)
            if FIRING:
                playerWeapon.fire(playerX, playerY, playerShip.angle, 'playerBullet')

            drop_behavior()

            if playerShip.hit == True:
                if time.time() - playerShip.blinkTimer >= .1:
                    playerShip.blinkTimer = time.time()
                    if playerShip.blink == True:
                        playerShip.blink = False
                        c.itemconfig(playerShip.sprite, state=HIDDEN)
                    elif playerShip.blink == False:
                        playerShip.blink = True
                        c.itemconfig(playerShip.sprite, state=NORMAL)
                if time.time() - playerShip.hitTimer >= 3:
                    playerShip.hitTimer = time.time()
                    c.itemconfig(playerShip.sprite, state=NORMAL)
                    playerShip.hit = False

            background_animate()

            difficulty_spike(DIFFICULTY_RATE, LEVELS)
            spawnRate = randint(spawnRateMin, spawnRateMax)
            spawn_enemy(spawnRate)
            enemy_ai(playerX, playerY)

            root.after(1000/FPS, loop)  # Ensures that the game runs at 60 fps (not guaranteed)

# Code that runs when the player dies
def lose():
    global playerName
    root.bind('<Motion>', navigate_UI)
    root.bind('<Button-1>', UI_click)
    root.unbind('<Key>')
    root.unbind('<KeyRelease>')
    c.config(cursor='arrow')
    c.itemconfig(playerShip.sprite, state=HIDDEN)
    c.itemconfig(restartText, state=NORMAL)
    c.itemconfig(quitText, state=NORMAL)
    c.lift(UImain)
    c.lift(restartText)
    c.lift(quitText)
    playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
    for player in playerData:
        if player[0] == playerName:
            player[1] += score
    c.itemconfig(UImain, text="YOU LOSE", state=NORMAL)
    pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))

# When the game is paused or the player dies, this block of code enables navigation around the menu and hover over UI elements
def navigate_UI(event):
    global restartEnabled, quitEnabled
    if 660 < event.x < 740 and 385 < event.y < 415:
        c.config(cursor='hand1')
        c.itemconfig(restartText, font=('Roboto', 28), fill='red')
        restartEnabled = True
    elif 660 < event.x < 740 and 585 < event.y < 615:
        c.config(cursor='hand1')
        c.itemconfig(quitText, font=('Roboto', 28), fill='red')
        quitEnabled = True
    else:
        c.config(cursor='arrow')
        c.itemconfig(restartText, font=('Roboto', 24), fill='white')
        c.itemconfig(quitText, font=('Roboto', 24), fill='white')
        restartEnabled = False
        quitEnabled = False

# Sets the states of certain keybindings, Canvas objects, and variables to pause the game.
def pause(event):
    global text
    if text != 'Paused':
        text = 'Paused'
        root.bind('<Motion>', navigate_UI)
        root.bind('<Button-1>', UI_click)
        root.unbind('<Key>')
        root.unbind('<KeyRelease>')
        c.config(cursor='arrow')
        c.itemconfig(UImain, text=text, state=NORMAL)
        c.itemconfig(restartText, state=NORMAL)
        c.itemconfig(quitText, state=NORMAL)
        c.lift(UImain)
        c.lift(restartText)
        c.lift(quitText)
    elif text == 'Paused':
        text = 'Unpaused'
        root.bind('<Motion>', player_rotate)
        root.bind('<Button-1>', fireon)
        root.bind('<Key>', keydown)
        root.bind('<KeyRelease>', keyup)
        c.config(cursor='target')
        c.itemconfig(UImain, state=HIDDEN)
        c.itemconfig(restartText, state=HIDDEN)
        c.itemconfig(quitText, state=HIDDEN)
        loop()

# Code for player movement
def player_move():
    if UP:
        playerShip.move_ship(0, playerShip.movementSpeed, True)
    if LEFT:
        playerShip.move_ship(-playerShip.movementSpeed, 0, True)
    if DOWN:
        playerShip.move_ship(0, -playerShip.movementSpeed, True)
    if RIGHT:
        playerShip.move_ship(playerShip.movementSpeed, 0, True)

# Function bound to <Motion> event
def player_rotate(event):
    global mouseX, mouseY
    mouseX, mouseY = event.x, event.y

# Hides UI, rebinds keys to game bindings from UI bindings, and resets Canvas objects
def restart():
    global text
    c.itemconfig(UImain, state=HIDDEN)
    c.itemconfig(restartText, font=('Roboto', 24), fill='white', state=HIDDEN)
    c.itemconfig(quitText, font=('Roboto', 24), fill='white', state=HIDDEN)
    for item in c.find_all():
        if str(c.gettags(item)) in ["('enemy',)", "('player',)"]:
            c.delete(item)
    if text == 'Paused':
        text = 'Unpaused'
        root.bind('<Motion>', player_rotate)
        root.bind('<Button-1>', fireon)
        root.bind('<Key>', keydown)
        root.bind('<KeyRelease>', keyup)
        c.config(cursor='target')

# Spawns a random enemy
def spawn_enemy(spawnRate):
    global spawnStart
    if time.time() - spawnStart >= spawnRate:
        spawnStart = time.time()
        randX = randint(-300, 1700)
        if 0 <= randX <= 1400:
            randY = choice([randint(-300,-150),randint(950, 1100)])
        else:
            randY = choice([0, 800])
        randomEnemy = choice(enemiesList)
        if randomEnemy == 'enemyBasic':
            enemyHealth, speed, score = 100, 3, 100
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 5, 1, 2, 'single', False, False, 90, 3
        elif randomEnemy == 'enemyBouncer':
            enemyHealth, speed, score = 50, 15, 100
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 5, 1, 5, 'single', False, False, 90, 3
        elif randomEnemy == 'enemyFighter':
            enemyHealth, speed, score = 200, 4, 200
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 10, 1, 1, 'single', False, False, 90, 3
        elif randomEnemy == 'enemyCruiser':
            enemyHealth, speed, score = 800, 2, 200
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 5, 5, 3, 'spread', False, False, 90, 3
        elif randomEnemy == 'enemyWingship':
            enemyHealth, speed, score = 500, 5, 300
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 25, 1, .25, 'single', False, False, 90, 3
        elif randomEnemy == 'alienShip':
            enemyHealth, speed, score = 1500, 3, 400
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 25, 25, 2, 'spread', False, False, 90, 4
        elif randomEnemy == 'alienRevenant':
            enemyHealth, speed, score = 10000, .5, 1000
            sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots = 'redLaser', 10, 25, 5, 'spread', False, False, 180, 18
        newEnemy = Ship(c, randX, randY, enemyHealth, randomEnemy, speed, score, 'enemy')
        newEnemy.killed = False
        newEnemyWeapon = Weapon(c, sprite, bulletSpeed, damage, fireRate, type, chase, piercing, spreadAngle, shots)

        # Each new enemy has a Ship instance and Weapon instance that get appended to lists
        existingEnemies.append(newEnemy)
        enemyWeapons.append(newEnemyWeapon)

# Initialization of game when player presses <space> or presses "Restart" in UI
def start(event):
    global drops, enemiesList, enemyWeapons, existingEnemies, item, level, levelStart, mouseX, mouseY,\
           playerShip, playerWeapon, score, spawnRateMin, spawnRateMax, spawnStart, trembleStart

    c.config(cursor='target')

    mouseX, mouseY = 0, 0
    centerX, centerY = 640, 360
    score = 0
    existingEnemies = []
    enemyWeapons = []
    drops = []
    level = 0
    enemiesList = LEVELS[level]
    spawnRateMin, spawnRateMax = SPAWN_RATES[level][0], SPAWN_RATES[level][1]

    playerShip = Ship(c, centerX, centerY, PLAYER_HEALTH, 'playerShip', 10, 0, 'player')
    playerWeapon = Weapon(c, 'blueLaser', 30, 10, .25, 'single', False, False)

    for line in startText:
        c.itemconfig(line, state=HIDDEN)
    c.itemconfig(healthDisplay, state=NORMAL)
    c.itemconfig(scoreDisplay, state=NORMAL)

    spawnStart = time.time()
    levelStart = time.time()
    trembleStart = time.time()

    root.unbind('<space>')
    root.bind('<Key>', keydown)  # Key down
    root.bind('<KeyRelease>', keyup)  # Key release
    root.bind('<Motion>', player_rotate)  # Mouse movement
    root.bind('<Button-1>', fireon)  # Mouse click
    root.bind('<ButtonRelease-1>', fireoff)  # Mouse Release
    root.bind('<Escape>', pause)

    loop()

# Defines what happens if you click on the "Restart" or "Quit" options
def UI_click(event):
    global restartEnabled, quitEnabled
    if restartEnabled:
        restart()
        start(event)
    elif quitEnabled:
        root.destroy()
        if DEVELOPER_MODE:
            devWindow.destroy()

# Updates the health and kills display
def update_gui():
    healthText = "Health:", playerShip.health
    c.itemconfig(healthDisplay, text=healthText)
    c.tag_raise(healthDisplay)

    scoreText = "Score:", score
    c.itemconfig(scoreDisplay, text=scoreText)
    c.tag_raise(scoreDisplay)

# Initialization of Tkinter canvas objects and global variables
c = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

backgroundImage = PhotoImage(file="images/%s/0.gif" % BACKGROUND_NAME)
background = c.create_image(0, 0, image=backgroundImage, anchor='nw', tag='gui')

BACKGROUND_FRAMES = []
for number in range(NUMBER_OF_FRAMES):
    newFrame = PhotoImage(file="images/%s/%s.gif" % (BACKGROUND_NAME, number))
    BACKGROUND_FRAMES.append(newFrame)
bgFrameIndex = 0

c.pack()

# List of potential upgrades that enemies drop; repeats dictate a higher chance of being dropped
potentialDrops = ['health20', 'health20', 'health20', 'health20', 'health20', 'health20', 'health20', 'health20', 'health20', 'health20',\
                  'health50', 'health50', 'health50',\
                  'spreadShot30', 'spreadShot30', 'spreadShot30', 'spreadShot30', 'spreadShot30',\
                  'spreadShot60', 'spreadShot60', 'spreadShot60',\
                  'spreadShot90',\
                  'spreadShot120',\
                  'piercing', 'piercing', 'piercing', 'piercing', 'piercing',\
                  'rapidFire', 'rapidFire', 'rapidFire',\
                  'damageIncrease1', 'damageIncrease1', 'damageIncrease1', 'damageIncrease1', 'damageIncrease1',\
                  'damageIncrease2', 'damageIncrease2',\
                  'speedUp', 'speedUp', 'speedUp', 'speedUp', 'speedUp',\
                  'chaser'
                  ]

startText = []
startTextFile = open("data/startText.txt")
text = startTextFile.readlines()
for line in text:
    startTextLine = c.create_text(700, 210+30*text.index(line), text=line, font=('Roboto', 18), fill='white', justify=CENTER)
    startText.append(startTextLine)

healthDisplay = c.create_text(20, 775, text="Health: 100", font='Roboto', fill='white', anchor='sw', tag='gui')
c.itemconfig(healthDisplay, state=HIDDEN)

scoreDisplay = c.create_text(700, 775, text="Score: 0", font='Roboto', fill='white', anchor='se', tag='gui')
c.itemconfig(scoreDisplay, state=HIDDEN)

UImain = c.create_text(700, 200, text="Placeholder", fill='white', font=('Roboto', 30), tag='gui')
c.itemconfig(UImain, state=HIDDEN)

restartText = c.create_text(700, 400, text="Restart", fill='white', font=('Roboto', 24), tag='gui')
c.itemconfig(restartText, state=HIDDEN)

quitText = c.create_text(700, 600, text="Quit", fill='white', font=('Roboto', 24), tag='gui')
c.itemconfig(quitText, state=HIDDEN)

root.bind('<space>', start)

root.mainloop()
