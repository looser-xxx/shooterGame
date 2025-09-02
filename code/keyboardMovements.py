

import pygame
import environmentInfo as enV






def keyPressesReverse(rect,keys):
    if keys[pygame.K_w]:
        rect.top += 1

    if keys[pygame.K_s]:
        rect.top -= 1

    if keys[pygame.K_a]:
        rect.left += 1

    if keys[pygame.K_d]:
        rect.left -= 1

    return rect




def keyPresses(rect,keys):
    if keys[pygame.K_w]:
        rect.top -= 1

    if keys[pygame.K_s]:
        rect.top += 1

    if keys[pygame.K_a]:
        rect.left -= 1

    if keys[pygame.K_d]:
        rect.left += 1

    return rect


def boundingRect(rect):
    if rect.left < 0:
        rect.left = 0

    if rect.top < 0:
        rect.top = 0

    if rect.bottom > enV.windowHeight:
        rect.bottom = enV.windowHeight

    if rect.right > enV.windowWidth:
        rect.right = enV.windowWidth

    return rect



pygame.init()








pygame.quit()