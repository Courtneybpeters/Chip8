import pygame, sys
from pygame.locals import *

pygame.init()

size = 10

fps = pygame.time.Clock()

dark = pygame.Color(93, 1, 130)
light = pygame.Color(229, 204, 255)

#True -- Dark
#False -- Light
display = [[True for x in range(64)] for x in range(32)]

display[0][0] = False
display[0][63] = False
display[31][0] = False
display[31][63] = False

while True:

    screen = pygame.display.set_mode((64 * size, 32 * size), pygame.RESIZABLE)

    for y, row in enumerate(display):
        for x, pixel in enumerate(row):

            if pixel == True:
                screen.fill(dark, (x * size, y * size, size, size))

            else:
                screen.fill(light, (x * size, y * size, size, size))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_EQUALS:
                size += 2
            if event.key == K_MINUS:
                size -= 2

    pygame.display.update()

    x_axis, y_axis = 0, 0

    fps.tick(60)
