import pygame, random, math  # imports pygame module
from pygame.draw import line, circle, rect  # will make it easier to use pygame functions

pygame.init()  # initializes pygame
screen = pygame.display.set_mode([600, 600])  # creates a window of size 800 x 600
done = False  # this variable lets you quit the game by closing your window
clock = pygame.time.Clock()  # this lets you adjust the speed of the program

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
leftPress = False  # Control variable for moving to the side
rightPress = False  # Control variable for moving to the side
font = pygame.font.SysFont("Arial", 26)  # Font for the score
score = 0
jumperImage = pygame.image.load("pixil-frame-0.png").convert()  # Calls the image of the jumper from the folder
jumperImage = pygame.transform.scale(jumperImage, (30, 50))     # Transforms the size of the jumper
jumperImage.set_colorkey(BLACK)                                 # Erases the background
coinImage = pygame.image.load("Coin.png").convert()             # Calls the image of the coin from the folder
coinImage = pygame.transform.scale(coinImage, (60, 60))         # Transforms the size of the coin
coinImage.set_colorkey(BLACK)                                   # Erases the background
platformImage = pygame.image.load("Platform.png").convert()     # Calls the image of the platform from the folder
platformImage = pygame.transform.scale(platformImage, (120, 60)) # Changes the shape of the platform
platformImage.set_colorkey(BLACK)                                   # Erases the background
backgroundImage = pygame.image.load("background.png").convert()     #Calls the background image from the folder
backgroundImage = pygame.transform.scale(backgroundImage, (600, 600))   # Changes the background size
gameStart = pygame.image.load("StartGame.png").convert()            # Calls the start screen from the folder
gameStart = pygame.transform.scale(gameStart, (600, 600))           #Changes the size
gameOver = pygame.image.load("gameOver.png").convert()              # Calls the game over screen from the folder
gameOver = pygame.transform.scale(gameOver, (600, 600))             # Changes the size of the game over screen
jumpNoise = pygame.mixer.Sound("boing.wav")                     # Adds the jumping noise
walk = pygame.mixer.Sound("CarWalk.wav")            # Adds the walking noise
theme = pygame.mixer.Sound("theme.wav") # Adds the theme noise
coinGet = pygame.mixer.Sound("floop.wav")# Adds the coin getting noise
diedNoise = pygame.mixer.Sound("GameOver.wav")# Adds the dying noise
scoreImage = pygame.image.load("score.png").convert()     # Calls the image of the platform from the folder
scoreImage = pygame.transform.scale(scoreImage, (100, 50)) # Changes the shape of the platform
scoreImage.set_colorkey(BLACK)                                   # Erases the background
pygame.font.get_fonts()
playerHeight = 40 # height of player, for proper collision
coinAmount = 1 # multiplier for your coins
i = 0 # range for tables
platCount = 0 #for counting and resetting tables, (Collision)
platAmount = 10 #Amount of platforms
hasJump = False #Making sure the player has a jump so they can only jump once
gamePlay = False #For making the actual game appear as apposed to the start of game over screen
startedGame = True #For making the title screen, if its off, the game over screen appears
hasDied = False #checks if you have died, if so it makes the game over screen


# Change self.x and self.y back after done testing


def points(score, coinAmount): #Function for determining the score per round
    return ((score * coinAmount) // 2)

def gameScreen():
    if startedGame == True:
        screen.blit(gameStart, (0, 0))
    elif hasDied == True:
        screen.blit(gameOver, (0, 0))
        diedNoise.play()


def newGame():
    # reset the score to zero
    # create a new platform and a new jumper and a new coin
    global score
    score = 0
    jumper.makeNew()
    coin.draw()
    for i in range(0, platAmount):
        platTable[i].makeNew()


def drawScore():
    global finalSum, finalScore
    finalScore = points(score, coinAmount)
    screen.blit(scoreImage, (30, 30))
    label = font.render(" {}".format(finalScore), 1, RED)  # Draws the
    screen.blit(label, (130, 39))
    # draw the score to the screen


class JUMPER():
    def __init__(self):
        global onPlat
        self.x = 200  # Jumpers starting x
        self.y = 510  # Jumpers starting y
        self.gravity = 0.07  # don't change
        self.jumpSpeed = -8  # don't change
        self.onPlat = False
        self.speedY = 0

    def makeNew(self):
        self.speedY = 0  # start off with zero falling speed
        self.y = -600  # Restarts the jumper at the highest 7 position
        self.x = 300  # Restarts the jumper at x
        # set the jumper's initial position here

    def draw(self):  # Draws the circle that is used as the jumper
        for i in range(0, platAmount):
            screen.blit(jumperImage, (self.x, self.y))

    def move(self):
        global onPlat, hasDied, gamePlay, startedGame
        # these lines add gravity. Don't change these
        if self.onPlat == False: #Makes gravity if off platform
            self.speedY += self.gravity
        else:
            self.speedY = 0 #keeps gravity if on platform
            self.y += 0
        if self.onPlat: #lets gravity function work off of platform
            self.onPlat = False
        if self.y >= 600: #Kills you, resets coins, makes gameover screen appear if you die
            hasDied = True
            startedGame = False
            gamePlay = False
            coin.x = random.randint(50, 550)
            coin.y = random.randint(50, 550)

        # check if the jumper falls to the bottom of the screen and reset the game
        global leftClick, hasJump, jumpNoise
        if hasJump == True:
            if clicks[0] and not leftClick:
                self.speedY += self.jumpSpeed
                leftClick = True
                hasJump = False

    # check if the left mouse button was clicked (use a control variable so it only registers one click, not a held click)
    # if ...it's clicked:
    def go(self):  # Calls the draw and move variables into one class for clarity
        global collected
        jumper.draw()
        jumper.move()


class PLATFORM():
    def __init__(self):
        self.x = random.randint(0, 600)  # PLatforms x coordinates starts at a random point
        self.width = 120  # don't change, the width of the platform
        self.speedX = 5  # how fast it moves horizontally. Don't change
        self.speedY = random.uniform(0.15, 0.35)  # Vertical Speed
        self.y = random.randint(0, 200)

    def makeNew(self):
        self.x = random.randint(0, 600)
        self.speedY = random.uniform(0.10, 0.35)  # don't change
        self.width = 100
        self.y = random.randint(-200, 0)
        # initializes a platform at right side of screen
        # make a random x-location from the top of the screen

    def draw(self):  # Draws the platform to jump on
        screen.blit(platformImage, (self.x, int(self.y)))

    def move(self):
        self.y += self.speedY
        if self.y > 600:
            self.makeNew()
        # moves the platform downwards at the given speed

    def checkHit(self):
        global onPlat, playErrorNoise, score, platCount, hasJump
        if ((self.x < jumper.x < (self.x + self.width)) and (self.y < jumper.y + playerHeight < self.y + 10) and jumper.speedY > 0): #Checks the to see if the jumper is on the platform
            jumper.onPlat = True #Makes onplat true
            walk.play() #plays sound effect
            score += 10 #Adds score
            hasJump = True #Gives a jump
        for i in range(0, platAmount):
            if not ((platTable[i].x < jumper.x < (platTable[i].x + platTable[i].width)) or not (
                    platTable[i].y < jumper.y + playerHeight < platTable[i].y + 10) or jumper.speedY > 0):
                platCount += 1
        if platCount == 10:
            jumper.onPlat = False
        platCount = 0

    def go(self):
        # move the platform
        # draw the platform
        # makes a new platform if it falls
        self.checkHit()
        self.draw()
        self.move()


class COIN():  # Makes a new coint and draws it
    def __init__(self):
        global collected
        self.x = random.randint(50, 550)  # Randomly spawns a coins x coord
        self.y = random.randint(50, 550)  # Randomly spawns a coins y coord
        self.collected = False

    def checkIntercept(self):  # Checks to see if the intercept, if they do adds 100 points and makes a new one
        global score, collected, coinAmount
        if (self.x < jumper.x < (self.x + 60)) and ((self.y) < jumper.y < (self.y + 60)):
            score += 1000
            coinAmount += 1
            self.collected = True
            coinGet.play()

    def draw(self):  # Draws a circle for the coin
        global collected, hasDied
        screen.blit(coinImage, (self.x, self.y))
        self.checkIntercept()
        if self.collected:
            self.collected = False
            coinGet.play()
            self.x = random.randint(50, 550)  # Randomly spawns a coins x coord
            self.y = random.randint(50, 550)  # Randomly spawns a coins y coord


# global variables are here:
jumper = JUMPER()
coin = COIN()
leftClick = False  # your click control variable

# here's a font you can use, but you are free to use others:
myFont = pygame.font.SysFont('Comic Sans MS', 15)
theme.play()

platTable = []  # stores the 10 platforms in the game and brings them out randomly
for i in range(0, platAmount):
    platTable.append(PLATFORM())
# start a new game:


# MAIN LOOP
while not done:  # a WHILE loop. PYGAME works by continuously looping and redrawing the sreen
    # just like your TV refreshes the screen 60 times each second

    #######################

    # your code goes here #
    for i in range(0, platAmount):
        # if platTable[i].y >= 600: #Makes a new platform if it falls below the bottom
        for i in range(0, platAmount):
            platTable[i].go()
    #######################
    if gamePlay == False: #Makes the game screens with the gamescreen function
        gameScreen()
    else:

        screen.blit(backgroundImage, (0, 0)) #Makes the regular background
        xMouse, yMouse = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()

        # call the go() functions for the jumper and the platform

        jumper.go()
        coin.draw()
        drawScore()
        for i in range(0, platAmount):
            platTable[i].draw()
            if (jumper.speedY > 0):
                platTable[i].checkHit()
        # check your mouse control variable
        if not clicks[0]:
            leftClick = False
        #Makes jumper, coins and score, makes the 10 platforms in a list

    ####################

    if jumper.onPlat == False:
        jumper.speedY += jumper.gravity  # Moves the jumper in relation to the gravity
        jumper.y += jumper.speedY
    if jumper.y >= 800:  # Starts a new game if you go below the screen
        jumper.speedY = 0
        # newGame()
    if jumper.x >= 600:  # Puts them on the opposite side of the screen if they go off
        jumper.x = 0
    elif jumper.x <= 0:
        jumper.x = 600

    # end of your code #
    if rightPress:
        jumper.x += 5
    if leftPress:
        jumper.x -= 5

    ####################

    # key functions                             # this code allows you to close the window and end the program

    for event in pygame.event.get():
        # Controls the person moving from left to right
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                rightPress = True
            if event.key == pygame.K_LEFT:
                leftPress = True
            if event.key == pygame.K_SPACE:
                if hasJump == True:
                    jumper.speedY += jumper.jumpSpeed
                    jumpNoise.play()
                    hasJump = False
            if event.key == pygame.K_r:
                newGame()
                gamePlay = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftPress = False
            if event.key == pygame.K_RIGHT:
                rightPress = False

    pygame.display.flip()  # this line draws everything into the window all at once
    clock.tick(60)  # this line limits the frames per second to 60

pygame.quit()
