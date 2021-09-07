import pygame
from card import Card

t_1_w = 245
t_1_h = 351
treasure_1 = pygame.image.load("card_deck/images/treasure1.jpeg")

t_2_w = 500
t_2_h = 809
treasure_2 = pygame.image.load("card_deck/images/treasure2.jpeg")

d_1_w = 378
d_1_h = 585
door_1 = pygame.image.load("card_deck/images/door1.jpg")

d_2_w = 245
d_2_h = 351
door_2 = pygame.image.load("card_deck/images/door2.jpeg")

b_w = 379
b_h = 584
back = pygame.image.load("card_deck/images/back.jpg")

im_dimensions = {
    'treasure1.jpeg': [245, 351],
    'treasure2.jpeg': [500, 809],
    'door1.jpg': [378, 585],
    'door2.jpeg': [245, 351]
}

max_card_order = 0
t_discard = []
d_discard = []
t_discard_drag = []
d_discard_drag = []

class Cards:
    def __init__(self, c_w, c_h, t_pos, d_pos, t_discard_pos, d_discard_pos):
        self.cards = []
        self.door_back = Card(pygame.transform.smoothscale(back.subsurface((b_w, 0, b_w, b_h)), (c_w, c_h)),  0,  0,  c_w,  c_h,  -1, 'back', 0, 0, '')
        self.treasure_back = Card(pygame.transform.smoothscale(back.subsurface((0, 0, b_w, b_h)), (c_w, c_h)),  0,  0,  c_w,  c_h,  -1, 'back', 0, 0, '')
        self.t_pos = t_pos
        self.d_pos = d_pos
        self.t_discard_pos = t_discard_pos
        self.d_discard_pos = d_discard_pos
        self.expanded_card = None
        self.expanded_card_id = -1
        self.c_w = c_w
        self.c_h = c_h

        for i in range(70):
            self.cards.append(Card(pygame.transform.smoothscale(treasure_1.subsurface((i%10 * t_1_w, i//10 * t_1_h, t_1_w, t_1_h)), (c_w, c_h)),  t_pos[0],  t_pos[1],  c_w,  c_h,  i,  'treasure',  i%10 * t_1_w,  i//10 * t_1_h,  'treasure1.jpeg'))
            self.cards.append(Card(pygame.transform.smoothscale(treasure_2.subsurface((i%10 * t_2_w, i//10 * t_2_h, t_2_w, t_2_h)), (c_w, c_h)),  t_pos[0],  t_pos[1], c_w,  c_h,  70 + i,  'treasure',  i%10 * t_2_w,  i//10 * t_2_h,  'treasure2.jpeg'))
            self.cards.append(Card(pygame.transform.smoothscale(door_1.subsurface((i%10 * d_1_w, i//10 * d_1_h, d_1_w, d_1_h)), (c_w, c_h)),  d_pos[0],  d_pos[1], c_w,  c_h,  140 + i,  'door',  i%10 * d_1_w,  i//10 * d_1_h,  'door1.jpg'))
            self.cards.append(Card(pygame.transform.smoothscale(door_2.subsurface((i%10 * d_2_w, i//10 * d_2_h, d_2_w, d_2_h)), (c_w, c_h)),  d_pos[0],  d_pos[1],  c_w, c_h,  210 + i,  'door',  i%10 * d_2_w,  i//10 * d_2_h,  'door2.jpeg'))
    


    def draw(self, win):
        #desenha por padrao uma porta e tesouro no deck, a ultima e penultima de descarte e as que estão na mesa.
        self.cards.sort(key=lambda c: c.get_order())
        global t_discard
        global d_discard
        # win.blit(self.door_back.image, (self.d_pos[0], self.d_pos[1]))
        # win.blit(self.treasure_back.image, (self.t_pos[0], self.t_pos[1]))
        draw_count = 0
        t_draw = 0
        d_draw = 0

        if len(t_discard) > 2:
            for card in t_discard[-2:]:
                if not card.get_draging():
                    win.blit(card.image, (card.x, card.y))
                    draw_count = draw_count + 1
        else:
            for card in t_discard:
                if not card.get_draging():
                    win.blit(card.image, (card.x, card.y))
                    draw_count = draw_count + 1
        if len(d_discard) > 2:
            for card in d_discard[-2:]:
                if not card.get_draging():
                    win.blit(card.image, (card.x, card.y))
                    draw_count = draw_count + 1
        else:
            for card in d_discard:
                if not card.get_draging():
                    win.blit(card.image, (card.x, card.y))
                    draw_count = draw_count + 1

        for card in self.cards:
            if card.get_order() > 0:
                if card.get_face():
                    win.blit(card.image, (card.x, card.y))
                    draw_count = draw_count + 1
                else:
                    if card.get_type() == 'treasure':
                        win.blit(self.treasure_back.image, (card.x, card.y))
                        draw_count = draw_count + 1
                    else:
                        win.blit(self.door_back.image, (card.x, card.y))
                        draw_count = draw_count + 1
            elif t_draw < 2 and card.get_type() == 'treasure' and card not in t_discard:
                win.blit(self.treasure_back.image, (card.x, card.y))
                draw_count = draw_count + 1
                t_draw = t_draw + 1
            elif d_draw < 2 and card.get_type() == 'door' and card not in d_discard:
                win.blit(self.door_back.image, (card.x, card.y))
                draw_count = draw_count + 1
                d_draw = d_draw + 1
        if self.expanded_card:
            win.blit(self.expanded_card.image, (self.expanded_card.x, self.expanded_card.y))
        print(draw_count)

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
    
    def move(self, pos, rect_screen, rect_players, rect_logs, rect_deck):
        for card in self.cards:
            card.move(pos, rect_screen, rect_players, rect_logs, rect_deck)

    def reveal(self, pos):
        global max_card_order
        for card in reversed(self.cards):
            if card.reveal(pos):
                max_card_order = max_card_order + 1
                card.set_order(max_card_order)
                break

    def expand_card(self, pos, screen_width, screen_height):
        for card in reversed(self.cards):
            if card.focused(pos):
                if not(card.get_id() == self.expanded_card_id):
                    if card.get_im_name() == 'treasure1.jpeg':
                        self.expanded_card = Card(pygame.transform.smoothscale(treasure_1.subsurface((card.get_im_x(), card.get_im_y(), t_1_w, t_1_h)), (self.c_w * 2, self.c_h * 2)),  pos[0],  pos[1],  self.c_w * 2,  self.c_h * 2,  -1,  '',  0,  0,  '')
                    if card.get_im_name() == 'treasure2.jpeg':
                        self.expanded_card = Card(pygame.transform.smoothscale(treasure_2.subsurface((card.get_im_x(), card.get_im_y(), t_2_w, t_2_h)), (self.c_w * 2, self.c_h * 2)),  pos[0],  pos[1],  self.c_w * 2,  self.c_h * 2,  -1,  '',  0,  0,  '')
                    if card.get_im_name() == 'door1.jpg':
                        self.expanded_card = Card(pygame.transform.smoothscale(door_1.subsurface((card.get_im_x(), card.get_im_y(), d_1_w, d_1_h)), (self.c_w * 2, self.c_h * 2)),  pos[0],  pos[1],  self.c_w * 2,  self.c_h * 2,  -1,  '',  0,  0,  '')
                    if card.get_im_name() == 'door2.jpeg':
                        self.expanded_card = Card(pygame.transform.smoothscale(door_2.subsurface((card.get_im_x(), card.get_im_y(), d_2_w, d_2_h)), (self.c_w * 2, self.c_h * 2)),  pos[0],  pos[1],  self.c_w * 2,  self.c_h * 2,  -1,  '',  0,  0,  '')
                    self.expanded_card_id = card.get_id()
                else:
                    self.expanded_card.set_x_y(pos)
                break
    
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
                # if card.reveal(pos):
                #     max_card_order = max_card_order + 1
                #     card.set_order(max_card_order)
                #     break