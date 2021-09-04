import pygame
from field import Field

SCREEN_WIDTH = 1266
SCREEN_HEIGHT = 668

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (122, 122, 122)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

x_limits = [0.4, 0.8]
y_limits = [0.25, 0.75]

rects = []
rects.append(Field(0, 0, int(x_limits[0] * SCREEN_WIDTH), int(y_limits[0] * SCREEN_HEIGHT), RED, 'players'))
rects.append(Field(0, int(y_limits[0] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), BLACK, 'equipments'))
rects.append(Field(0, int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), SCREEN_HEIGHT, GREY, 'hand'))
rects.append(Field(int(x_limits[0] * SCREEN_WIDTH), 0, SCREEN_WIDTH, int(y_limits[1] * SCREEN_HEIGHT), GREEN, 'table'))
rects.append(Field(int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[1] * SCREEN_WIDTH), SCREEN_HEIGHT, BLUE, 'deck'))
rects.append(Field(int(x_limits[1] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT, PURPLE, 'logs'))

FPS = 30

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Tracking System")

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen.fill(WHITE)

    for rect in rects:
        rect.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()