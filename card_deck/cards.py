import pygame
from card import Card
from default_card import DefaultCard
import random
import json

images = {
    'treasure1': {'image': pygame.image.load("card_deck/images/treasure1.jpeg"), 'w': 245, 'h': 351, 'type': 'treasure'},
    'treasure2': {'image': pygame.image.load("card_deck/images/treasure2.jpeg"), 'w': 500, 'h': 809, 'type': 'treasure'},
    'door1': {'image': pygame.image.load("card_deck/images/door1.jpg"), 'w': 378, 'h': 585, 'type': 'door'},
    'door2': {'image': pygame.image.load("card_deck/images/door2.jpeg"), 'w': 245, 'h': 351, 'type': 'door'},
    'back': {'image': pygame.image.load("card_deck/images/back.jpg"), 'w': 379, 'h': 584, 'type': 'back'}
}

max_card_order = 0
t_discard = []
d_discard = []
t_discard_drag = []
d_discard_drag = []

class Cards:
    def __init__(self, c_w, c_h, treasure_rect):
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
            if im_type == 'treasure':
                init_x, init_y = self.t_pos
            else:
                init_x, init_y = self.d_pos
            for j in range(70):
                im_x = j%10 * im_w
                im_y = j//10 * im_h
                im_idx = (i * 70) + j
                self.cards.append(Card(pygame.transform.smoothscale(image.subsurface((im_x, im_y, im_w, im_h)), (c_w, c_h)),  init_x,  init_y,  im_idx,  im_type,  im_x,  im_y,  img_name))

        random.shuffle(self.cards)

    def draw(self, win):
        self.cards.sort(key=lambda c: c.get_order())
        global t_discard
        global d_discard
        t_draw = 0
        d_draw = 0

        for discard_list in [t_discard, d_discard]:
            if len(discard_list) > 2:
                for card in discard_list[-2:]:
                    if not card.get_draging(): # draging implica order > 0
                        card.draw(win)
            else:
                for card in discard_list:
                    if not card.get_draging():
                        card.draw(win)

        for card in self.cards:
            if card.get_order() > 0:
                if card.get_face():
                    card.draw(win)
                else:
                    self.back_cards[card.get_type()].draw_at(win, (card.x, card.y))
            elif t_draw < 2 and card.get_type() == 'treasure' and card not in t_discard:
                self.back_cards['treasure'].draw_at(win, (card.x, card.y))
                t_draw = t_draw + 1
            elif d_draw < 2 and card.get_type() == 'door' and card not in d_discard:
                self.back_cards['door'].draw_at(win, (card.x, card.y))
                d_draw = d_draw + 1
        if self.expanded_card:
            self.expanded_card.draw(win)

    def get_cards(self):
        return self.cards
    
    def click(self, pos):
        global t_discard
        global d_discard
        global t_discard_drag
        global d_discard_drag
        global max_card_order
        for card in reversed(self.cards):     
            if card.click(pos):
                max_card_order = max_card_order + 1
                card.set_order(max_card_order)
                if card in t_discard:
                    t_discard.remove(card)
                    t_discard_drag.append(card)
                if card in d_discard:
                    d_discard.remove(card)
                    d_discard_drag.append(card)
                break
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        global t_discard
        global d_discard
        global t_discard_drag
        global d_discard_drag
        for card in self.cards:
            if not card.release(pos, rect_equipments, rect_table, rect_hand):
                if card in t_discard_drag:
                    t_discard.append(card)
                if card in d_discard_drag:
                    d_discard.append(card)
            if card in t_discard_drag:
                t_discard_drag.remove(card)
            if card in d_discard_drag:
                d_discard_drag.remove(card)
    
    def move(self, pos, rect_screen):
        for card in self.cards:
            if card.move(pos, rect_screen):
                break

    def reveal(self, pos):
        global max_card_order
        for card in reversed(self.cards):
            if card.focused(pos):
                if card.reveal(pos):
                    max_card_order = max_card_order + 1
                    card.set_order(max_card_order)
                break

    def expand_card(self, pos, screen_width, screen_height):
        card_focused = False
        for card in reversed(self.cards):
            if card.focused(pos):
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

    def discard(self, pos):
        global t_discard
        global d_discard
        for card in reversed(self.cards):
            if card.get_order() > 0:
                if card.discard(pos, self.t_discard_pos, self.d_discard_pos):
                    if card.get_type() == 'treasure':
                        t_discard.append(card)
                    else:
                        d_discard.append(card)
                    break