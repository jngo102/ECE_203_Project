__author__ = 'Jason Ngo'
# Contains variables and classes that are referenced by main.py

from Tkinter import *
from math import *
import os
import time

CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 800
BACKGROUND_NAME = 'stars'
NUMBER_OF_FRAMES = len(os.listdir("images/%s" % BACKGROUND_NAME))
FPS = 60    # Number of times per second that loop() function will run in main.py
FIRING = False
DIFFICULTY_RATE = 60
PLAYER_HEALTH = 100

DEVELOPER_MODE = True

# Each levels defines the kinds of enemies that the player will encounter as they progress through the game
LEVELS = []
LEVELS.append(['enemyBasic']*7 + ['enemyBouncer']*3)
LEVELS.append(['enemyBasic']*4 + ['enemyBouncer']*4 + ['enemyFighter']*2)
LEVELS.append(['enemyBasic']*2 + ['enemyBouncer']*4 + ['enemyFighter']*3 + ['enemyCruiser']*2)
LEVELS.append(['enemyBouncer'])
LEVELS.append(['enemyBasic'] + ['enemyBouncer']*2 + ['enemyFighter']*5 + ['enemyCruiser'] + ['enemyWingship'])
LEVELS.append(['enemyBouncer'] + ['enemyFighter'] + ['enemyCruiser'] + ['enemyWingship'] + ['alienShip'])
LEVELS.append(['enemyBouncer']*11 + ['alienShip']*1)
LEVELS.append(['alienShip']*9 + ['alienRevenant'])
LEVELS.append(['alienRevenant'])

SPAWN_RATES = [ [5,20], [4,15], [4,12], [1,2], [4,10], [3,8], [1,2], [9,15], [15,20] ]

# Boolean variables to denote direction of movement
UP = False
LEFT = False
DOWN = False
RIGHT = False

class Bullet:
    def __init__(self, canvas, x, y, spriteImage, angle, piercing=False, tag='enemyBullet'):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.piercing = piercing
        self.spriteImage = PhotoImage(file="images/%s/%d.gif" % (spriteImage, angle))
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.spriteImage, tag=tag)

    def collide_with(self, collideTag='enemy'):
        imgWidth = self.spriteImage.width()
        imgHeight = self.spriteImage.height()
        bulletX, bulletY = self.canvas.coords(self.sprite)
        for item in self.canvas.find_overlapping(bulletX-imgWidth/2,bulletX+imgWidth/2,bulletY-imgHeight/2,bulletY+imgHeight/2):
            if not self.piercing and str(self.canvas.gettags(item)) == "('%s',)" % collideTag:
                self.canvas.delete(self.sprite)

# Drop class for player upgrades dropped by enemies
class Drop:
    def __init__(self, canvas, dropType, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dropType = dropType
        self.spriteImage = PhotoImage(file="images/drops/%s.gif" % self.dropType)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.spriteImage)
        self.pickedUp = False

    def picked_up(self):
        imgWidth = self.spriteImage.width()
        imgHeight = self.spriteImage.height()
        try:
            dropX, dropY = self.canvas.coords(self.sprite)
            for item in self.canvas.find_overlapping(dropX-imgWidth/2, dropY-imgHeight/2, dropX+imgWidth/2, dropY+imgHeight/2):
                if str(self.canvas.gettags(item)) == "('player',)":
                    self.canvas.delete(self.sprite)
                    self.pickedUp = True
        except:
            pass

# Ship class used to create and move ships
class Ship:
    def __init__(self, canvas, x, y, health=100, shipName='playerShip', movementSpeed=5, score=100, tag='enemy'):
        self.canvas = canvas
        self.health = health
        self.shipName = shipName
        self.movementSpeed = movementSpeed
        self.score = score
        self.tag = tag
        self.x = x
        self.y = y
        self.hit = False
        self.blink = False
        self.hitTimer = time.time()
        self.blinkTimer = time.time()
        self.bulletsTouched = []
        self.dropped = False
        self.spriteImage = PhotoImage(file="images/%s/0.gif" % (self.shipName))
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.spriteImage, tag=self.tag)

    # Method to control what happens when a Ship instance collides with a certain object
    def hit_by(self, tag='enemyBullet', damage=10, delete=True, invincible=False):
        imgWidth = self.spriteImage.width()
        imgHeight = self.spriteImage.height()
        centerX, centerY = self.canvas.coords(self.sprite)
        for item in self.canvas.find_overlapping(centerX-imgWidth/4, centerY-imgHeight/4, centerX+imgWidth/4, centerY+imgHeight/4):
            if str(self.canvas.gettags(item)) == "('%s',)" % tag:
                if delete:
                    self.canvas.delete(item)
                if invincible:
                    if self.hit == False:
                        self.health -= damage
                        self.hit = True
                        self.hitTimer = time.time()
                        self.blinkTimer = time.time()
                        self.blink = True
                    if time.time() - self.blinkTimer >= .5:
                        self.blinkTimer = time.time()
                        if self.blink == True:
                            self.blink = False
                        elif self.blink == False:
                            self.blink = True
                elif self.shipName != 'playerShip' and item not in self.bulletsTouched:
                    self.bulletsTouched.append(item)
                    self.health -= damage
        for item in self.bulletsTouched:
            if item not in self.canvas.find_overlapping(centerX-imgWidth/4, centerY-imgHeight/4, centerX+imgWidth/4, centerY+imgHeight/4):
                del self.bulletsTouched[self.bulletsTouched.index(item)]

    # Used exclusively for enemies; defines how a Ship instance moves around the canvas
    def movement_pattern(self, targetX, targetY, pattern='toward', until=True, distance=200):
        if pattern == 'toward':     # Ship moves towards a target
            self.x, self.y = self.canvas.coords(self.sprite)
            dx,dy = targetX - self.x, self.y - targetY
            magnitude = sqrt((dx**2) + (dy**2))
            if magnitude <= distance:
                pass
            else:
                (self.trajectoryX, self.trajectoryY) = (dx/magnitude, dy/magnitude)
                self.canvas.move(self.sprite, self.movementSpeed*self.trajectoryX, self.movementSpeed*-self.trajectoryY)
        elif pattern == 'bounce':   # Ship bounces off Canvas borders
            self.x, self.y = self.canvas.coords(self.sprite)
            if self.x <= 0 or self.x >= 1400:
                self.trajectoryX = -self.trajectoryX
            if self.y <= 0 or self.y >= 800:
                self.trajectoryY = -self.trajectoryY
            self.canvas.move(self.sprite, self.movementSpeed*self.trajectoryX, self.movementSpeed*-self.trajectoryY)

    # Used exclusively for the player; controls Ship movement along the x- and y-axes
    def move_ship(self, xSpeed=5, ySpeed=5, collide=False, canvasWidth=1400, canvasHeight=800):
        self.canvas.move(self.sprite, xSpeed, -ySpeed)
        if collide:
            if self.sprite not in self.canvas.find_enclosed(0, 0, canvasWidth, canvasHeight):
                self.canvas.move(self.sprite, -xSpeed, ySpeed)

    # Rotates Ship instance towards a target
    def rotate(self, targetX, targetY):
        self.x, self.y = self.canvas.coords(self.sprite)
        self.dx, self.dy = targetX - self.x, self.y - targetY
        if self.dx == 0 and self.dy > 0:
            self.angle = 90
        elif self.dx == 0 and self.dy < 0:
            self.angle = 270
        elif self.dx == 0 and self.dy == 0:
            self.angle = 0
        elif self.dx > 0 and self.dy < 0:
            self.angle = 360 + degrees(atan(self.dy / self.dx))
        elif self.dx < 0:
            self.angle = 180 + degrees(atan(self.dy / self.dx))
        else:
            self.angle = degrees(atan(self.dy / self.dx))
        self.spriteImage = PhotoImage(file='images/%s/%d.gif' % (self.shipName, int(self.angle)))
        self.canvas.itemconfig(self.sprite, image=self.spriteImage)

# Weapon class used to create and fire ship weapons
class Weapon:
    def __init__(self, canvas, sprite='blueLaser', bulletSpeed=10, damage=10, fireRate=0.5, type='single', chase=False, piercing=False, spreadAngle=90, shots=3):
        self.canvas = canvas
        self.sprite = sprite
        self.bulletSpeed = bulletSpeed
        self.damage = damage
        self.fireRate = fireRate
        self.chase = chase
        self.type = type
        self.piercing = piercing
        self.spreadAngle = spreadAngle
        self.shots = shots
        self.bullets = []
        self.startTime = time.time()

    # Fires a bullet or number of bullets depending on Weapon type
    def fire(self, posx=640, posy=360, angle=0, bulletTag='enemyBullet'):
        if time.time() - self.startTime >= self.fireRate:
            self.startTime = time.time()
            if self.type == 'single':
                self.weaponImage = PhotoImage(file='images/%s/%d.gif' % (self.sprite, angle))
                bullet = Bullet(self.canvas, posx, posy, self.sprite, angle, self.piercing, bulletTag)
                if self.piercing:
                    self.canvas.itemconfig(bullet, tag='piercing')
                dx,dy = cos(radians(angle)), sin(radians(angle))
                magnitude = sqrt((dx**2) + (dy**2))
                bullet.trajectoryX, bullet.trajectoryY = (dx/magnitude, -dy/magnitude)
                self.bullets.append(bullet)
            elif self.type == 'spread':
                minAngle = int(angle - self.spreadAngle / 2)
                angleInterval = int(self.spreadAngle / self.shots)
                maxAngle = int(angle + self.spreadAngle / 2)
                for angle in range(minAngle, maxAngle, angleInterval):
                    if angle < 0:
                        angle += 360
                    elif angle > 360:
                        angle -= 360
                    self.weaponImage = PhotoImage(file="images/%s/%d.gif" % (self.sprite, angle))
                    bullet = Bullet(self.canvas, posx, posy, self.sprite, angle, self.piercing, bulletTag)
                    if self.piercing:
                        self.canvas.itemconfig(bullet, tag='piercing')
                    dx, dy = cos(radians(angle)), sin(radians(angle))
                    magnitude = sqrt((dx**2) + (dy**2))
                    bullet.trajectoryX, bullet.trajectoryY = (dx/magnitude, -dy/magnitude)
                    self.bullets.append(bullet)

    # Moves each bullet in the Weapons bullet dictionary and deletes them if they exit the Canvas
    def move_bullet(self, canvasWidth, canvasHeight, targetTag='enemy'):
        bulletsToDelete = []
        for bullet in self.bullets:
            if self.chase:
                closestDistance = float('inf')
                if len(self.canvas.find_withtag(targetTag)) != 0:
                    try:
                        bulletX, bulletY = self.canvas.coords(bullet.sprite)
                        for item in self.canvas.find_withtag(targetTag):
                            itemX, itemY = self.canvas.coords(item)
                            vectorX, vectorY = itemX - bulletX, bulletY - itemY
                            distance = sqrt(vectorX**2 + vectorY**2)
                            if distance <= closestDistance:
                                closestDistance = distance
                                targetdx, targetdy = vectorX, vectorY
                        if targetdx == 0 and targetdy > 0:
                            targetAngle = 90
                        elif targetdx == 0 and targetdy < 0:
                            targetAngle = 270
                        elif targetdx == 0 and targetdy == 0:
                            targetAngle = 0
                        elif targetdx > 0 and targetdy < 0:
                            targetAngle = 360 + degrees(atan(targetdy / targetdx))
                        elif targetdx < 0:
                            targetAngle = 180 + degrees(atan(targetdy / targetdx))
                        else:
                            targetAngle = degrees(atan(targetdy / targetdx))

                        if bullet.angle > targetAngle and bullet.angle - targetAngle > 180 or\
                            targetAngle > bullet.angle and targetAngle - bullet.angle < 180:
                            dTheta = self.bulletSpeed * 0.5
                        elif bullet.angle > targetAngle and bullet.angle - targetAngle < 180 or\
                            targetAngle > bullet.angle and targetAngle - bullet.angle > 180:
                            dTheta = -self.bulletSpeed * 0.5
                        bullet.angle += dTheta
                        if bullet.angle > 360:
                            bullet.angle -= 360
                        elif bullet.angle < 0:
                            bullet.angle += 360
                        dx, dy = cos(radians(bullet.angle)), sin(radians(bullet.angle))
                        magnitude = sqrt((dx**2) + (dy**2))
                        bullet.trajectoryX, bullet.trajectoryY = dx/magnitude, -dy/magnitude
                        bullet.bulletImage = PhotoImage(file="images/%s/%d.gif" % (self.sprite, bullet.angle))
                        self.canvas.itemconfig(bullet.sprite, image=bullet.bulletImage)
                    except:
                        pass
            self.canvas.move(bullet.sprite, self.bulletSpeed*bullet.trajectoryX, self.bulletSpeed*bullet.trajectoryY)
            if bullet.sprite not in self.canvas.find_overlapping(-1000, -1000, canvasWidth+1000, canvasHeight+1000):
                self.canvas.delete(bullet.sprite)
                del self.bullets[self.bullets.index(bullet)]
