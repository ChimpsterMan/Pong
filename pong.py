import pygame
import random
import keyboard

#init windows and vars
pygame.init()

width = 800
height = 600

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()
fps = 60
crashed = False

phase = 0
countDown = fps*3
cNum = 3

#colors and images
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#ehh players
p1Score = 0
p2Score = 0

#object def
class Player:
    
    def __init__ (self, new_x, new_y, new_pNum):
        self.w = width/53
        self.l = height/5
        self.x = new_x-self.w/2
        self.y = new_y-self.l/2
        self.pNum = new_pNum
        self.velocity = 0
        self.speedNorm = 8
        self.speed = self.speedNorm

    def move (self, direction):
        if not (self.y + self.speed*direction < 0 or self.y + self.l + self.speed*direction > height):
            self.velocity = self.speed*direction
            self.y += self.speed*direction
            #self.speed *= 1.03

    def update (self):

        #self.speedNorm *= 0.9996
        self.velocity = 0
        
    def draw (self):
        pygame.draw.rect(gameDisplay, red, (self.x,self.y,self.w,self.l))

class Ball:
    
    def __init__ (self, new_x = width/2, new_y = height/2, new_size = 15, new_vX = float(random.randint(0,1)*3), new_vY = (float(random.randint(-100,100))/100)*5):
        self.x = new_x
        self.y = new_y
        self.size = new_size
        if (new_vX == 0):
            new_vX = -3
        self.vX = new_vX
        self.vY = new_vY
        
    def update (self, p1, p2):
        global p1Score, p2Score
        
        #walls
        if not (self.x + self.vX + self.size > width or self.x + self.vX - self.size < 0):
            self.x += self.vX
        elif self.x + self.vX + self.size > width:
            self.x = width - self.size
            self.vX *= -1
            p1Score += 1
            newRound()
        else:
            self.x = 0 + self.size
            self.vX *= -1
            p2Score += 1
            newRound()
            
        if not (self.y + self.vY + self.size > height or self.y + self.vY - self.size < 0):
            self.y += self.vY
        elif self.y + self.vY + self.size > height:
            self.y = height - self.size
            self.vY *= -1
        else:
            self.y = 0 + self.size
            self.vY *= -1

        #players
        if not (((self.x + self.vX + self.size > p1.x and p1.x > width/2) or (self.x + self.vX - self.size < p1.x + p1.w and p1.x < width/2)) and (self.y + self.size > p1.y and self.y < p1.y + p1.l)):
            self.x += self.vX
        elif (self.x + self.vX + self.size > p1.x and p1.x > width/2) and (self.y + self.size > p1.y and self.y < p1.y + p1.l):
            self.x = p1.x - self.size
            self.vX *= -1
            self.vY += p1.velocity*0.5
        else:
            self.x = p1.x + p1.w + self.size
            self.vX *= -1
            self.vY += p1.velocity*0.5
            
        if not (((self.x + self.vX + self.size > p2.x and p2.x > width/2) or (self.x + self.vX - self.size < p2.x + p2.w and p2.x < width/2)) and (self.y + self.size > p2.y and self.y < p2.y + p2.l)):
            self.x += self.vX
        elif (self.x + self.vX + self.size > p2.x and p2.x > width/2) and (self.y + self.size > p2.y and self.y < p2.y + p2.l):
            self.x = p2.x - self.size
            self.vX *= -1
            self.vY += p2.velocity*0.5
        else:
            self.x = p2.x + p2.w + self.size
            self.vX *= -1
            self.vY += p2.velocity*0.5
        
        self.vX *= 1.0003

    def draw (self):
        pygame.draw.circle(gameDisplay, white, (int(self.x),int(self.y)), self.size)

class OnScreen:
    
    def __init__ (self):
        self.font = pygame.font.SysFont("comicsansms", 72)

    def addScore (self, player):
        if (player == 1):
            p1Score += 1
        elif (player == 2):
            p2Score += 1

    def draw (self):
        self.font = pygame.font.SysFont("comicsansms", 72)
        
        self.text = self.font.render("Pong", True, (0, 128, 0))
        gameDisplay.blit(self.text, (width*0.5 - self.text.get_width()/2, height*0.05 - self.text.get_height()/2))

        self.font = pygame.font.SysFont("comicsansms", 30)
        
        self.text = self.font.render("Player 1: " + str(p1Score), True, (0, 128, 0))
        gameDisplay.blit(self.text, (width*0.15 - self.text.get_width()/2, height*0.05 - self.text.get_height()/2))

        self.text = self.font.render("Player 2: " + str(p2Score), True, (0, 128, 0))
        gameDisplay.blit(self.text, (width*0.85 - self.text.get_width()/2, height*0.05 - self.text.get_height()/2))
    
#game setup
ball = Ball()

player1 = Player(20, height/2, 1)
player2 = Player(width-20, height/2, 2)
screen = OnScreen()

def newRound ():
    global phase, countDown, cNum, ball, player1, player2
    phase = 0
    countDown = fps*3
    cNum = 3
    ball = Ball()
    player1 = Player(20, height/2, 1)
    player2 = Player(width-20, height/2, 2)

#main game loop
while not crashed:
    #game data
    gameDisplay.fill(black)
    screen.draw()

    if (phase == 0):
        text = screen.font.render(str(cNum+1), True, (0, 128, 0))
        gameDisplay.blit(text, (width*0.5 - text.get_width()/2, height*0.3 - text.get_height()/2))
        if (countDown % fps == 0):
            cNum -= 1
            if (cNum < 0):
                phase = 1
        countDown -= 1
            
    if (phase == 1):
        ball.update(player1,player2)
        player1.update()
        player2.update()

    #keyboard input
    if (keyboard.is_pressed('w')):
        player1.move(-1)
    elif (keyboard.is_pressed('s')):
        player1.move(1)
    elif (keyboard.is_pressed('up')):
        player2.move(-1)
    elif (keyboard.is_pressed('down')):
        player2.move(1)
        
    #graphics
    player1.draw()
    player2.draw()
    ball.draw()
    
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
    
