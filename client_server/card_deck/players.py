from card_deck.field import Field

WHITE = (255, 255, 255)
GREY = (170, 170, 170)
DARKGREY = (85, 85, 85)
BLACK = (0, 0, 0)

# ISSO DEVE VIR NA INICIALIZAÇÃO DA CLASSE
players_w = 0.4 / 2
players_h = 0.25 / 5

class Players:
    def __init__(self, player_ids):
        self.players = {}
        self.update_players(player_ids)

    
    def update_players(self, player_ids):
        for i, p_id in enumerate(player_ids):
            start_x = i // 2
            start_y = i % 2
            self.players[p_id] = Field(start_x, start_y, players_w, players_h, DARKGREY, str(p_id))

        # self.fields = {
        #     'screen':     Field(0,                          0,                           screen_width,                               screen_height,                               WHITE, 'screen'),
        #     'players':    Field(0,                          0,                           x_limits[0] * screen_width,                 y_limits[0] * screen_height,                 RED, 'players'),
        #     'hand':       Field(0,                          y_limits[1] * screen_height, x_limits[0] * screen_width,                 (1 - y_limits[1]) * screen_height,           GREY, 'hand'),
        #     'equipments': Field(0,                          y_limits[0] * screen_height, x_limits[0] * screen_width,                 (y_limits[1] - y_limits[0]) * screen_height, BLACK, 'equipments'),
        #     'table':      Field(x_limits[0] * screen_width, 0,                           (1 - x_limits[0]) * screen_width,           y_limits[1] * screen_height,                 GREEN, 'table'),
        #     'deck':       Field(x_limits[0] * screen_width, y_limits[1] * screen_height, (x_limits[1] - x_limits[0]) * screen_width, (1 - y_limits[1]) * screen_height,           BLUE, 'deck'),
        #     'logs':       Field(x_limits[1] * screen_width, y_limits[1] * screen_height, (1 - x_limits[1]) * screen_width,           (1 - y_limits[1]) * screen_height,           PURPLE, 'logs')
        # }
    
    # def get_rect(self, field_name):
    #     return self.fields[field_name].get_rect()

    def draw(self, win):
        for p_id, player in self.players.items():
            player.draw(win)
    
    # def get_rects(self):
    #     return self.fields
