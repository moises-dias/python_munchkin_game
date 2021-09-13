import pygame

class Field:
    def __init__(self, x, y, w, h, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.width = w
        self.height = h
        self.rect = pygame.rect.Rect((x, y, w, h))
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40) #font e text pode ser criado uma vez só, deixar na inicialização
        text = font.render(self.name, 1, (255,255,255))
        win.blit(text, (self.x, self.y))
    
    def get_rect(self):
        return self.rect
