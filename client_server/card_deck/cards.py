import pygame
from card_deck.card import Card
from card_deck.default_card import DefaultCard
import random
import json

images = {
    'treasure1': {'image': pygame.image.load("card_deck/images/treasure1.jpeg"), 'w': 245, 'h': 351, 'type': 'treasure'},
    'treasure2': {'image': pygame.image.load("card_deck/images/treasure2.jpeg"), 'w': 500, 'h': 809, 'type': 'treasure'},
    'door1': {'image': pygame.image.load("card_deck/images/door1.jpg"), 'w': 378, 'h': 585, 'type': 'door'},
    'door2': {'image': pygame.image.load("card_deck/images/door2.jpeg"), 'w': 245, 'h': 351, 'type': 'door'},
    'back': {'image': pygame.image.load("card_deck/images/back.jpg"), 'w': 379, 'h': 584, 'type': 'back'}
}

# colocar essas variaveis dentro da classe?
max_card_order = 0
t_discard = []
d_discard = []
t_discard_drag = []
d_discard_drag = []
class Cards:
    def __init__(self, screen_width, screen_height, cards_info, c_w, c_h, treasure_rect):
        global max_card_order
        self.cards = []
        self.back_cards = {'treasure': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((0, 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0), 
                           'door': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((images['back']['w'], 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0)}
        self.expanded_card = None
        self.expanded_card_id = -1
        self.c_w = c_w
        self.c_h = c_h
        self.t_pos =         (treasure_rect.x + 0.01*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.d_pos =         (treasure_rect.x + 0.26*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.t_discard_pos = (treasure_rect.x + 0.51*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.d_discard_pos = (treasure_rect.x + 0.76*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)

        #tirar isso, n tem pq ter screen width e height no cards, mas colocar onde?
        self.screen_width = screen_width
        self.screen_height = screen_height

        # preencher o json card_names
        # with open('card_deck/card_names.json') as test:
        #     data = json.load(test)
        # print(data)
        # print(type(data))

        for i, (img_name, img_attrs) in enumerate(images.items()):
            if img_name == 'back':
                continue
            image = img_attrs['image']
            im_w = img_attrs['w']
            im_h = img_attrs['h']
            im_type = img_attrs['type']
            # if im_type == 'treasure':
            #     init_x, init_y = self.t_pos
            # else:
            #     init_x, init_y = self.d_pos
            for j in range(70):
                im_idx = (i * 70) + j
                
                init_x = cards_info[im_idx]['x'] * screen_width
                init_y = cards_info[im_idx]['y'] * screen_height

                im_x = j%10 * im_w
                im_y = j//10 * im_h

                c = Card(pygame.transform.smoothscale(image.subsurface((im_x, im_y, im_w, im_h)), (c_w, c_h)),  init_x,  init_y,  im_idx,  im_type,  im_x,  im_y,  img_name)
                
                # c.last_x = cards_info[im_idx]['last_x'] * self.screen_height
                # c.last_y = cards_info[im_idx]['last_y'] * self.screen_height
                c.draging = cards_info[im_idx]['draging']
                # c.type = cards_info[im_idx]['type']
                c.order = cards_info[im_idx]['order']
                # c.last_order = cards_info[im_idx]['last_order']
                c.face = cards_info[im_idx]['face']
                c.p_id = cards_info[im_idx]['p_id']
                c.area = cards_info[im_idx]['area']
                c.discarded = cards_info[im_idx]['discarded']
                if c.discarded and not c.face:
                    print('YO WTF')
                    print('YO WTF')
                    print('YO WTF')
                    print('YO WTF')
                
                self.cards.append(c)

                if c.order > max_card_order:
                    max_card_order = c.order
                


                #dar um random.shuffle na lista la no servidor, e aqui ordenar pela ordem no servidor
                #mas e qnd o jogo ja tiver começado? ordena como?

        #comentado para testar o servidor, mas não vai mais ser necessário, shuffle deve ficar no server ao iniciar as cartas
        random.shuffle(self.cards)

    def draw(self, win, player_id, player_selected, player_hover):
        self.cards.sort(key=lambda c: c.get_order())
        # global t_discard
        # global d_discard
        t_draw = 0
        d_draw = 0

        # # remover esse for
        # for card in self.cards:
        #     card.draw(win)
        # return

        # for discard_list in [t_discard, d_discard]:
        #     if len(discard_list) > 2:
        #         for card in discard_list[-2:]:
        #             if not card.get_draging(): # draging implica order > 0
        #                 card.draw(win)
        #     else:
        #         for card in discard_list:
        #             if not card.get_draging():
        #                 card.draw(win)
        door_discard_list = []
        treasure_discard_list = []

        for card in self.cards:
            if card.discarded:
                # print('card is discarded')
                if card.type == 'treasure':
                    treasure_discard_list.append(card)
                else:
                    door_discard_list.append(card)
        for card in treasure_discard_list[-2:]:
            # print('t')
            card.draw(win)
        for card in door_discard_list[-2:]:
            # print('d')
            card.draw(win)

        for card in self.cards:
            #se id diferente e carta na area hand:
            # continue
            if card.area == 'hand' and not (card.p_id == player_id):
                continue
            if card.area == 'equipments':
                # print(player_selected, player_hover, player_id, card.p_id)
                if not player_selected == -1:
                    id_to_draw = player_selected
                    # print('')
                elif not player_hover == -1:
                    id_to_draw = player_hover
                else:
                    id_to_draw = player_id
                if not card.p_id == id_to_draw:
                    continue
            
            # if card.discarded:
            #     print('card is discarded')
            #     if card.type == 'treasure':
            #         treasure_discard_list.append(card)
            #     else:
            #         door_discard_list.append(card)
            if card.get_order() > 0 and not card.discarded:
                if card.get_face():
                    card.draw(win)
                else:
                    # print('begin')
                    # print(card.get_type())
                    # print('end')
                    self.back_cards[card.get_type()].draw_at(win, (card.x, card.y))
                #printar id no x, y
                if card.draging: # and card.area != 'equipments' and card.area != 'hand':
                    # melhorar isso, nao precisa criar a font toda vez
                    font = pygame.font.SysFont("comicsans", 40)
                    text = font.render(str(card.p_id), 1, (255,255,255))
                    win.blit(text, (card.x, card.y))
            elif t_draw < 2 and card.get_type() == 'treasure' and not card.discarded: # and card not in t_discard:
                self.back_cards['treasure'].draw_at(win, (card.x, card.y))
                t_draw = t_draw + 1
            elif d_draw < 2 and card.get_type() == 'door' and not card.discarded: # and card not in d_discard:
                self.back_cards['door'].draw_at(win, (card.x, card.y))
                d_draw = d_draw + 1
        if self.expanded_card:
            self.expanded_card.draw(win)
        # for card in treasure_discard_list[-2:]:
        #     print('t')
        #     card.draw(win)
        # for card in door_discard_list[-2:]:
        #     print('d')
        #     card.draw(win)

    def get_cards(self):
        return self.cards
    
    def click(self, pos, player_id):
        global t_discard
        global d_discard
        global t_discard_drag
        global d_discard_drag
        global max_card_order
        for card in reversed(self.cards):     
            if card.area in ['equipments', 'hand'] and not (card.p_id == player_id):
                continue
            if card.click(pos):
                card.p_id = player_id
                max_card_order = max_card_order + 1
                card.set_order(max_card_order)
                
                card.last_discarded = card.discarded
                card.discarded = False
                # if card in t_discard:
                #     t_discard.remove(card)
                #     t_discard_drag.append(card)
                # if card in d_discard:
                #     d_discard.remove(card)
                #     d_discard_drag.append(card)
                return card.get_info(self.screen_width, self.screen_height)
                # break
        return None
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        global t_discard
        global d_discard
        global t_discard_drag
        global d_discard_drag
        for card in self.cards:
            if card.get_draging():
                if not card.release(pos, rect_equipments, rect_table, rect_hand):
                    if card.last_discarded:
                        card.discarded = True
                        card.face = True
                        card.area = 'deck'
                #     if card in t_discard_drag:
                #         t_discard.append(card)
                #     if card in d_discard_drag:
                #         d_discard.append(card)
                # if card in t_discard_drag:
                #     t_discard_drag.remove(card)
                # if card in d_discard_drag:
                #     d_discard_drag.remove(card)
                return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def move(self, pos, rect_screen, rects):
        for card in self.cards:
            if card.move(pos, rect_screen):
                for rect_name, rect in rects.items():
                    if rect_name == 'screen':
                        continue
                    if rect.get_rect().collidepoint(pos):
                        card.area = rect_name
                        print(card.area)
                        break
                return card.get_info(self.screen_width, self.screen_height)
                # break
        return None

    def reveal(self, pos, player_id):
        global max_card_order
        for card in reversed(self.cards):
            if card.discarded or (card.area in ['equipments', 'hand'] and not (card.p_id == player_id)):
                continue
            if card.focused(pos):
                if card.reveal(pos):
                    max_card_order = max_card_order + 1
                    card.set_order(max_card_order)
                return card.get_info(self.screen_width, self.screen_height)
                # break
        return None

    def expand_card(self, pos, screen_width, screen_height, player_id, player_selected):
        card_focused = False
        for card in reversed(self.cards):
            if card.focused(pos) and not (card.area == 'hand' and not (card.p_id == player_id)) and (card.area == 'equipments' and (player_selected == card.p_id or player_selected == -1 and card.p_id == player_id)): #fazer o if card.desenhado T/F resolve isso...
                if not card.get_face():
                    break
                
                if pos[0] < screen_width/2:
                    card_x = pos[0]
                else:
                    card_x = pos[0] - self.c_w * 2
                if pos[1] < screen_height/2:
                    card_y = pos[1]
                else:
                    card_y = pos[1] - self.c_h * 2
                if not(card.get_id() == self.expanded_card_id):
                    im_name = card.get_im_name()
                    image = images[im_name]['image']
                    im_w = images[im_name]['w']
                    im_h = images[im_name]['h']
                    self.expanded_card = DefaultCard(pygame.transform.smoothscale(image.subsurface((card.get_im_x(), card.get_im_y(), im_w, im_h)), (self.c_w * 2, self.c_h * 2)),  card_x,  card_y)
                    self.expanded_card_id = card.get_id()
                else:
                    self.expanded_card.set_x_y(card_x, card_y)
                card_focused = True
                break
        if not card_focused:
            self.cancel_expand()
    
    def cancel_expand(self):
        self.expanded_card = None
        self.expanded_card_id = -1

    def discard(self, pos, player_id):
        global max_card_order
        # global t_discard
        # global d_discard
        for card in reversed(self.cards):
            if card.get_order() > 0 and not card.discarded and not (card.area in ['equipments', 'hand'] and not (card.p_id == player_id)):
                if card.discard(pos, self.t_discard_pos, self.d_discard_pos):
                    print('discard okay')
                    card.discarded = True
                    card.face = True
                    card.area = 'deck'
                    max_card_order = max_card_order + 1
                    card.set_order(max_card_order)
                    return card.get_info(self.screen_width, self.screen_height)
                    # if card.get_type() == 'treasure':
                    #     t_discard.append(card)
                    # else:
                    #     d_discard.append(card)
                    # break
        return None
    
    def update(self, message):
        global max_card_order
        #transformar cards num dicionario
        for c in self.cards:
            # print(message)
            if c.id == message['id']:
                c.x = c.rect.x = message['data']['x'] * self.screen_width
                c.y = c.rect.y = message['data']['y'] * self.screen_height
                # c.last_x = message['data']['last_x'] * self.screen_height
                # c.last_y = message['data']['last_y'] * self.screen_height
                c.draging = message['data']['draging']
                # c.type = message['data']['type']
                c.order = message['data']['order']
                # c.last_order = message['data']['last_order']
                c.face = message['data']['face']
                c.p_id = message['data']['p_id']
                c.area = message['data']['area']
                c.discarded = message['data']['discarded']

                if message['data']['order'] > max_card_order:
                    max_card_order = message['data']['order']
    
    def discard_player(self, disconnected_player_id):
        for card in self.cards:
            if card.p_id == disconnected_player_id and not card.discarded: # e carta na mao ou equips, não descarta as da mesa
                card.discarded = True
                card.face = True
                card.area = 'deck'
                card.draging = False
                # card.order = 0 # colocar last order + 1
                if card.type == 'treasure':
                    card.x = card.rect.x = self.t_discard_pos[0]
                    card.y = card.rect.y = self.t_discard_pos[1]
                else:
                    card.x = card.rect.x = self.d_discard_pos[0]
                    card.y = card.rect.y = self.d_discard_pos[1]