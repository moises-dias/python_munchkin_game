import pygame
from field import Field
from card import Card

SCREEN_WIDTH = 1666
SCREEN_HEIGHT = 950

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

im_w = 500
im_h = 809

my_image = pygame.image.load("workspace/teste2.jpeg")

rect_screen = pygame.rect.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)) 
rect_players = pygame.rect.Rect((0, 0, int(x_limits[0] * SCREEN_WIDTH), int(y_limits[0] * SCREEN_HEIGHT)))
rect_logs = pygame.rect.Rect((int(x_limits[1] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT))
rect_deck = pygame.rect.Rect((int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[1] * SCREEN_WIDTH), SCREEN_HEIGHT))

cards = []

cards.append(Card(pygame.transform.scale(my_image.subsurface((0, 0, im_w, im_h)), (125, 202)), 500, 10, 125, 202))
cards.append(Card(pygame.transform.scale(my_image.subsurface((0, im_h, im_w, im_h)), (125, 202)), 550, 10, 125, 202))
cards.append(Card(pygame.transform.scale(my_image.subsurface((im_w, 0, im_w, im_h)), (125, 202)), 600, 10, 125, 202))
cards.append(Card(pygame.transform.scale(my_image.subsurface((im_w, im_h, im_w, im_h)), (125, 202)), 650, 10, 125, 202))



FPS = 30

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tracking System")
clock = pygame.time.Clock()



running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:     
                for card in cards:     
                    card.click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                for card in cards:
                    card.release()       

        elif event.type == pygame.MOUSEMOTION:
            for card in cards:
                card.move(event.pos, rect_screen, rect_players, rect_logs, rect_deck)

    #screen.fill(WHITE)

    for rect in rects:
        rect.draw(screen)
    for card in cards:
        card.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

    if not (pygame.mouse.get_focused()): # trocar para mouse.x e y > 1000 ou < 0?
        for card in cards:
            card.release()


pygame.quit()