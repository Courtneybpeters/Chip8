import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((640, 320))

fps = pygame.time.Clock()

dark = pygame.Color(255, 0, 255)
light = pygame.Color(229, 204, 255)

x_axis = 0
y_axis = 0

size = 30

#True -- Dark
#False -- Light
display = [True, False, True, True, False, True]

while True:
    for pixel in display:
        if pixel == True:
            screen.fill(dark, (x_axis, y_axis, size, size))
            x_axis += 30

        else:
            screen.fill(light, (x_axis, y_axis, size, size))
            x_axis += 30


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    x_axis, y_axis = 0, 0

    fps.tick(60)
