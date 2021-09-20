import pygame

class Field:
    def __init__(self, x, y, w, h, color, name, font_size):
        self.x = x
        self.y = y
        self.color = color
        self.width = w
        self.height = h
        self.rect = pygame.rect.Rect((x, y, w, h))
        self.name = name
        self.font = pygame.font.SysFont("comicsans", font_size) #font e text pode ser criado uma vez só, deixar na inicialização
        self.text = self.name

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        text_to_draw = self.font.render(self.text, 1, (0, 0, 0))
        win.blit(text_to_draw, (self.x, self.y))
    
    def get_rect(self):
        return self.rect
    
    def set_name(self, name):
        self.text = name
        # self.text = self.font.render(self.name, 1, (255,255,255))
