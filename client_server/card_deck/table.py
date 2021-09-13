from card_deck.field import Field

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (122, 122, 122)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

x_limits = [0.4, 0.8]
y_limits = [0.25, 0.75]

class Table:
    def __init__(self, screen_width, screen_height):
        self.fields = {
            'screen':     Field(0,                          0,                           screen_width,                               screen_height,                               WHITE, 'screen'),
            'players':    Field(0,                          0,                           x_limits[0] * screen_width,                 y_limits[0] * screen_height,                 BLACK, 'players'),
            'hand':       Field(0,                          y_limits[1] * screen_height, x_limits[0] * screen_width,                 (1 - y_limits[1]) * screen_height,           GREY, 'hand'),
            'equipments': Field(0,                          y_limits[0] * screen_height, x_limits[0] * screen_width,                 (y_limits[1] - y_limits[0]) * screen_height, RED, 'equipments'),
            'table':      Field(x_limits[0] * screen_width, 0,                           (1 - x_limits[0]) * screen_width,           y_limits[1] * screen_height,                 GREEN, 'table'),
            'deck':       Field(x_limits[0] * screen_width, y_limits[1] * screen_height, (x_limits[1] - x_limits[0]) * screen_width, (1 - y_limits[1]) * screen_height,           BLUE, 'deck'),
            'logs':       Field(x_limits[1] * screen_width, y_limits[1] * screen_height, (1 - x_limits[1]) * screen_width,           (1 - y_limits[1]) * screen_height,           PURPLE, 'logs')
        }
    
    def get_rect(self, field_name):
        return self.fields[field_name].get_rect()

    def draw(self, win):
        for field_name, field in self.fields.items():
            if not field_name == 'screen':
                field.draw(win)
    
    def get_rects(self):
        return self.fields
