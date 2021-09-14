from card_deck.field import Field

WHITE = (255, 255, 255)
GREY = (170, 170, 170)
DARKGREY = (85, 85, 85)
BLACK = (0, 0, 0)

# ISSO DEVE VIR NA INICIALIZAÇÃO DA CLASSE
# players_w = 0.4 / 2
# players_h = 0.25 / 5

class Players:
    def __init__(self, player_ids, screen_width, screen_height):
        self.players = {}
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.players_w = (0.4 / 2) * screen_width
        self.players_h = (0.25 / 5) * screen_height 
        # CHAMAR UPDATE PLAYERS E DRAW/hover/click AO MESMO TEMPO DA ERRO!!! usar o msm lock usado no server
        self.update_players(player_ids)

    
    def update_players(self, player_ids):
        for i, p_id in enumerate(player_ids):
            start_x = (i % 2) * self.players_w
            start_y = (i // 2) * self.players_h
            # print(self.screen_width, self.screen_height)
            print(p_id, start_x, start_y)
            self.players[p_id] = Field(start_x, start_y, self.players_w, self.players_h, DARKGREY, str(p_id))

        # self.fields = {
        #     'screen':     Field(0,                          0,                           screen_width,                               screen_height,                               WHITE, 'screen'),
        #     'players':    Field(0,                          0,                           x_limits[0] * screen_width,                 y_limits[0] * screen_height,                 RED, 'players'),
        #     'hand':       Field(0,                          y_limits[1] * screen_height, x_limits[0] * screen_width,                 (1 - y_limits[1]) * screen_height,           GREY, 'hand'),
        #     'equipments': Field(0,                          y_limits[0] * screen_height, x_limits[0] * screen_width,                 (y_limits[1] - y_limits[0]) * screen_height, BLACK, 'equipments'),
        #     'table':      Field(x_limits[0] * screen_width, 0,                           (1 - x_limits[0]) * screen_width,           y_limits[1] * screen_height,                 GREEN, 'table'),
        #     'deck':       Field(x_limits[0] * screen_width, y_limits[1] * screen_height, (x_limits[1] - x_limits[0]) * screen_width, (1 - y_limits[1]) * screen_height,           BLUE, 'deck'),
        #     'logs':       Field(x_limits[1] * screen_width, y_limits[1] * screen_height, (1 - x_limits[1]) * screen_width,           (1 - y_limits[1]) * screen_height,           PURPLE, 'logs')
        # }
    
    # def click(self, pos):
    #     return self.fields[field_name].get_rect()
    
    def focused(self, pos):
        for p_id, player in self.players.items():
            if player.rect.collidepoint(pos):
                return p_id
        return -1

    def draw(self, win):
        for p_id, player in self.players.items():
            # print(p_id, sep='')
            player.draw(win)
    
    # def get_rects(self):
    #     return self.fields
