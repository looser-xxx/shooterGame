#   importing pakages
from os import path

import pygame
import random

#   pygame initialization
pygame.init()

#   initializing window size and aspect ratio
windowWidth, windowHeight = 1920, 1080
displaySurface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption("Alian Wars")

#   initializing variable to be used
running = True
surf = pygame.Surface((0, 0))

#   importing an image
current_dir = path.dirname('main.py')
imagePath = path.join(current_dir, '..', 'images', 'player.png')
playerSurface = pygame.image.load(imagePath).convert_alpha()



imagePath = path.join(current_dir, '..', 'images', 'star.png')
starSurface = pygame.image.load(imagePath).convert_alpha()

randomPositionForStars=[]
numberOfStars=20

random.seed(5034345)
for i in range(numberOfStars):
    x=random.randint(0,windowWidth)
    y=random.randint(0,windowHeight)
    randomPositionForStars.append((x,y))



widthOfPlayer, heightOfPlayer = playerSurface.get_size()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('darkslategray')

    for x in range(numberOfStars):
            displaySurface.blit(starSurface, randomPositionForStars[x])





    playerPosition = pygame.mouse.get_pos()
    offsetPosition = (playerPosition[0] + widthOfPlayer / -2, playerPosition[1] + heightOfPlayer / -2)

    displaySurface.blit(playerSurface, offsetPosition)

    pygame.display.flip()

pygame.quit()
