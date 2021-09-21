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
    def __init__(self, screen_width, screen_height, cards_info, c_w, c_h, treasure_rect, font_size):
        self.max_card_order = 0
        self.cards = []
        self.back_cards = {'treasure': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((0, 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0), 
                           'door': DefaultCard(pygame.transform.smoothscale(images['back']['image'].subsurface((images['back']['w'], 0, images['back']['w'], images['back']['h'])), (c_w, c_h)),  0,  0)}
        self.expanded_card = None
        self.expanded_card_id = -1
        self.c_w = c_w
        self.c_h = c_h
        self.t_discard_pos = (treasure_rect.x + 0.51*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)
        self.d_discard_pos = (treasure_rect.x + 0.76*treasure_rect.w, treasure_rect.y + 0.03*treasure_rect.h)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.SysFont("comicsans", font_size)

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
            for j in range(70):
                im_idx = (i * 70) + j
                im_x = j%10 * im_w
                im_y = j//10 * im_h

                card = Card(pygame.transform.smoothscale(image.subsurface((im_x, im_y, im_w, im_h)), (c_w, c_h)),  0,  0,  im_idx,  im_type,  im_x,  im_y,  img_name)
                card.set_info(cards_info[im_idx], screen_width, screen_height)

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
        
        counts = {'deck': {'treasure': 0, 'door': 0}, 'discard': {'treasure': 0, 'door': 0}}
        for card in self.cards:
            # nesse for pegar os ultimos descartados e pegar a contagem dos decks e descarte
            if card.order == 0:
                counts['deck'][card.type] += 1
            elif card.discarded:
                counts['discard'][card.type] += 1

            if card.discarded:
                if card.type == 'treasure':
                    treasure_discard_list.append(card)
                else:
                    door_discard_list.append(card)

        for card in treasure_discard_list[-2:]:
            card.draw(win)
        text = self.font.render(str(counts['discard']['treasure']), 1, ((0, 0, 0)))
        win.blit(text, (self.t_discard_pos[0], self.t_discard_pos[1]))

        for card in door_discard_list[-2:]:
            card.draw(win)
        text = self.font.render(str(counts['discard']['door']), 1, ((0, 0, 0)))
        win.blit(text, (self.d_discard_pos[0], self.d_discard_pos[1]))

        for card in self.cards:
            #inverter a ordem para desenhar os tesouros primeiro e colocar a contagem nos mesmos
            if not card.discarded:
                if card.order == 0:
                    if t_draw < 2 and card.get_type() == 'treasure':
                        self.back_cards['treasure'].draw_at(win, (card.x, card.y))
                        t_draw = t_draw + 1
                        if t_draw == 2:
                            text = self.font.render(str(counts['deck']['treasure']), 1, ((0, 0, 0)))
                            win.blit(text, (card.x, card.y))

                    elif d_draw < 2 and card.get_type() == 'door':
                        self.back_cards['door'].draw_at(win, (card.x, card.y))
                        d_draw = d_draw + 1
                        if d_draw == 2:
                            text = self.font.render(str(counts['deck']['door']), 1, ((0, 0, 0)))
                            win.blit(text, (card.x, card.y))

                elif card.to_draw:
                    if card.get_face():
                        card.draw(win)
                    else:
                        self.back_cards[card.get_type()].draw_at(win, (card.x, card.y))
                    if card.draging:
                        text = self.font.render(str(card.p_id), 1, ((0, 0, 0)))
                        win.blit(text, (card.x, card.y))

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
                return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        for card in self.cards:
            if card.interact and card.get_draging():
                card.release(pos, rect_equipments, rect_table, rect_hand)
                return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def move(self, pos, rect_screen, rects, player_id):
        for card in self.cards:
            if card.p_id == player_id:
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
                # retornar um false se tiver hoverando e não puder descartar, n tem pq checar mais 
                if card.try_discard(pos, self.t_discard_pos, self.d_discard_pos):
                    self.max_card_order = self.max_card_order + 1
                    card.set_order(self.max_card_order)
                    return card.get_info(self.screen_width, self.screen_height)
        return None
    
    def update(self, message):
        #transformar cards num dicionario, vai facilitar aqui
        for card in self.cards:
            if card.id == message['id']:
                print(message['data']['draging'], card.draging)
                if not message['data']['draging'] and card.draging:
                    print("someone else released a card")

                card.set_info(message['data'], self.screen_width, self.screen_height)

                if message['data']['order'] > self.max_card_order:
                    self.max_card_order = message['data']['order']
    
    def discard_player(self, disconnected_player_id):
        for card in self.cards:
            if card.p_id == disconnected_player_id and not card.discarded:
                card.discard(self.t_discard_pos, self.d_discard_pos)

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
            
            if card.to_draw and not (card.area == 'equipments' and card.p_id != player_id) and not(card.draging and card.p_id != player_id):
                    card.interact = True
            else:
                card.interact = False
    
    def get_quantities(self):
        quantities = {}
        for card in self.cards:
            if card.area in ['hand', 'equipments']:
                if not card.p_id in quantities:
                    quantities[card.p_id] = {'hand': 0, 'equipments': 0}
                quantities[card.p_id][card.area] += 1
        return quantities

def get_id_to_draw(player_selected, player_hover, player_id):
    if not player_selected == -1:
        return player_selected
    elif not player_hover == -1:
        return player_hover
    else:
        return player_id