
class DefaultCard:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
    
        
    def draw_at(self, win, pos):
        win.blit(self.image, (pos[0], pos[1]))

    def set_x_y(self, x, y):
        self.x = x
        self.y = y
