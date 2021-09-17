import pygame
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table
from card_deck.players import Players
import time
cards_class = None
players = None
players_class = None
running = False

def listen(network):
    global cards_class
    global players_class
    global running
    global players
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
    global cards_class
    global players
    global players_class
    global running
    # DEFAULT_WIDTH = 1580
    # DEFAULT_HEIGHT = 950
    # DEFAULT_SCALE_X = 137
    # DEFAULT_SCALE_Y = 222
    DEFAULT_WIDTH = 527
    DEFAULT_HEIGHT = 317
    DEFAULT_SCALE_X = 46
    DEFAULT_SCALE_Y = 74

    FPS = 30

    player_id = network.p['player']
    players = network.p['players']

    player_selected = -1
    player_hover = -1

    pygame.init()
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("colocar uns meme aqui")
    clock = pygame.time.Clock()

    # user32 = windll.user32
    # ShowWindow = user32.ShowWindow
    # wm_info = pygame.display.get_wm_info()['window']
    # ShowWindow(wm_info, 3)

    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

    scale_x = int(DEFAULT_SCALE_X * SCREEN_WIDTH / DEFAULT_WIDTH)
    scale_y = int(DEFAULT_SCALE_Y * SCREEN_HEIGHT / DEFAULT_HEIGHT)

    table_class = Table(SCREEN_WIDTH, SCREEN_HEIGHT, player_id)

    cards_info = network.get_all_cards()

    cards_class = Cards(SCREEN_WIDTH, SCREEN_HEIGHT, cards_info, scale_x, scale_y, table_class.get_rect('deck'))
    cards_class.set_draw_interact(player_selected, player_hover, player_id) # chamar la dentro do init

    players_class = Players(players, SCREEN_WIDTH, SCREEN_HEIGHT)
    
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
                cards_class.expand_card(pygame.mouse.get_pos(), SCREEN_WIDTH, SCREEN_HEIGHT)
            if action:
                network.send({'message_type': 'card_update', 'message': action}) #action no formato {'id': X, 'data': Y} sendo Y igual o dicionario no servidor

        table_class.update_equips_text(player_selected, player_hover)

        table_class.draw(screen)

        players_class.draw(screen)

        cards_class.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()