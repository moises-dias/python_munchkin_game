import pygame
from ctypes import windll
from card_deck.cards import Cards
from card_deck.table import Table

def play(network):
    # DEFAULT_WIDTH = 1580
    # DEFAULT_HEIGHT = 950
    # DEFAULT_SCALE_X = 137
    # DEFAULT_SCALE_Y = 222
    DEFAULT_WIDTH = 527
    DEFAULT_HEIGHT = 317
    DEFAULT_SCALE_X = 46
    DEFAULT_SCALE_Y = 74

    FPS = 30

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

    table_class = Table(SCREEN_WIDTH, SCREEN_HEIGHT)

    cards_info = network.get_all_cards()

    cards_class = Cards(SCREEN_WIDTH, SCREEN_HEIGHT, cards_info, scale_x, scale_y, table_class.get_rect('deck'))

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:    
                    cards_class.click(event.pos) 
                if event.button == 3 and not pygame.mouse.get_pressed()[0]:    
                    cards_class.reveal(event.pos) 

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    cards_class.release(event.pos, table_class.get_rect('equipments'), table_class.get_rect('table'), table_class.get_rect('hand')) 

            elif event.type == pygame.MOUSEMOTION:
                result = cards_class.move(event.pos, table_class.get_rect('screen'))
                if result:
                    network.move(result)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and not pygame.mouse.get_pressed()[0]:
                    cards_class.discard(pygame.mouse.get_pos())

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_v:
                    cards_class.cancel_expand()
                    # network.send(['test'])
            if pygame.key.get_pressed()[pygame.K_v]: #IMPEDIR CLICK, RELEASE,E DEMAIS FUNCOES ACIMA SE TIVER APERTANDO V
                cards_class.expand_card(pygame.mouse.get_pos(), SCREEN_WIDTH, SCREEN_HEIGHT)
            # network.send()
        # fazer o if else e tratar o que for recebido
        message = network.receive()
        if message:
            # print('message')
            if message[0] == 'card':
                # print('card')
                cards_class.update(message[1])

        table_class.draw(screen)

        cards_class.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()