import pygame
import time
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table
from card_deck.players import Players
from card_deck.scores import Scores
import threading

cards_class = None
players = None
players_class = None
table_class = None
scores_class = None

cards_class_lock = threading.Lock()
# players_lock = threading.Lock()
players_class_lock = threading.Lock()
table_class_lock = threading.Lock()
scores_class_lock = threading.Lock()

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
    try:
        global cards_class
        global players_class
        global table_class
        global scores_class
        global players
        global running
        while not running:
            time.sleep(0.01)
        while running:
            message = network.receive()
            if message:
                if message['message_type'] == 'card_update':
                    caller(cards_class, 'update', [message['message']], cards_class_lock)

                elif message['message_type'] == 'player_disconnected':
                    caller(cards_class, 'discard_player', [message['message']], cards_class_lock)
                    players.remove(message['message'])
                    caller(players_class, 'delete_player', [players, message['message']], players_class_lock)

                elif message['message_type'] == 'players_update':
                    players.append(message['message']['player'])
                    caller(players_class, 'update_players', [players, message['message']['levels']], players_class_lock)
                    caller(cards_class, 'set_player_cards', [message['message']['player']], cards_class_lock)

                elif message['message_type'] == 'reset_game':
                    caller(cards_class, 'reset', [], cards_class_lock)

                elif message['message_type'] == 'reset_discarded':
                    caller(cards_class, 'reset_discarded', [], cards_class_lock)

                elif message['message_type'] == 'dice_roll':
                    caller(table_class, 'dice_roll', [message['message']], table_class_lock)

                elif message['message_type'] == 'level_update':
                    caller(players_class, 'set_level', [message['message']['player'], message['message']['level']], players_class_lock)

                elif message['message_type'] == 'score_update':
                    caller(scores_class, 'set_number', [message['message']['type'], message['message']['value']], scores_class_lock)

                elif message['message_type'] == 'heartbeat':
                    # print('client received heartbeat')
                    network.send({'message_type': 'heartbeat'})
                    # print('client sent heartbeat')

                elif message['message_type'] == 'self_disconnected':
                    break

        print('listen ended')
    except Exception as e:
        print('listen error ', e)
        network.send({'message_type': 'quit'})
        raise e

def play(network):
    try:
        global cards_class
        global players
        global players_class
        global table_class
        global scores_class
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

        FPS = 20

        typed_word = ''
        reset_word = 'reset12345'
        reset_discarded_word = 'reset54321'

        player_id = network.get_player_id()
        players = network.get_player_list()
        player_levels = network.get_player_levels()

        player_selected = -1
        player_hover = -1

        pygame.init()
        screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("munchkin")
        clock = pygame.time.Clock()

        user32 = windll.user32
        ShowWindow = user32.ShowWindow
        wm_info = pygame.display.get_wm_info()['window']
        ShowWindow(wm_info, 3)

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

        players_class = Players(players, player_levels, w_players, h_players, FIELD_FONT_SIZE)

        scores_class = Scores(x_limits[0], SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_FONT_SIZE)
        
        running = True

        while running:
            action = None
            caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    network.send({'message_type': 'quit'})
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:   
                        if caller(table_class, 'get_collidepoint', ['players', event.pos], table_class_lock):
                            player_selected = caller(players_class, 'focused', [pygame.mouse.get_pos(), 'select'], players_class_lock)
                        if caller(table_class, 'get_collidepoint', ['logs', event.pos], table_class_lock):
                            dice_result = caller(table_class, 'dice_roll', [None], table_class_lock)
                            network.send({'message_type': 'dice_roll', 'message': dice_result})
                        action = caller(cards_class, 'click', [event.pos, player_id], cards_class_lock)

                    if event.button == 3 and not pygame.mouse.get_pressed()[0]:    
                        action = caller(cards_class, 'reveal', [event.pos], cards_class_lock)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  
                        action = caller(cards_class, 'release', [event.pos, caller(table_class, 'get_rect', ['equipments'], table_class_lock), caller(table_class, 'get_rect', ['table'], table_class_lock), caller(table_class, 'get_rect', ['hand'], table_class_lock)], cards_class_lock)

                elif event.type == pygame.MOUSEMOTION:
                    if caller(table_class, 'get_collidepoint', ['players', event.pos], table_class_lock):
                        player_hover = caller(players_class, 'focused', [pygame.mouse.get_pos(), 'hover'], players_class_lock)
                        caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
                    elif not caller(table_class, 'get_collidepoint', ['equipments', event.pos], table_class_lock):
                        if player_hover != -1 or player_selected != -1:
                            player_hover = -1
                            player_selected = -1
                            caller(players_class, 'clear', [], players_class_lock)
                            caller(cards_class, 'set_draw_interact', [player_selected, player_hover, player_id], cards_class_lock)
                    action = caller(cards_class, 'move', [event.pos, caller(table_class, 'get_rect', ['screen'], table_class_lock), caller(table_class, 'get_rects', [], table_class_lock), player_id], cards_class_lock)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and not pygame.mouse.get_pressed()[0]:
                        action = caller(cards_class, 'discard', [pygame.mouse.get_pos()], cards_class_lock)
                    if event.unicode.isalnum():
                        typed_word = (typed_word + event.unicode)[-10:]
                        if typed_word == reset_word:
                            network.send({'message_type': 'reset_game', 'message': player_id})
                            caller(cards_class, 'reset', [], cards_class_lock)
                        elif typed_word == reset_discarded_word:
                            network.send({'message_type': 'reset_discarded', 'message': player_id})
                            caller(cards_class, 'reset_discarded', [], cards_class_lock)
                    if event.unicode.isnumeric() and caller(table_class, 'get_collidepoint', ['players', pygame.mouse.get_pos()], table_class_lock):
                        network.send({'message_type': 'level_update', 'message': {'player': player_id, 'level': event.unicode}})
                        caller(players_class, 'set_level', [player_id, event.unicode], players_class_lock)
                    if caller(scores_class, 'collidepoint', [pygame.mouse.get_pos()], scores_class_lock):
                        score = None
                        if event.key == pygame.K_BACKSPACE:
                            score = caller(scores_class, 'backspace', [pygame.mouse.get_pos()], scores_class_lock)
                        elif event.unicode.isnumeric():
                            score = caller(scores_class, 'add_number', [pygame.mouse.get_pos(), event.unicode], scores_class_lock)
                        if score:
                            network.send({'message_type': 'score_update', 'message': score})
                            # print('score sent to server')

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_v:
                        caller(cards_class, 'cancel_expand', [], cards_class_lock)
                if pygame.key.get_pressed()[pygame.K_v]:
                    caller(cards_class, 'expand_card', [pygame.mouse.get_pos()], cards_class_lock)
                if action:
                    network.send({'message_type': 'card_update', 'message': action}) #action no formato {'id': X, 'data': Y} sendo Y igual o dicionario no servidor

            caller(table_class, 'update_equips_text', [player_selected, player_hover], table_class_lock) # colocar dentro da table, criar um metodo draw com table player e cards?

            caller(table_class, 'draw', [screen], table_class_lock)

            caller(players_class, 'draw', [screen, caller(cards_class, 'get_quantities', [], cards_class_lock)], players_class_lock)

            caller(scores_class, 'draw', [screen], scores_class_lock)

            caller(cards_class, 'draw', [screen], cards_class_lock)

            pygame.display.flip()

            clock.tick(FPS)

        pygame.quit()

        print('play ended')
    except Exception as e:
        print('play error ', e)
        network.send({'message_type': 'quit'})
        raise e