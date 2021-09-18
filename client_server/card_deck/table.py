from card_deck.field import Field

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (122, 122, 122)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

class Table:
    def __init__(self, screen_width, screen_height, player_id, x_limits, y_limits, font_size):
        self.fields = {
            'screen':     Field(0,           0,           screen_width,                 screen_height,                 WHITE, 'screen', font_size),
            'players':    Field(0,           0,           x_limits[0],                  y_limits[0],                   BLACK, 'players', font_size),
            'hand':       Field(0,           y_limits[1], x_limits[0],                  (screen_height - y_limits[1]), GREY, 'hand', font_size),
            'equipments': Field(0,           y_limits[0], x_limits[0],                  (y_limits[1] - y_limits[0]),   RED, 'equipments', font_size),
            'table':      Field(x_limits[0], 0,           (screen_width - x_limits[0]), y_limits[1],                   GREEN, 'table', font_size),
            'deck':       Field(x_limits[0], y_limits[1], (x_limits[1] - x_limits[0]),  (screen_height - y_limits[1]), BLUE, 'deck', font_size),
            'logs':       Field(x_limits[1], y_limits[1], (screen_width - x_limits[1]), (screen_height - y_limits[1]), PURPLE, 'logs', font_size)
        }
        self.player_id = player_id
        self.last_id = player_id

        self.fields['equipments'].set_name(f"{player_id}'s equips")
    
    def get_rect(self, field_name):
        return self.fields[field_name].get_rect()

    def draw(self, win):
        for field_name, field in self.fields.items():
            if not field_name == 'screen':
                field.draw(win)
    
    def get_rects(self):
        return self.fields

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
