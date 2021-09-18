import pygame
import time
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table
from card_deck.players import Players

cards_class = None
players = None
players_class = None

running = False

X_LIMITS_DEFAULT = [0.4, 0.8]
Y_LIMITS_DEFAULT = [0.25, 0.75]
W_PLAYERS_DEFAULT = X_LIMITS_DEFAULT[0] / 2
H_PLAYERS_DEFAULT = Y_LIMITS_DEFAULT[0] / 5

def listen(network):
    # ver se precisa desses globals aqui
    global cards_class
    global players_class
    global players
    global running
    while not running:
        time.sleep(0.01)
    while running:
        message = network.receive()
        if message:
            if message['message_type'] == 'card_update':
                cards_class.update(message['message'])
            elif message['message_type'] == 'player_disconnected':
                cards_class.discard_player(message['message'])
                players.remove(message['message'])
                players_class.delete_player(players, message['message'])
            elif message['message_type'] == 'players_update':
                players.append(message['message'])
                players_class.update_players(players)

def play(network):
    # ver se precisa desses globals aqui
    global cards_class
    global players
    global players_class
    global running
    # global x_limits
    # global y_limits
    # global w_players
    # global h_players
    
    # DEFAULT_WIDTH = 1580
    # DEFAULT_HEIGHT = 950
    # DEFAULT_SCALE_X = 137
    # DEFAULT_SCALE_Y = 222
    DEFAULT_WIDTH = 527
    DEFAULT_HEIGHT = 317
    DEFAULT_SCALE_X = 46
    DEFAULT_SCALE_Y = 74

    FPS = 30

    player_id = network.get_player_id()
    players = network.get_player_list()

    player_selected = -1
    player_hover = -1

    pygame.init()
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("munchkin")
    clock = pygame.time.Clock()

    # user32 = windll.user32
    # ShowWindow = user32.ShowWindow
    # wm_info = pygame.display.get_wm_info()['window']
    # ShowWindow(wm_info, 3)

    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

    scale_x = int(DEFAULT_SCALE_X * SCREEN_WIDTH / DEFAULT_WIDTH)
    scale_y = int(DEFAULT_SCALE_Y * SCREEN_HEIGHT / DEFAULT_HEIGHT)

    x_limits = [x * SCREEN_WIDTH for x in X_LIMITS_DEFAULT]
    y_limits = [y * SCREEN_HEIGHT for y in Y_LIMITS_DEFAULT]
    w_players = W_PLAYERS_DEFAULT * SCREEN_WIDTH
    h_players = H_PLAYERS_DEFAULT * SCREEN_HEIGHT

    table_class = Table(SCREEN_WIDTH, SCREEN_HEIGHT, player_id, x_limits, y_limits)

    cards_info = network.get_all_cards()

    cards_class = Cards(SCREEN_WIDTH, SCREEN_HEIGHT, cards_info, scale_x, scale_y, table_class.get_rect('deck'))
    cards_class.set_draw_interact(player_selected, player_hover, player_id) # chamar la dentro do init

    players_class = Players(players, w_players, h_players)
    
    running = True

    while running:
        action = None
        cards_class.set_draw_interact(player_selected, player_hover, player_id)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                network.send({'message_type': 'quit'})
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   
                    if table_class.fields['players'].rect.collidepoint(event.pos):
                        player_selected = players_class.focused(pygame.mouse.get_pos(), 'select')
                    action = cards_class.click(event.pos, player_id)

                if event.button == 3 and not pygame.mouse.get_pressed()[0]:    
                    action = cards_class.reveal(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    action = cards_class.release(event.pos, table_class.get_rect('equipments'), table_class.get_rect('table'), table_class.get_rect('hand'))

            elif event.type == pygame.MOUSEMOTION:
                if table_class.fields['players'].rect.collidepoint(event.pos):
                    player_hover = players_class.focused(pygame.mouse.get_pos(), 'hover')
                    cards_class.set_draw_interact(player_selected, player_hover, player_id)
                elif not table_class.fields['equipments'].rect.collidepoint(event.pos):
                    if player_hover != -1 or player_selected != -1:
                        player_hover = -1
                        player_selected = -1
                        players_class.clear()
                        cards_class.set_draw_interact(player_selected, player_hover, player_id)
                action = cards_class.move(event.pos, table_class.get_rect('screen'), table_class.get_rects())
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and not pygame.mouse.get_pressed()[0]:
                    action = cards_class.discard(pygame.mouse.get_pos())

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_v:
                    cards_class.cancel_expand()
            if pygame.key.get_pressed()[pygame.K_v]:
                cards_class.expand_card(pygame.mouse.get_pos())
            if action:
                network.send({'message_type': 'card_update', 'message': action}) #action no formato {'id': X, 'data': Y} sendo Y igual o dicionario no servidor

        table_class.update_equips_text(player_selected, player_hover)

        table_class.draw(screen)

        players_class.draw(screen)

        cards_class.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()