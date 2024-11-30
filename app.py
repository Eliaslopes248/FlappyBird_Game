import pygame
import math
import time
import random


pygame.init()

# screen dimensions
screenW, screenH = 350, 530
screen = pygame.display.set_mode((screenW,screenH))

# background
rawbg = pygame.image.load('images\\bg.png')
bg = pygame.transform.scale(rawbg,(screenW,screenH))

# bird sprite
class player:

    # gravity logic
    velocityY = 0
    gravity = .035
    maxflap = 30
    
    
    

    def __init__(self,urlList,x,y,width,height):
        self.spritelist = urlList
        self.currImg = pygame.image.load(urlList[0])
        self.x = x
        self.y = y
        self.middle = y
        self.width = width
        self.height = height
        

    def draw(self):
        adjustedImg = pygame.transform.scale(self.currImg,(self.width,self.height))
        screen.blit(adjustedImg,(self.x,self.y))

    def falling(self,jumping):

        if jumping:
            self.currImg = pygame.image.load(self.spritelist[1])
            player.velocityY = -2.5
            self.y += player.velocityY
            player.velocityY += player.gravity

        elif jumping == None:
            pass 
        else:
            
            self.y += player.velocityY
            player.velocityY += player.gravity
            self.currImg = pygame.image.load(self.spritelist[0])

class tubes:

    def __init__(self,url,x,y,width,height,type):
        self.rawImg = pygame.image.load(url)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type

    def draw(self):
        adjustedImg = pygame.transform.scale(self.rawImg,(self.width,self.height))
        screen.blit(adjustedImg,(self.x,self.y))

    def moving(self,running):
        if running:
            self.x -= 1

            if self.type == 'down':
                if self.x < -80:
                    self.x = screenW
                    self.height = random.randint(100,200)
            else:
                if self.x < -80:
                    self.x = screenW
                    self.height = random.randint(100,200)
                    self.y = screenH - self.height

    def reset(self):
        if self.type == 'down':
            self.x = screenW
            self.height = random.randint(100,200)
        else:
            self.x = screenW
            self.height = random.randint(100,200)
            self.y = screenH - self.height
        
# test tubes
tubeH = random.randint(120,220)
tubeW = 60
downtube = tubes('images\\downtube.png',270,0,tubeW,tubeH,'down')

randomX = random.randint(250,300)
tubeH = random.randint(120,220)
tubeW = 60
uptube = tubes('images\\uptube.png',randomX,screenH - tubeH,tubeW,tubeH,'up')

#all tubes
tubeList = [uptube,downtube]      

#check for collision
def isCollision(tubes, player):
    for tube in tubes:
    
        if (player.x < tube.x + tube.width and 
            player.x + player.width > tube.x and 
            player.y < tube.y + tube.height and 
            player.y + player.height > tube.y):
            return True

    if player.y > screenH + 300:
        return True

    return False

            

            




sprites = ['images\\idle.png', 'images\\jump.png','images\\down.png']
bird = player(sprites,30,screenH//2,55,50)
is_jumping = None

# game loop
running = True
gameStart = False

title = pygame.display.set_caption("FlappyBird by Elias Lopes")

# player score
score = 0

text_font = pygame.font.SysFont("Arial",30)

def draw_score(text,font,color,x,y):
    global screen
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

gamescore = 0
while running:
    
    screen.fill((0,20,100))
    screen.blit(bg,(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                gameStart = True
                is_jumping = True
                
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE:
                gameStart = True
                is_jumping = False
 
    
    downtube.draw()
    uptube.draw()
    downtube.moving(gameStart)
    uptube.moving(gameStart)

    bird.draw()
     

    if isCollision(tubeList,bird):
        gameStart = False
        bird.y = screenH // 2
        score = 0
        for i in tubeList:
            i.reset()


    if gameStart == True:
        bird.falling(is_jumping)
        gamescore += 1
        draw_score(str(score),text_font,(250,250,250),20,50)
    else:
        gamescore = 0
        score = 0


    isCollision(tubeList,bird)

   
    if gamescore % 340 == 0:
        score = int(score) + 1


    
    pygame.display.update()