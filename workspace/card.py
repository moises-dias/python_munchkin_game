#server só retorna novas coordenadas se tiver alterações, senao retorna um false só
import pygame

class Card:
    def __init__(self, image, x, y, w, h):
        self.image = image
        self.x = x
        self.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.width = w
        self.height = h
        self.draging = False
        self.name = ''
        self.type = ''

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def click(self, pos):
        mouse_x = pos[0]
        mouse_y = pos[1]
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            self.draging = True
            self.offset_x = self.x - mouse_x
            self.offset_y = self.y - mouse_y
        else:
            self.draging = False
    
    def release(self):
        self.draging = False

    def move(self, pos, screen_size, players_size, logs_size, deck_size):
        if self.draging:
            mouse_x = pos[0]
            mouse_y = pos[1]
            if 0 <= mouse_x + self.offset_x and mouse_x + self.offset_x + self.width <= screen_size[3]:
                self.x = mouse_x + self.offset_x
            else:
                self.offset_x = self.x - mouse_x
            if 0 <= mouse_y + self.offset_y and mouse_y + self.offset_y + self.height <= screen_size[2]:
                self.y = mouse_y + self.offset_y
            else:
                self.offset_y = self.y - mouse_y

    def position(self):
        return [self.x, self.y, self.width, self.height]