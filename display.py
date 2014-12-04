import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((703, 351))

fps = pygame.time.Clock()

dark = pygame.Color(93, 1, 130)
light = pygame.Color(229, 204, 255)

x_axis = 0
y_axis = 0

size = 10

#True -- Dark
#False -- Light
display = [[[True for x in range(64)], [False for x in range(64)]] for x in range(32)]

while True:
    for row in display:
        for col in row:
            for pixel in col:
                if x_axis >= 703:
                    x_axis = 0
                    y_axis += size + 1

                if pixel == True:
                    screen.fill(dark, (x_axis, y_axis, size, size))
                    x_axis += size + 1

                else:
                    screen.fill(light, (x_axis, y_axis, size, size))
                    x_axis += size + 1


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    x_axis, y_axis = 0, 0

    fps.tick(60)
