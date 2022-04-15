import pygame
import time
import random
import math

# Initiate pygame. Always needed
pygame.init() 

# Clock
clock = pygame.time.Clock()

# RGB Color
BLACK = (0,0,0)
RED = (255,0,0)

# window with size of 500 x 400 pixels
wn_width = 800
wn_height = 800
wn = pygame.display.set_mode((wn_width,wn_height))
pygame.display.set_caption('Surrounded Shooter')

#Set up fonts
pygame.font.init()
font=pygame.font.SysFont("Comic Sans MS", 30)
killed_text=font.render("Killed: 0", False, (0,0,0))
missed_text=font.render("Missed: 0", False, (0,0,0))

# image
carimg = pygame.image.load('assets/ship.png')
carimg = pygame.transform.scale(carimg, (60, 60))
beamimg=pygame.image.load('assets/beam.png')
beamimg = pygame.transform.scale(beamimg, (30, 30))
alienimg=pygame.image.load("assets/alien.png")
alienimg=pygame.transform.scale(alienimg, (45, 35))

# boundary
west_b = 157
east_b = 359

beams=[]
aliens=[]
score=0
missed=0

def get_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

class Alien:
    def __init__(self):
        self.image=alienimg
        self.rect=self.image.get_rect()
        x=random.uniform(0, 800)
        y=random.choice([0, 800])
        #left or right side
        if random.randint(0, 1)==0:
            x=random.choice([0, 800])
            y=random.uniform(0, 800)
            
        self.position=[x,y]
        dx, dy = (400 - self.position[0], 400 - self.position[1])
        self.stepx, self.stepy = (dx / 130, dy / 130)

    def collision(self, player):
        global score, killed_text, missed, missed_text
        for beam in beams:
            
            if self.rect.colliderect(beam.rect):
                #collides
                score+=1
                killed_text=font.render("Killed: " + str(score), False, (0,0,0))

                aliens.remove(self)
                beams.remove(beam)


        if self.rect.colliderect(player.rect):
            missed+=1
            missed_text=font.render("Missed: " + str(missed), False, (0,0,0))
            aliens.remove(self)
            return
        
    def update(self, player):
        self.position=[self.position[0] + self.stepx, self.position[1] + self.stepy]
        self.rect.topleft=self.position[0], self.position[1]

        if self.position[0]<0 or self.position[0]>820 or self.position[1]<0 or self.position[1]>820:
            aliens.remove(self)

        self.collision(player)

class Beam:
    def __init__(self, x,y, angle):
        self.angle=-angle
        self.image=pygame.transform.rotate(beamimg, self.angle-90)
        
        self.rect=self.image.get_rect()
        #self.rect = self.image.get_rect(center=self.rect.center)
        self.width=self.image.get_width()
        self.height=self.image.get_height()

        self.dx=math.cos((-self.angle) * math.pi/180) * 7.5
        self.dy=math.sin((-self.angle) * math.pi/180) * 7.5
        
        self.position = [x, y]
                
                
    def update(self):
        self.position[0]+=self.dx
        self.position[1]+=self.dy

        if self.position[0]<0 or self.position[0]>820 or self.position[1]<0 or self.position[1]>820:
            beams.remove(self)

        self.rect.topleft = self.position[0], self.position[1]
     
def get_angle(player):
    direction = pygame.mouse.get_pos() - pygame.math.Vector2(player.rect.x + player.width/2, player.rect.y + player.height/2) 
    return direction.as_polar()

class Player:
    def __init__(self):
        
        self.image = carimg
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.x = int(wn_width * 0.5)
        self.rect.y = int(wn_height * 0.5)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(carimg, -angle -90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, angle):
        keystate = pygame.key.get_pressed()
        dx=0
        dy=0
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            dx = -1
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            dx = 1
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            dy=-1
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            dy=1

        newXDistance=self.rect.x+dx*2
        newYDistance=self.rect.y+dy*2
        if get_distance(newXDistance + self.width/2, newYDistance + self.height/2, 400, 400)<80:
            self.rect.x=newXDistance
            self.rect.y=newYDistance
        self.rotate(angle)

start=time.time()

# def game function 
def game_loop():
    global start
    player = Player()
    while True:
        radius, angle=get_angle(player)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                b=Beam(player.rect.x+player.width/2,  player.rect.y + player.height/2, angle)
                beams.append(b)
        
        
        wn.fill((199, 242, 248))

        #Draw center circle
        pygame.draw.circle(wn, (0,255,0), (400, 400), 80)
        pygame.draw.circle(wn, (199, 242, 248), (400, 400), 75)

        if time.time()-start>=2:
            aliens.append(Alien())
            aliens.append(Alien())
            start=time.time()
            
        player.update(angle)
        wn.blit(player.image,(player.rect.x,player.rect.y))

        for alien in aliens:
            alien.update(player)
            wn.blit(alien.image,(alien.rect.x,alien.rect.y))
        
        for b in beams:
            b.update()
            wn.blit(b.image,(b.rect.x,b.rect.y))

        wn.blit(killed_text, (0,0))
        wn.blit(missed_text, (600, 0))
        pygame.display.update()
        clock.tick(60) 

### pygame quit
game_loop()
pygame.quit()
quit()
