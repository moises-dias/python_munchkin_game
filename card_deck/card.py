import pygame

class Card:
    def __init__(self, image, x, y, w, h, id, type):
        self.image = image
        self.x = x
        self.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.last_x = 0
        self.last_y = 0
        self.width = w
        self.height = h
        self.draging = False
        self.id = id
        self.type = type
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
        self.order = 0
        self.area = ''
        self.face = False
        self.name = ''
        

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
    
    def set_order(self, order):
        self.order = order

    def get_order(self):
        return self.order

    def set_face(self, face):
        self.face = face

    def get_face(self):
        return self.face

    def get_type(self):
        return self.type

    def reveal(self, pos):
        if self.rect.collidepoint(pos):
            self.face = not self.face
            print(self.face)
            return True
        return False


    def click(self, pos):
        if self.rect.collidepoint(pos):
            mouse_x = pos[0]
            mouse_y = pos[1]
            self.last_x = self.x
            self.last_y = self.y
            self.draging = True
            self.offset_x = self.x - mouse_x
            self.offset_y = self.y - mouse_y
            return True
        else:
            self.draging = False
            return False
    
    def focused(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def discard(self, pos, t_discard_pos, d_discard_pos):
        if self.rect.collidepoint(pos):
            if self.type == 'treasure':
                self.x = t_discard_pos[0]
                self.rect.x = t_discard_pos[0]
                self.y = t_discard_pos[1]
                self.rect.y = t_discard_pos[1]
            if self.type == 'door':
                self.x = d_discard_pos[0]
                self.rect.x = d_discard_pos[0]
                self.y = d_discard_pos[1]
                self.rect.y = d_discard_pos[1]
            self.order = 0
            self.face = True
            return True
        return False
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        if self.draging:
            if not(self.rect.collidepoint(pos) and any([rect.collidepoint(pos) for rect in [rect_equipments, rect_table, rect_hand]])):
                self.x = self.last_x
                self.rect.x = self.last_x
                self.y = self.last_y
                self.rect.y = self.last_y
                self.draging = False
                return False
            else:
                for rect in [rect_equipments, rect_table, rect_hand]:
                    if (rect.collidepoint(pos) and self.rect.colliderect(rect) and not rect.contains(self.rect)):
                        print(rect.top, rect.left, rect.bottom, rect.right)
                        if self.x < rect.right < self.x + self.width: #right collision
                            self.x = self.x - (self.x + self.width - rect.right)
                            self.rect.x = self.x - (self.x + self.width - rect.right)
                        if self.x < rect.left < self.x + self.width: #left collision
                            self.x = rect.left
                            self.rect.x = rect.left
                        if self.y < rect.top < self.y + self.height: #top collision
                            self.y = rect.top
                            self.rect.y = rect.top
                        if self.y < rect.bottom < self.y + self.height: #bottom collision
                            self.y = self.y - (self.y + self.height - rect.bottom)
                            self.rect.y = self.y - (self.y + self.height - rect.bottom)
            self.draging = False
            return True

    def move(self, pos, rect_screen, rect_players, rect_logs, rect_deck):
        if self.draging:
            mouse_x = pos[0]
            mouse_y = pos[1]

            prev_x = self.x
            prev_y = self.y

            self.x = mouse_x + self.offset_x
            self.rect.x = mouse_x + self.offset_x
            if(not(rect_screen.contains(self.rect)) ): #or not any([self.rect.colliderect(rect) for rect in [rect_equipments, rect_table, rect_hand]])):
                self.x = prev_x
                self.rect.x = prev_x

            self.y = mouse_y + self.offset_y
            self.rect.y = mouse_y + self.offset_y

            if(not(rect_screen.contains(self.rect)) ):# or not any([self.rect.colliderect(rect) for rect in [rect_equipments, rect_table, rect_hand]])):
                self.y = prev_y
                self.rect.y = prev_y

    def position(self): # trocar para tupla?
        return [self.x, self.y, self.width, self.height]