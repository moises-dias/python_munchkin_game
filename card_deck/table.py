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

user32 = windll.user32
ShowWindow = user32.ShowWindow
def getSDLWindow():
    return pygame.display.get_wm_info()['window']
ShowWindow(getSDLWindow(), 3)

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

# fazer um método no field que retorna o rect e jogar esses rects abaixo dentro dele
rect_screen = pygame.rect.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)) 
rect_players = pygame.rect.Rect((0, 0, int(x_limits[0] * SCREEN_WIDTH), int(y_limits[0] * SCREEN_HEIGHT)))
rect_logs = pygame.rect.Rect((int(x_limits[1] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), (1 - x_limits[1]) * SCREEN_WIDTH, (1 - y_limits[1]) * SCREEN_HEIGHT))
rect_deck = pygame.rect.Rect((int(x_limits[0] * SCREEN_WIDTH), int(y_limits[1] * SCREEN_HEIGHT), int((x_limits[1] - x_limits[0]) * SCREEN_WIDTH), (1 - y_limits[1]) * SCREEN_HEIGHT))
rect_equipments = pygame.rect.Rect((0, int(y_limits[0] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), int((y_limits[1] - y_limits[0]) * SCREEN_HEIGHT)))
rect_table = pygame.rect.Rect((int(x_limits[0] * SCREEN_WIDTH), 0, (1 - x_limits[0]) * SCREEN_WIDTH, int(y_limits[1] * SCREEN_HEIGHT)))
rect_hand = pygame.rect.Rect((0, int(y_limits[1] * SCREEN_HEIGHT), int(x_limits[0] * SCREEN_WIDTH), (1 - y_limits[1]) * SCREEN_HEIGHT))

deck_x = int(x_limits[0] * SCREEN_WIDTH)
deck_y = int(y_limits[1] * SCREEN_HEIGHT)
deck_w = int((x_limits[1] - x_limits[0]) * SCREEN_WIDTH)
deck_h = (1 - y_limits[1]) * SCREEN_HEIGHT
cards_class = Cards(scale_x, scale_y, (deck_x + 0.01*deck_w, deck_y + 0.03*deck_h), (deck_x + 0.26*deck_w, deck_y + 0.03*deck_h), (deck_x + 0.51*deck_w, deck_y + 0.03*deck_h), (deck_x + 0.76*deck_w, deck_y + 0.03*deck_h))
cards = cards_class.get_cards()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:    
                cards_class.click(event.pos) 
            if event.button == 3:    
                cards_class.reveal(event.pos) 

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                cards_class.release(event.pos, rect_equipments, rect_table, rect_hand) 

        elif event.type == pygame.MOUSEMOTION:
            cards_class.move(event.pos, rect_screen, rect_players, rect_logs, rect_deck)
            # print(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                cards_class.discard(pygame.mouse.get_pos())

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_v:
                cards_class.cancel_expand()

        if pygame.key.get_pressed()[pygame.K_v]: #IMPEDIR CLICK, RELEASE,E DEMAIS FUNCOES ACIMA SE TIVER APERTANDO V
            cards_class.expand_card(pygame.mouse.get_pos(), SCREEN_WIDTH, SCREEN_HEIGHT)

    for rect in rects:
        rect.draw(screen)
    
    cards_class.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

    # if not (pygame.mouse.get_focused()): # trocar para mouse.x e y > 1000 ou < 0?
    #     for card in cards:
    #         card.release()


pygame.quit()