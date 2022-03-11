from cgi import print_arguments
import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 25
fpsClock = pygame.time.Clock()

print(fpsClock)

DISPLASURF = pygame.display.set_mode((400,300), 0, 32)
pygame.display.set_caption('Cat Animation')

WHITE = (255,255,255)
catImg = pygame.image.load('cat.png')
cat_x = 10
cat_y = 10
direction = 'right'

while True:
    DISPLASURF.fill(WHITE)

    if direction == 'right':
        cat_x += 5
        if cat_x == 280:
            direction = 'down'

    elif direction == 'down':
        cat_y += 5
        if cat_y == 220:
            direction = 'left'

    elif direction == 'left':
        cat_x -= 5
        if cat_x == 10:
            direction = 'up'

    elif direction == 'up':
        cat_y -= 5
        if cat_y == 10:
            direction = 'right'

    DISPLASURF.blit(catImg, (cat_x, cat_y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
