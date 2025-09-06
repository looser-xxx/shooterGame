#   importing pakages
import random
from os import path

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
toFireShot = False
destroyMeteor = False

#   importing an image



randomPositionForStars = []
numberOfStars = 20

random.seed(5034345)
for i in range(numberOfStars):
    x = random.randint(0, enV.windowWidth)
    y = random.randint(0, enV.windowHeight)
    randomPositionForStars.append((x, y))



meteorExplode=False

gA.meteorRect.top-=200
loopTime = 0
initialLoopTime = 0
while running:

    loopTime+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    displaySurface.fill('darkslategray')

    for x in range(numberOfStars):
        displaySurface.blit(gA.starSurface, randomPositionForStars[x])




    if pygame.mouse.get_just_pressed()[0]:
        toFireShot = True
        destroyMeteor = True
        initialLoopTime = loopTime
        gA.laserRect.bottom = gA.playerRect.top
        gA.laserRect.left = gA.playerRect.centerx-5





    if gA.laserRect.bottom < 0:
        gA.laserRect.bottom = 0
    else:
        gA.laserRect.top-=5


    if toFireShot :
        displaySurface.blit(gA.laserSurface, gA.laserRect)


    displaySurface.blit(gA.meteorSurface, gA.meteorRect)

    if gA.meteorRect.bottom > gA.laserRect.bottom > gA.meteorRect.top and gA.meteorRect.right > gA.laserRect.left > gA.meteorRect.left and toFireShot:
        gA.laserRect.bottom = 0
        meteorExplode = True
        print('true')
        explodeSizeX, explodeSizeY = gA.explodeSurface.get_size()
        displaySurface.blit(gA.explodeSurface,(gA.meteorRect.left + explodeSizeX / 2, gA.meteorRect.top + explodeSizeY / 2 - 7))


    if meteorExplode:
        meteorExplode = False




    displaySurface.blit(gA.playerSurface, gA.playerRect)





    keys = pygame.key.get_pressed()
    playerRect = keyboardMovements.keyPresses(gA.playerRect,keys)
    playerRect =keyboardMovements.boundingRect(playerRect)


    pygame.display.flip()

pygame.quit()
