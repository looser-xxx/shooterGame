from os import path

import pygame
import gameSettings as gS
import random


def loadingAssets(fileName):
    return pygame.image.load(path.join(path.dirname('main.py'), '..', 'images', fileName)).convert_alpha()


class Shooter:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.screenColor=gS.screenColor
        self.displaySurface=pygame.display.set_mode(gS.screenSize)
        self.stars=Stars(loadingAssets('star.png'))
        self.player=Player(loadingAssets('player.png'))
        self.lasers=pygame.sprite.Group()
        self.allSprites=pygame.sprite.Group()
        self.allSprites.add(self.stars)
        self.allSprites.add(self.player)




    def draw(self):
        self.displaySurface.fill(self.screenColor)
        self.stars.draw(self.displaySurface)
        self.allSprites.draw(self.displaySurface)


    def handleEvents(self,dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("button pressed")
                    laser = Laser(loadingAssets('laser.png'), self.player.rect.centerx, self.player.rect.top)
                    self.lasers.add(laser)
                    self.allSprites.add(laser)




        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move('w',dt)
        if keys[pygame.K_s]:
            self.player.move('s',dt)
        if keys[pygame.K_a]:
            self.player.move('a',dt)
        if keys[pygame.K_d]:
            self.player.move('d',dt)








    def boundary(self):
        if self.player.rect.top<0:
            self.player.rect.top=0
        if self.player.rect.bottom>gS.screenHeight:
            self.player.rect.bottom=gS.screenHeight
        if self.player.rect.left<0:
            self.player.rect.left=0
        if self.player.rect.right>gS.screenWidth:
            self.player.rect.right=gS.screenWidth

    def run(self):
        while self.running:
            dt = self.clock.tick(gS.fps) / 1000
            self.handleEvents(dt)
            self.allSprites.update(dt)

            self.draw()
            self.boundary()



            pygame.display.flip()



class Stars(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()
        self.randStarPose=[]

    def starPose(self):
        random.seed(gS.randomSeed)
        for i in range(gS.numberOfStars):
            x = random.randint(0, gS.screenWidth)
            y = random.randint(0, gS.screenHeight)
            self.randStarPose.append((x, y))

    def draw(self,displaySurface):
        if not self.randStarPose:
            self.starPose()
        else:
            for pos in self.randStarPose:
                displaySurface.blit(self.image, pos)


class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image=image
        self.rect=self.image.get_frect(center=gS.screenCenter)
        self.speed=gS.playerSpeed



    def move(self,keyPressed,dt):
        if keyPressed=='w':
            self.rect.top-=self.speed * dt
        elif keyPressed=='a':
            self.rect.left-=self.speed * dt
        elif keyPressed=='s':
            self.rect.bottom+=self.speed * dt
        elif keyPressed=='d':
            self.rect.right+=self.speed * dt

    def draw(self,displaySurface):
        displaySurface.blit(self.image,self.rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image=image
        self.rect=self.image.get_frect()
        self.rect.centerx=x
        self.rect.bottom=y

    def draw(self,displaySurface):
        print("draw call")
        displaySurface.blit(self.image,self.rect)

    def update(self,dt):
        self.rect.bottom -= gS.laserSpeed * dt

        if self.rect.bottom < 0:
            self.kill()


if __name__ == "__main__":
    screen = pygame.display.set_mode(gS.screenSize)
    game = Shooter()
    game.run()