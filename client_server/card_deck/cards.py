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

class Cards:
    def __init__(self, screen_width, screen_height, cards_info, c_w, c_h, treasure_rect):
        self.max_card_order = 0
        self.cards = []
        self.back_cards = {'treasure': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((0, 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0), 
                           'door': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((images['back']['w'], 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0)}
        self.expanded_card = None
        self.expanded_card_id = -1
        self.c_w = c_w
        self.c_h = c_h
        # self.t_pos =         (treasure_rect.x + 0.01*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        # self.d_pos =         (treasure_rect.x + 0.26*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.t_discard_pos = (treasure_rect.x + 0.51*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.d_discard_pos = (treasure_rect.x + 0.76*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)

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
                
                # init_x = cards_info[im_idx]['x'] * screen_width
                # init_y = cards_info[im_idx]['y'] * screen_height

                im_x = j%10 * im_w
                im_y = j//10 * im_h

                card = Card(pygame.transform.smoothscale(image.subsurface((im_x, im_y, im_w, im_h)), (c_w, c_h)),  0,  0,  im_idx,  im_type,  im_x,  im_y,  img_name)
                
                # metodo no card q recebe um dict e atribui aos atributos
                # card.p_id = cards_info[im_idx]['p_id']
                # card.draging = cards_info[im_idx]['draging']
                # card.order = cards_info[im_idx]['order']
                # card.face = cards_info[im_idx]['face']
                # card.area = cards_info[im_idx]['area']
                # card.discarded = cards_info[im_idx]['discarded']
                
                cards_info[im_idx]['x'] = cards_info[im_idx]['x'] * screen_width
                cards_info[im_idx]['y'] = cards_info[im_idx]['y'] * screen_height

                card.set_info(cards_info[im_idx])
                
                self.cards.append(card)

                if card.order > self.max_card_order:
                    self.max_card_order = card.order

        random.shuffle(self.cards)

    def draw(self, win):
        self.cards.sort(key=lambda c: c.get_order())
        t_draw = 0
        d_draw = 0

        door_discard_list = []
        treasure_discard_list = []

        for card in self.cards:
            if card.discarded:
                if card.type == 'treasure':
                    treasure_discard_list.append(card)
                else:
                    door_discard_list.append(card)
        for card in treasure_discard_list[-2:]:
            card.draw(win)
        for card in door_discard_list[-2:]:
            card.draw(win)

        for card in self.cards:
            if card.get_order() > 0 and not card.discarded and card.to_draw:
                if card.get_face():
                    card.draw(win)
                else:
                    self.back_cards[card.get_type()].draw_at(win, (card.x, card.y))
                if card.draging:
                    # melhorar isso, nao precisa criar a font toda vez, jogar dentro da classe card e criar um método
                    font = pygame.font.SysFont("comicsans", 40)
                    text = font.render(str(card.p_id), 1, (255,255,255))
                    win.blit(text, (card.x, card.y))
            elif t_draw < 2 and card.get_type() == 'treasure' and not card.discarded:
                self.back_cards['treasure'].draw_at(win, (card.x, card.y))
                t_draw = t_draw + 1
            elif d_draw < 2 and card.get_type() == 'door' and not card.discarded:
                self.back_cards['door'].draw_at(win, (card.x, card.y))
                d_draw = d_draw + 1
        if self.expanded_card:
            self.expanded_card.draw(win)

    def get_cards(self):
        return self.cards
    
    def click(self, pos, player_id):
        for card in reversed(self.cards):     
            if not card.to_draw or not card.interact:
                continue
            if card.click(pos):
                card.p_id = player_id
                self.max_card_order = self.max_card_order + 1
                card.set_order(self.max_card_order)
                card.last_discarded = card.discarded
                card.discarded = False
                return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        for card in self.cards:
            if card.get_draging():
                # if not card.release(pos, rect_equipments, rect_table, rect_hand):
                #     if card.last_discarded:
                #         card.discarded = True
                #         card.face = True
                #         card.area = 'deck'
                card.release(pos, rect_equipments, rect_table, rect_hand)
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
                        break
                return card.get_info(self.screen_width, self.screen_height)
        return None

    def reveal(self, pos):
        for card in reversed(self.cards):
            if card.discarded or not card.to_draw or not card.interact:
                continue
            if card.focused(pos):
                if card.reveal(pos):
                    self.max_card_order = self.max_card_order + 1
                    card.set_order(self.max_card_order)
                return card.get_info(self.screen_width, self.screen_height)
        return None

    def expand_card(self, pos):
        card_focused = False
        for card in reversed(self.cards):
            if card.focused(pos) and card.to_draw:
                if not card.get_face():
                    break
                
                if pos[0] < self.screen_width/2:
                    card_x = pos[0]
                else:
                    card_x = pos[0] - self.c_w * 2
                if pos[1] < self.screen_height/2:
                    card_y = pos[1]
                else:
                    card_y = pos[1] - self.c_h * 2
                if not(card.get_id() == self.expanded_card_id):
                    im_name = card.get_im_name()
                    image = images[im_name]['image']
                    im_w = images[im_name]['w']
                    im_h = images[im_name]['h']
                    expanded_image = pygame.transform.smoothscale(image.subsurface((card.get_im_x(), card.get_im_y(), im_w, im_h)), (self.c_w * 2, self.c_h * 2))
                    self.expanded_card = DefaultCard(expanded_image,  card_x,  card_y)
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

    def discard(self, pos):
        for card in reversed(self.cards):
            if card.get_order() > 0 and not card.discarded and card.to_draw and card.interact:
                if card.try_discard(pos, self.t_discard_pos, self.d_discard_pos):
                    # card.discarded = True
                    # card.face = True
                    # card.area = 'deck'
                    self.max_card_order = self.max_card_order + 1
                    card.set_order(self.max_card_order)
                    return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def update(self, message):
        #transformar cards num dicionario, vai facilitar aqui
        for card in self.cards:
            if card.id == message['id']:
                # card.x = card.rect.x = message['data']['x'] * self.screen_width
                # card.y = card.rect.y = message['data']['y'] * self.screen_height
                # card.p_id = message['data']['p_id']
                # card.draging = message['data']['draging']
                # card.order = message['data']['order']
                # card.face = message['data']['face']
                # card.area = message['data']['area']
                # card.discarded = message['data']['discarded']

                # ver algum jeito de nao ter que multiplicar o x e y por width e height, fazer isso aonde?
                message['data']['x'] = message['data']['x'] * self.screen_width
                message['data']['y'] = message['data']['y'] * self.screen_height
                card.set_info(message['data'])

                if message['data']['order'] > self.max_card_order:
                    self.max_card_order = message['data']['order']
    
    def discard_player(self, disconnected_player_id):
        for card in self.cards:
            if card.p_id == disconnected_player_id and not card.discarded:
                card.discard(self.t_discard_pos, self.d_discard_pos)
                # card.discarded = True
                # card.face = True
                # card.area = 'deck'
                # card.draging = False
                # card.to_draw = True
                # card.interact = True
                # if card.type == 'treasure':
                #     card.x = card.rect.x = self.t_discard_pos[0]
                #     card.y = card.rect.y = self.t_discard_pos[1]
                # else:
                #     card.x = card.rect.x = self.d_discard_pos[0]
                #     card.y = card.rect.y = self.d_discard_pos[1]
    
    def set_draw_interact(self, player_selected, player_hover, player_id):
        for card in self.cards:
            if card.area in ['deck', 'table', 'players', 'logs']:
                card.to_draw = True
            elif card.area == 'hand' and card.p_id == player_id:
                card.to_draw = True
            elif card.area == 'equipments' and card.p_id == get_id_to_draw(player_selected, player_hover, player_id):
                card.to_draw = True
            else:
                card.to_draw = False
            
            if card.to_draw and not (card.area == 'equipments' and card.p_id != player_id):
                    card.interact = True
            else:
                card.interact = False
            

def get_id_to_draw(player_selected, player_hover, player_id):
    if not player_selected == -1:
        return player_selected
    elif not player_hover == -1:
        return player_hover
    else:
        return player_id