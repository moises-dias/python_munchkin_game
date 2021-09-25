from card_deck.field import Field
import random
import pygame

WHITE = (255, 255, 255)
DECK = (52, 97, 47)
PLAYERS = (122, 224, 110)
TABLE = (160, 230, 158)
EQUIPMENTS = (16, 102, 6)
HAND = (94, 173, 85)
LOGS = (94, 173, 85)
# table: c
# nomes: a
# equips: d
# hand: e
# baralho: b
# logs: e

class Table:
    def __init__(self, screen_width, screen_height, player_id, x_limits, y_limits, font_size):
        self.fields = {
            'screen':     Field(0,           0,           screen_width,                 screen_height,                 WHITE, 'screen', font_size),
            'players':    Field(0,           0,           x_limits[0],                  y_limits[0],                   PLAYERS, 'players', font_size),
            'hand':       Field(0,           y_limits[1], x_limits[0],                  (screen_height - y_limits[1]), HAND, 'hand', font_size),
            'equipments': Field(0,           y_limits[0], x_limits[0],                  (y_limits[1] - y_limits[0]),   EQUIPMENTS, 'equipments', font_size),
            'table':      Field(x_limits[0], 0,           (screen_width - x_limits[0]), y_limits[1],                   TABLE, 'table', font_size),
            'deck':       Field(x_limits[0], y_limits[1], (x_limits[1] - x_limits[0]),  (screen_height - y_limits[1]), DECK, 'deck', font_size),
            'logs':       Field(x_limits[1], y_limits[1], (screen_width - x_limits[1]), (screen_height - y_limits[1]), LOGS, 'logs', font_size)
        }
        self.player_id = player_id
        self.last_id = player_id
        self.fields['equipments'].set_name(f"{player_id}'s equips")

        self.font = pygame.font.Font("client_server/card_deck/fonts/comicsans.ttf", font_size*6)
        self.dice_count = 0
        self.dice_result = '1'
    
    def get_rect(self, field_name):
        return self.fields[field_name].get_rect()

    def draw(self, win):
        for field_name, field in self.fields.items():
            if not field_name == 'screen':
                field.draw(win)
        self.draw_dice_number(win)
    
    def get_rects(self):
        return self.fields
    
    def get_collidepoint(self, field, pos):
        return self.fields[field].rect.collidepoint(pos)
    
    def dice_roll(self, dice_result):
        self.dice_count = 30
        if dice_result:
            self.dice_result = dice_result
        else:
            self.dice_result = str(random.randint(1, 6))
        return self.dice_result


    def draw_dice_number(self, win):
        if self.dice_count > 0:
            self.dice_count -= 1
            text_to_draw = self.font.render(str(random.randint(1, 6)), 1, (0, 0, 0))
        else:
            text_to_draw = self.font.render(self.dice_result, 1, (0, 0, 0))
        win.blit(text_to_draw, (1.075 * self.fields['logs'].x, 0.97 * self.fields['logs'].y))

    def update_equips_text(self, player_selected, player_hover):
        if player_selected != -1:
            id_to_draw = player_selected
        elif player_hover != -1:
            id_to_draw = player_hover
        else:
            id_to_draw = self.player_id

        if id_to_draw != self.last_id:
            self.fields['equipments'].set_name(f"{id_to_draw}'s equips")
            self.last_id = id_to_draw
