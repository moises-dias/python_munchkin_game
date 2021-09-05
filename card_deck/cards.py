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

max_card_order = 0

class Cards:
    def __init__(self, c_w, c_h, t_pos, d_pos, t_discard_pos, d_discard_pos):
        self.cards = []
        self.door_back = None
        self.treasure_back = None
        self.t_pos = t_pos
        self.d_pos = d_pos
        self.t_discard_pos = t_discard_pos
        self.d_discard_pos = d_discard_pos

        #colocar id nas cartas
        for i in range(70):
            self.cards.append(Card(pygame.transform.smoothscale(treasure_1.subsurface((i%10 * t_1_w, i//10 * t_1_h, t_1_w, t_1_h)), (c_w, c_h)),  t_pos[0],  t_pos[1],  c_w,  c_h,  i))
            self.cards.append(Card(pygame.transform.smoothscale(treasure_2.subsurface((i%10 * t_2_w, i//10 * t_2_h, t_2_w, t_2_h)), (c_w, c_h)),  t_pos[0],  t_pos[1], c_w,  c_h,  70 + i))
            self.cards.append(Card(pygame.transform.smoothscale(door_1.subsurface((i%10 * d_1_w, i//10 * d_1_h, d_1_w, d_1_h)), (c_w, c_h)),  d_pos[0],  d_pos[1], c_w,  c_h,  140 + i))
            self.cards.append(Card(pygame.transform.smoothscale(door_2.subsurface((i%10 * d_2_w, i//10 * d_2_h, d_2_w, d_2_h)), (c_w, c_h)),  d_pos[0],  d_pos[1],  c_w, c_h,  210 + i))
    
    def draw(self, win):
        #desenha por padrao uma porta e tesouro no deck, a ultima e penultima de descarte e as que estão na mesa.
        self.cards.sort(key=lambda c: c.get_order())

        for card in self.cards:
            win.blit(card.image, (card.x, card.y))

    def get_cards(self):
        return self.cards
    
    def click(self, pos):
        global max_card_order
        for card in reversed(self.cards):     
            if card.click(pos):
                max_card_order = max_card_order + 1
                card.set_order(max_card_order)
                break
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        for card in self.cards:
            card.release(pos, rect_equipments, rect_table, rect_hand)
    
    def move(self, pos, rect_screen, rect_players, rect_logs, rect_deck):
        for card in self.cards:
            card.move(pos, rect_screen, rect_players, rect_logs, rect_deck)