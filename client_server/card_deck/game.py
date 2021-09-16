import pygame
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table
from card_deck.players import Players
from threading import Thread
import time
cards_class = None
players = None
players_class = None
running = True

def listen(network):
    global cards_class
    global players_class
    global running
    global players
    print('sleeping...')
    # resolver isso daqui
    # depois que inicializar tudo na play setar um booleano pra liberar aqui?
    time.sleep(1)
    print('awake')
    while running:
        print('test')
        message = network.receive()
        #usar o mesmo padrao aqui, msg type e msg
        if message and cards_class:
            # print('message')
            if message['message_type'] == 'card_update':
                cards_class.update(message['message'])
            if message['message_type'] == 'player_disconnected':
                cards_class.discard_player(message['message'])
                players.remove(message['message'])
                players_class.update_players(players)
            elif message['message_type'] == 'players_update':
                print('player update')
                players.append(message['message']) #ou só mandar a lista de players novamente
                print(players)
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
    print('id do player é', player_id)
    print(players)

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

    players_class = Players(players, SCREEN_WIDTH, SCREEN_HEIGHT)

    

    while running:
        result = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('quitou')
                running = False
                network.send({'message_type': 'quit'})
            #mudado de elif para if
            #trocar nome de result para action
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   
                    
                    #pegar o selected dos players aqui se mouse no campo players
                    if table_class.fields['players'].rect.collidepoint(event.pos): #que codigo mais feio mano
                        # print('player selected = ', players_class.focused(pygame.mouse.get_pos()))
                        player_selected = players_class.focused(pygame.mouse.get_pos(), 'select')
                    # IMPEDIR CLICK RELEASE E REVEAL NOS EQUIPAMENTOS DE OUTRAS PESSOAS
                    #se eu jogar a logica de segurar click reveal release pra dentro da classe cards, não vai precisar desse monte de if else aqui
                    result = cards_class.click(event.pos, player_id) #ok
                    if result:
                        print('click')
                if event.button == 3 and not pygame.mouse.get_pressed()[0]:    
                    result = cards_class.reveal(event.pos, player_id) #ok
                    if result:
                        print('reveal')

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    result = cards_class.release(event.pos, table_class.get_rect('equipments'), table_class.get_rect('table'), table_class.get_rect('hand')) #ok
                    if result:
                        print('release')

            elif event.type == pygame.MOUSEMOTION:
                #pegar o hover dos players aqui se mouse no campo players
                #se mouse nao estiver no players ou equips selected = -1
                #se mouse nao estiver no players hover = -1
                if table_class.fields['players'].rect.collidepoint(event.pos):
                    # print('player hover = ', players_class.focused(pygame.mouse.get_pos()))
                    player_hover = players_class.focused(pygame.mouse.get_pos(), 'hover')
                elif not table_class.fields['equipments'].rect.collidepoint(event.pos):
                    #fazer um if player hover ou selected != -1 seta ambos como -1 e da um clear no players_class
                    if player_hover != -1 or player_selected != -1:
                        player_hover = -1
                        player_selected = -1
                        players_class.clear()
                result = cards_class.move(event.pos, table_class.get_rect('screen'), table_class.get_rects()) #ok
                # if result:
                #     print('move')
            
            elif event.type == pygame.KEYDOWN:
                # se tecla esc -> selected = -1
                if event.key == pygame.K_d and not pygame.mouse.get_pressed()[0]:
                    result = cards_class.discard(pygame.mouse.get_pos(), player_id)
                    if result:
                        print('discard')

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_v:
                    cards_class.cancel_expand()
            if pygame.key.get_pressed()[pygame.K_v]: #IMPEDIR CLICK, RELEASE,E DEMAIS FUNCOES ACIMA SE TIVER APERTANDO V
                cards_class.expand_card(pygame.mouse.get_pos(), SCREEN_WIDTH, SCREEN_HEIGHT, player_id)
            if result:
                network.send({'message_type': 'card_update', 'message': result}) #result no formato {'id': X, 'data': Y} sendo Y igual o dicionario no servidor
            # else:
            #     print('none')
        # fazer o if else e tratar o que for recebido
        # message = network.receive()
        # #usar o mesmo padrao aqui, msg type e msg
        # if message:
        #     # print('message')
        #     if message['message_type'] == 'card_update':
        #         # print('card')
        #         cards_class.update(message['message'])
        table_class.update_equips_text(player_selected, player_hover)

        table_class.draw(screen)

        cards_class.draw(screen, player_id, player_selected, player_hover)

        players_class.draw(screen)

        # print('selected=', player_selected, ' hover=', player_hover)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()