import pygame
import time
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table
from card_deck.players import Players
import threading

cards_class = None
players = None
players_class = None

cards_class_lock = threading.Lock()
# players_lock = threading.Lock()
players_class_lock = threading.Lock()

running = False

X_LIMITS_DEFAULT = [0.4, 0.8]
Y_LIMITS_DEFAULT = [0.25, 0.75]
W_PLAYERS_DEFAULT = X_LIMITS_DEFAULT[0] / 2
H_PLAYERS_DEFAULT = Y_LIMITS_DEFAULT[0] / 5

def caller(obj, method, args, lock):
    with lock:
        return getattr(obj, method)(*args)

# network precisa de lock? na listen eu só uso receive e na play uso send
def listen(network):
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
                # cards_class.update(message['message'])
                caller(cards_class, 'update', [message['message']], cards_class_lock)
            elif message['message_type'] == 'player_disconnected':
                # cards_class.discard_player(message['message'])
                caller(cards_class, 'discard_player', [message['message']], cards_class_lock)
                players.remove(message['message'])
                # players_class.delete_player(players, message['message'])
                caller(players_class, 'delete_player', [players, message['message']], players_class_lock)
            elif message['message_type'] == 'players_update':
                players.append(message['message'])
                # players_class.update_players(players)
                caller(players_class, 'update_players', [players], players_class_lock)
            elif message['message_type'] == 'reset_game':
                print('calling reset on listen function')
                caller(cards_class, 'reset', [], cards_class_lock)
            elif message['message_type'] == 'self_disconnected':
                break
    print('listen ended')

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
    DEFAULT_FIELD_FONT_SIZE = 11
    DEFAULT_CARD_FONT_SIZE = 11

    FPS = 30

    typed_word = ''
    reset_word = 'reset12345'

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
    FIELD_FONT_SIZE = int(DEFAULT_FIELD_FONT_SIZE * SCREEN_WIDTH / DEFAULT_WIDTH)
    CARD_FONT_SIZE = int(DEFAULT_CARD_FONT_SIZE * SCREEN_HEIGHT / DEFAULT_HEIGHT)

    x_limits = [x * SCREEN_WIDTH for x in X_LIMITS_DEFAULT]
    y_limits = [y * SCREEN_HEIGHT for y in Y_LIMITS_DEFAULT]
    w_players = W_PLAYERS_DEFAULT * SCREEN_WIDTH
    h_players = H_PLAYERS_DEFAULT * SCREEN_HEIGHT

    table_class = Table(SCREEN_WIDTH, SCREEN_HEIGHT, player_id, x_limits, y_limits, FIELD_FONT_SIZE)

    cards_info = network.get_all_cards()

    cards_class = Cards(SCREEN_WIDTH, SCREEN_HEIGHT, cards_info, scale_x, scale_y, table_class.get_rect('deck'), CARD_FONT_SIZE)
    cards_class.set_draw_interact(player_selected, player_hover, player_id) # chamar la dentro do init?

    players_class = Players(players, w_players, h_players, FIELD_FONT_SIZE)
    
    running = True

    while running:
        action = None
        # cards_class.set_draw_interact(player_selected, player_hover, player_id)
        caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                network.send({'message_type': 'quit'})
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   
                    # if table_class.fields['players'].rect.collidepoint(event.pos):
                    if table_class.get_collidepoint('players', event.pos):
                        # player_selected = players_class.focused(pygame.mouse.get_pos(), 'select')
                        player_selected = caller(players_class, 'focused', [pygame.mouse.get_pos(), 'select'], players_class_lock)
                    # action = cards_class.click(event.pos, player_id)
                    action = caller(cards_class, 'click', [event.pos, player_id], cards_class_lock)

                if event.button == 3 and not pygame.mouse.get_pressed()[0]:    
                    # action = cards_class.reveal(event.pos)
                    action = caller(cards_class, 'reveal', [event.pos], cards_class_lock)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    # action = cards_class.release(event.pos, table_class.get_rect('equipments'), table_class.get_rect('table'), table_class.get_rect('hand'))
                    action = caller(cards_class, 'release', [event.pos, table_class.get_rect('equipments'), table_class.get_rect('table'), table_class.get_rect('hand')], cards_class_lock)

            elif event.type == pygame.MOUSEMOTION:
                if table_class.fields['players'].rect.collidepoint(event.pos):
                    # player_hover = players_class.focused(pygame.mouse.get_pos(), 'hover')
                    player_hover = caller(players_class, 'focused', [pygame.mouse.get_pos(), 'hover'], players_class_lock)
                    # cards_class.set_draw_interact(player_selected, player_hover, player_id)
                    caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
                elif not table_class.fields['equipments'].rect.collidepoint(event.pos):
                    if player_hover != -1 or player_selected != -1:
                        player_hover = -1
                        player_selected = -1
                        # players_class.clear()
                        caller(players_class, 'clear', [], players_class_lock)
                        # cards_class.set_draw_interact(player_selected, player_hover, player_id)
                        caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
                # action = cards_class.move(event.pos, table_class.get_rect('screen'), table_class.get_rects())
                action = caller(cards_class, 'move', [event.pos, table_class.get_rect('screen'), table_class.get_rects(), player_id], cards_class_lock)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and not pygame.mouse.get_pressed()[0]:
                    # action = cards_class.discard(pygame.mouse.get_pos())
                    action = caller(cards_class, 'discard', [pygame.mouse.get_pos()], cards_class_lock)
                # print(event.unicode, event.unicode.isalnum())
                if event.unicode.isalnum():
                    typed_word = (typed_word + event.unicode)[-10:]
                    if typed_word == reset_word:
                        print("RESETAR")
                        network.send({'message_type': 'reset_game', 'message': player_id})
                        caller(cards_class, 'reset', [], cards_class_lock)
                # print(typed_word)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_v:
                    # cards_class.cancel_expand()
                    caller(cards_class, 'cancel_expand', [], cards_class_lock)
            if pygame.key.get_pressed()[pygame.K_v]:
                # cards_class.expand_card(pygame.mouse.get_pos())
                caller(cards_class, 'expand_card', [pygame.mouse.get_pos()], cards_class_lock)
            if action:
                network.send({'message_type': 'card_update', 'message': action}) #action no formato {'id': X, 'data': Y} sendo Y igual o dicionario no servidor

        table_class.update_equips_text(player_selected, player_hover)

        table_class.draw(screen)

        # players_class.draw(screen, cards_class.get_quantities())
        caller(players_class, 'draw', [screen, caller(cards_class, 'get_quantities', [], cards_class_lock)], players_class_lock)

        # cards_class.draw(screen)
        caller(cards_class, 'draw', [screen], cards_class_lock)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

    print('play ended')