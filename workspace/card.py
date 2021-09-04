#server só retorna novas coordenadas se tiver alterações, senao retorna um false só
import pygame

# w_start = 0
# h_start = 1
# w_end = 2
# h_end = 3

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
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            mouse_x = pos[0]
            mouse_y = pos[1]
            self.draging = True
            self.offset_x = self.x - mouse_x
            self.offset_y = self.y - mouse_y
        else:
            self.draging = False
    
    def release(self):
        self.draging = False

    def move(self, pos, rect_screen, rect_players, rect_logs, rect_deck):
        if self.draging:
            mouse_x = pos[0]
            mouse_y = pos[1]

            prev_x = self.x
            prev_y = self.y

            self.x = mouse_x + self.offset_x
            self.rect.x = mouse_x + self.offset_x
            if(not(rect_screen.contains(self.rect)) or any([self.rect.colliderect(rect) for rect in [rect_players, rect_logs, rect_deck]])):
                self.x = prev_x
                self.rect.x = prev_x

            self.y = mouse_y + self.offset_y
            self.rect.y = mouse_y + self.offset_y

            if(not(rect_screen.contains(self.rect)) or any([self.rect.colliderect(rect) for rect in [rect_players, rect_logs, rect_deck]])):
                self.y = prev_y
                self.rect.y = prev_y

    def position(self): # trocar para tupla?
        return [self.x, self.y, self.width, self.height]