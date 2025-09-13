

from os import path


import environmentInfo as enV

import pygame


pygame.init()



screen = pygame.display.set_mode(enV.screenSize)







class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player/player.png").convert_alpha()
        self.rect = self.image.get_frect(center=enV.windowCenter)




current_dir = path.dirname('main.py')
imagePath = path.join(current_dir, '..', 'images', 'player.png')
playerSurface = pygame.image.load(imagePath).convert_alpha()
playerX,playerY=playerSurface.get_size()
playerRect = playerSurface.get_frect(center=enV.windowCenter)

imagePath = path.join(current_dir, '..', 'images', 'star.png')
starSurface = pygame.image.load(imagePath)

imagePath = path.join(current_dir, '..', 'images', 'meteor.png')
meteorSurface = pygame.image.load(imagePath).convert_alpha()
meteorRect = meteorSurface.get_frect(center=enV.windowCenter)


imagePath = path.join(current_dir, '..', 'images', 'laser.png')
laserSurface = pygame.image.load(imagePath).convert_alpha()
laserRect = laserSurface.get_frect(center=enV.windowCenter)




imagePath = path.join(current_dir, '..', 'images/explosion', '3.png')
explodeSurface = pygame.image.load(imagePath).convert_alpha()
explodeRect = explodeSurface.get_frect(center=enV.windowCenter)


