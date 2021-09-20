from card_deck.field import Field

SELECTED_COLOR = (255, 255, 255)
HOVERED_COLOR = (192, 192, 192)
DEFAULT_COLOR = (128, 128, 128)

class Players:
    def __init__(self, player_ids, players_w, players_h, font_size):
        self.players = {}
        self.players_w = players_w
        self.players_h = players_h
        self.hover = -1
        self.selected = -1
        self.font_size = font_size
        # CHAMAR UPDATE PLAYERS E DRAW/hover/click AO MESMO TEMPO DA ERRO!!! usar o msm lock usado no server
        self.update_players(player_ids)

    
    def update_players(self, player_ids):
        self.players = {}
        for i, p_id in enumerate(player_ids):
            start_x = (i % 2) * self.players_w
            start_y = (i // 2) * self.players_h
            self.players[p_id] = Field(start_x, start_y, self.players_w, self.players_h, DEFAULT_COLOR, str(p_id), self.font_size)

    def focused(self, pos, type):
        if type == 'select':
            if self.selected != -1:
                self.players[self.selected].color = DEFAULT_COLOR
                self.selected = -1
        if type == 'hover':
            if self.hover != -1 and self.hover != self.selected:
                self.players[self.hover].color = DEFAULT_COLOR
            self.hover = -1

        for p_id, player in self.players.items():
            if player.rect.collidepoint(pos):
                if type == 'select':
                        self.selected = p_id
                        self.hover = p_id
                        self.players[self.selected].color = SELECTED_COLOR 

                elif type == 'hover':
                    if self.selected == -1 or p_id != self.selected:
                        self.hover = p_id
                        self.players[self.hover].color = HOVERED_COLOR
                 
                return p_id
        return -1

    def draw(self, win, quantities):
        for p_id, player in self.players.items():
            text = player.name
            if p_id in quantities and 'hand' in quantities[p_id]:
                text = f"{text} - {quantities[p_id]['hand']}"
            else:
                text = f"{text} - 0"
            if p_id in quantities and 'equipments' in quantities[p_id]:
                text = f"{text} - {quantities[p_id]['equipments']}"
            else:
                text = f"{text} - 0"
            player.text = text # pode usar o metodo set name
            player.draw(win)

    def clear(self):
        if self.selected != -1:
            self.players[self.selected].color = DEFAULT_COLOR 
            self.selected = -1
        if self.hover != -1:
            self.players[self.hover].color = DEFAULT_COLOR 
            self.hover = -1
    
    def delete_player(self, player_ids, p_id):
        if self.selected == p_id:
            self.selected = -1
        if self.hover == p_id:
            self.hover = -1
        self.update_players(player_ids)
