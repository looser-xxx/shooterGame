#   importing pakages
import random

import pygame

import environmentInfo as enV
import gameAssets as gA
import keyboardMovements

#   pygame initialization
pygame.init()



displaySurface = pygame.display.set_mode((enV.windowWidth, enV.windowHeight))


#   initializing variable to be used
running = True
surf = pygame.Surface((0, 0))

#   importing an image


randomPositionForStars = []
numberOfStars = 20

random.seed(5034345)
for i in range(numberOfStars):
    x = random.randint(0, enV.windowWidth)
    y = random.randint(0, enV.windowHeight)
    randomPositionForStars.append((x, y))

widthOfPlayer, heightOfPlayer = gA.playerSurface.get_size()


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('darkslategray')
    displaySurface.blit(gA.meteorSurface, gA.meteorRect)

    for x in range(numberOfStars):
        displaySurface.blit(gA.starSurface, randomPositionForStars[x])




    displaySurface.blit(gA.playerSurface, gA.playerRect)
    keys = pygame.key.get_pressed()
    playerRect = keyboardMovements.keyPresses(gA.playerRect,keys)
    playerRect = keyboardMovements.boundingRect(playerRect)


    pygame.display.flip()

pygame.quit()
