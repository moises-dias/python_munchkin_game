from card_deck.field import Field

WINNER_COLOR = (60, 218, 37)
LOSER_COLOR = (242, 36, 13)
DEFAULT_COLOR = (100, 112, 100)

class Scores:
    def __init__(self, table_start_x, screen_width, screen_height, font_size):
        table_center_x = (screen_width + table_start_x) / 2
        delta = 0.01*screen_width
        field_w = 0.13*screen_width
        field_h = 0.06*screen_height
        self.scores = {
            'player': Field(table_center_x + delta, 0.01*screen_height, field_w, field_h, DEFAULT_COLOR, 'player: 0', font_size),
            'monster': Field(table_center_x - field_w - delta, 0.01*screen_height, field_w, field_h, DEFAULT_COLOR, 'monster: 0', font_size)
        }

    def draw(self, win):
        for id, field in self.scores.items():
            field.draw(win)
    
    def collidepoint(self, pos):
        return self.scores['player'].rect.collidepoint(pos) or self.scores['monster'].rect.collidepoint(pos)
    
    def backspace(self, pos):
        for id, field in self.scores.items():
            if field.rect.collidepoint(pos):
                if len(field.text.split(' ')[1]) == 1 and field.text.split(' ')[1] != '0': #se tiver um digito só o poder do monstro/jogador
                    field.text = field.text[:-1] + '0'
                    self.update_colors()
                    return {'type': field.text.split(' ')[0][:-1], 'value': field.text.split(' ')[1]}
                elif len(field.text.split(' ')[1]) == 2: #se tiver dois digitos o poder do monstro/jogador
                    field.text = field.text[:-1]
                    self.update_colors()
                    return {'type': field.text.split(' ')[0][:-1], 'value': field.text.split(' ')[1]}
    
    def add_number(self, pos, number):
        for id, field in self.scores.items():
            if field.rect.collidepoint(pos):
                if len(field.text.split(' ')[1]) == 1: #se tiver um digito só o poder do monstro/jogador
                    if field.text[-1] == '0':
                        field.text = field.text[:-1] + number
                    else:
                        field.text = field.text + number
                    self.update_colors()
                    return {'type': field.text.split(' ')[0][:-1], 'value': field.text.split(' ')[1]}
    
    def set_number(self, type, number):
        self.scores[type].text = self.scores[type].text.split(' ')[0] + f' {number}'
        self.update_colors()
    
    def update_colors(self):
        player_power = int(self.scores['player'].text.split(' ')[1])
        monster_power = int(self.scores['monster'].text.split(' ')[1])
        if player_power == 0 and monster_power == 0:
            self.scores['player'].color = DEFAULT_COLOR
            self.scores['monster'].color = DEFAULT_COLOR
        elif player_power > monster_power:
            self.scores['player'].color = WINNER_COLOR
            self.scores['monster'].color = LOSER_COLOR
        else:
            self.scores['player'].color = LOSER_COLOR
            self.scores['monster'].color = WINNER_COLOR
