

from os import path
import environmentInfo as enV

import pygame


pygame.init()

current_dir = path.dirname('main.py')
imagePath = path.join(current_dir, '..', 'images', 'player.png')
playerSurface = pygame.image.load(imagePath)
playerRect = playerSurface.get_frect(center=enV.windowCenter)

imagePath = path.join(current_dir, '..', 'images', 'star.png')
starSurface = pygame.image.load(imagePath)

imagePath = path.join(current_dir, '..', 'images', 'meteor.png')
meteorSurface = pygame.image.load(imagePath)
meteorRect = starSurface.get_frect(center=enV.windowCenter)


imagePath = path.join(current_dir, '..', 'images', 'meteor.png')
laserSurface = pygame.image.load(imagePath)
laserRect = starSurface.get_frect(center=enV.windowCenter)