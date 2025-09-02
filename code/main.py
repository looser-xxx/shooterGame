#   importing pakages
from os import path
from turtledemo import clock

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

playerPosition = pygame.Vector2(windowWidth / 2, windowHeight / 2)
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('darkslategray')

    for x in range(numberOfStars):
            displaySurface.blit(starSurface, randomPositionForStars[x])










    offsetPosition = (playerPosition[0] + widthOfPlayer / -2, playerPosition[1] + heightOfPlayer / -2)
    displaySurface.blit(playerSurface, offsetPosition)

    keys = pygame.key.get_pressed()

    # playerPosition = pygame.mouse.get_pos()




    if keys[pygame.K_w]:
        playerPosition.y -= 1
    if keys[pygame.K_s]:
        playerPosition.y += 1
    if keys[pygame.K_a]:
        playerPosition.x -= 1
    if keys[pygame.K_d]:
        playerPosition.x += 1



    #








    pygame.display.flip()

pygame.quit()
