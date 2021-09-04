#server só retorna novas coordenadas se tiver alterações, senao retorna um false só
import pygame

w_start = 0
h_start = 1
w_end = 2
h_end = 3

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
            if screen_size[w_start] <= mouse_x + self.offset_x and mouse_x + self.offset_x + self.width <= screen_size[w_end]:
                self.x = mouse_x + self.offset_x
            else:
                self.offset_x = self.x - mouse_x
            if screen_size[h_start] <= mouse_y + self.offset_y and mouse_y + self.offset_y + self.height <= screen_size[h_end]:
                self.y = mouse_y + self.offset_y
            else:
                self.offset_y = self.y - mouse_y

    def position(self): # trocar para tupla?
        return [self.x, self.y, self.width, self.height]