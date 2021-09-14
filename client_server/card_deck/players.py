from card_deck.field import Field

WHITE = (255, 255, 255)
GREY = (191, 191, 191)
MEDIUMGREY = (128, 128, 128)
DARKGREY = (64, 64, 64)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)

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
        self.hover = -1
        self.selected = -1
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
    
    def focused(self, pos, type):
        if type == 'select':
            if self.selected != -1:
                self.players[self.selected].color = DARKGREY
                self.selected = -1
        if type == 'hover':
            if self.hover != -1 and self.hover != self.selected:
                self.players[self.hover].color = DARKGREY
            self.hover = -1
        for p_id, player in self.players.items():
            if player.rect.collidepoint(pos):
                if type == 'select':
                        self.selected = p_id
                        self.hover = p_id
                        self.players[self.selected].color = GREY 

                elif type == 'hover':
                    print(self.selected, self.hover)
                    if self.selected == -1 or p_id != self.selected:
                        self.hover = p_id
                        self.players[self.hover].color = MEDIUMGREY
                 
                return p_id
            
        # self.players[self.hover].color = DARKGREY
        # self.players[self.selected].color = DARKGREY
        return -1

    def draw(self, win):
        for p_id, player in self.players.items():
            # print(p_id, sep='')
            player.draw(win)

    def clear(self):
        if self.selected != -1:
            self.players[self.selected].color = DARKGREY 
            self.selected = -1
        if self.hover != -1:
            self.players[self.hover].color = DARKGREY 
            self.hover = -1
    
    # def get_rects(self):
    #     return self.fields
