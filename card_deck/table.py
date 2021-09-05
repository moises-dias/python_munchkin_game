import pygame
from field import Field
from card import Card
from ctypes import windll
from cards import Cards
# from pygame.locals  import *

DEFAULT_WIDTH = 1580
DEFAULT_HEIGHT = 950
DEFAULT_SCALE_X = 137
DEFAULT_SCALE_Y = 222
DEFAULT_STARTING_POINT = 800

FPS = 30

pygame.init()
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("colocar uns meme aqui")
clock = pygame.time.Clock()

# user32 = windll.user32
# ShowWindow = user32.ShowWindow
# def getSDLWindow():
#     return pygame.display.get_wm_info()['window']
# ShowWindow(getSDLWindow(), 3)

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

scale_x = int(DEFAULT_SCALE_X * SCREEN_WIDTH / DEFAULT_WIDTH)
scale_y = int(DEFAULT_SCALE_Y * SCREEN_HEIGHT / DEFAULT_HEIGHT)

starting_point = DEFAULT_STARTING_POINT * SCREEN_WIDTH / DEFAULT_WIDTH

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
rects.append(Field(0, int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), (1 - y_limits[1]) * SCREEN_HEIGHT, GREY, 'hand'))
rects.append(Field(0, int(y_limits[0] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), int((y_limits[1] - y_limits[0]) * SCREEN_HEIGHT), BLACK, 'equipments'))
rects.append(Field(int(x_limits[0] * SCREEN_WIDTH), 0, (1 - x_limits[0]) * SCREEN_WIDTH, int(y_limits[1] * SCREEN_HEIGHT), GREEN, 'table'))
rects.append(Field(int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), int((x_limits[1] - x_limits[0]) * SCREEN_WIDTH), (1 - y_limits[1]) * SCREEN_HEIGHT, BLUE, 'deck'))
rects.append(Field(int(x_limits[1] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), (1 - x_limits[1]) * SCREEN_WIDTH, (1 - y_limits[1]) * SCREEN_HEIGHT, PURPLE, 'logs'))

im_w = 500
im_h = 809
my_image = pygame.image.load("card_deck/images/treasure2.jpeg")

rect_screen = pygame.rect.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)) 
rect_players = pygame.rect.Rect((0, 0, int(x_limits[0] * SCREEN_WIDTH), int(y_limits[0] * SCREEN_HEIGHT)))
rect_logs = pygame.rect.Rect((int(x_limits[1] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT))
rect_deck = pygame.rect.Rect((int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[1] * SCREEN_WIDTH), SCREEN_HEIGHT))

rect_equipments = pygame.rect.Rect((0, int(y_limits[0] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), int((y_limits[1] - y_limits[0]) * SCREEN_HEIGHT)))
rect_table = pygame.rect.Rect((int(x_limits[0] * SCREEN_WIDTH), 0, (1 - x_limits[0]) * SCREEN_WIDTH, int(y_limits[1] * SCREEN_HEIGHT)))
rect_hand = pygame.rect.Rect((0, int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), (1 - y_limits[1]) * SCREEN_HEIGHT))

#print(rect_players.x, rect_players.y)

cards = []

cards.append(Card(pygame.transform.smoothscale(my_image.subsurface((0, 0, im_w, im_h)), (scale_x, scale_y)), starting_point, 10, scale_x, scale_y, 0))
cards.append(Card(pygame.transform.smoothscale(my_image.subsurface((0, im_h, im_w, im_h)), (scale_x, scale_y)), starting_point + 10, 10, scale_x, scale_y, 1))
cards.append(Card(pygame.transform.smoothscale(my_image.subsurface((im_w, 0, im_w, im_h)), (scale_x, scale_y)), starting_point + 20, 10, scale_x, scale_y, 2))
cards.append(Card(pygame.transform.smoothscale(my_image.subsurface((im_w, im_h, im_w, im_h)), (scale_x, scale_y)), starting_point + 30, 10, scale_x, scale_y, 3))

running = True
max_card_order = 0

cards_class = Cards()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:     
                for card in reversed(cards):     
                    if card.click(event.pos):
                        max_card_order = max_card_order + 1
                        card.set_order(max_card_order)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                for card in cards:
                    card.release(event.pos, rect_equipments, rect_table, rect_hand)

        elif event.type == pygame.MOUSEMOTION:
            for card in cards:
                card.move(event.pos, rect_screen, rect_players, rect_logs, rect_deck)

    screen.fill(WHITE)

    cards.sort(key=lambda c: c.get_order())

    for rect in rects:
        rect.draw(screen)
    for card in cards:
        card.draw(screen)
    
    # cards_class.draw(screen)

    # rect_equipments
    # rect_table
    # rect_hand

    # pygame.draw.rect(screen, (0,   255,   170), rect_equipments)

    pygame.display.flip()

    clock.tick(FPS)

    # if not (pygame.mouse.get_focused()): # trocar para mouse.x e y > 1000 ou < 0?
    #     for card in cards:
    #         card.release()


pygame.quit()