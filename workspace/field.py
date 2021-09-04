import pygame

class Field:
    def __init__(self, x, y, w, h, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.width = w
        self.height = h
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.name, 1, (255,255,255))
        win.blit(text, (self.x, self.y))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
    
    def position(self):
        return (self.x, self.y, self.width, self.height)