import pygame

class Card:
    def __init__(self, image, x, y, id, type, im_x, im_y, im_name):
        self.image = image
        self.x = x
        self.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.last_x = 0
        self.last_y = 0
        self.width = image.get_width()
        self.height = image.get_height()
        self.draging = False
        self.id = id
        self.type = type
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
        self.order = 0
        self.last_order = 0
        self.area = ''
        self.last_area = ''
        self.face = False
        self.name = ''
        self.im_x = im_x
        self.im_y = im_y
        self.im_name = im_name
        self.p_id = -1
        self.discarded = False
        self.last_discarded = False
        self.to_draw = False
        self.interact = False
        
    def reset(self, t_pos, d_pos):
        # colocar aqui tudo o que precisa setar pra resetar a carta
        pass

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
    
    def set_order(self, order):
        self.order = order

    def get_order(self):
        return self.order

    def get_face(self):
        return self.face

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_im_name(self):
        return self.im_name

    def get_im_x(self):
        return self.im_x

    def get_im_y(self):
        return self.im_y

    def get_draging(self):
        return self.draging

    def reveal(self, pos):
        if self.rect.collidepoint(pos) and self.order > 0:
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
            self.last_order = self.order
            self.draging = True
            self.offset_x = self.x - mouse_x
            self.offset_y = self.y - mouse_y
            self.last_area = self.area
            self.last_discarded = self.discarded
            self.discarded = False
            return True
        else:
            self.draging = False #ISSO VAI DAR PROBLEMA QND FOR PRA ONLINE
            return False
    
    def focused(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def try_discard(self, pos, t_discard_pos, d_discard_pos):
        if self.rect.collidepoint(pos):
            if self.type == 'treasure':
                self.x = self.rect.x = t_discard_pos[0]
                self.y = self.rect.y = t_discard_pos[1]
            if self.type == 'door':
                self.x = self.rect.x = d_discard_pos[0]
                self.y = self.rect.y = d_discard_pos[1]
            # self.order = 0
            self.discarded = True
            self.face = True
            self.area = 'deck'
            return True
        return False
    
    def discard(self, t_discard_pos, d_discard_pos):
        self.discarded = True
        self.face = True
        self.area = 'deck'
        self.draging = False
        self.to_draw = True
        self.interact = True
        if self.type == 'treasure':
            self.x = self.rect.x = t_discard_pos[0]
            self.y = self.rect.y = t_discard_pos[1]
        else:
            self.x = self.rect.x = d_discard_pos[0]
            self.y = self.rect.y = d_discard_pos[1]
    
    def release(self, pos, rect_equipments, rect_table, rect_hand):
        # if self.draging: #redundante, ja ta sendo checado ao chamar o release
        if not(self.rect.collidepoint(pos) and any([rect.collidepoint(pos) for rect in [rect_equipments, rect_table, rect_hand]])):
            self.x = self.rect.x = self.last_x
            self.y = self.rect.y = self.last_y
            if self.last_order == 0:
                self.order = 0
            self.area = self.last_area
            self.draging = False
            if self.last_discarded:
                self.discarded = True
                self.face = True
                self.area = 'deck' # setando last area acima n é suficiente?
            return False
        else:
            for rect in [rect_equipments, rect_table, rect_hand]:
                if (rect.collidepoint(pos) and self.rect.colliderect(rect) and not rect.contains(self.rect)):
                    # print(rect.top, rect.left, rect.bottom, rect.right)
                    if self.x < rect.right < self.x + self.width: #right collision
                        self.x = self.rect.x = self.x - (self.x + self.width - rect.right)
                    if self.x < rect.left < self.x + self.width: #left collision
                        self.x = self.rect.x = rect.left
                    if self.y < rect.top < self.y + self.height: #top collision
                        self.y = self.rect.y = rect.top
                    if self.y < rect.bottom < self.y + self.height: #bottom collision
                        self.y = self.rect.y = self.y - (self.y + self.height - rect.bottom)
        self.draging = False
        return True

    def move(self, pos, rect_screen):
        if self.draging:
            mouse_x = pos[0]
            mouse_y = pos[1]

            prev_x = self.x
            prev_y = self.y

            self.x = self.rect.x = mouse_x + self.offset_x
            if(not(rect_screen.contains(self.rect))):
                self.x = self.rect.x = prev_x

            self.y = self.rect.y = mouse_y + self.offset_y
            if(not(rect_screen.contains(self.rect))):
                self.y = self.rect.y = prev_y
            
            return True
        return False
    
    def get_info(self, screen_width, screen_height):
        return {
            'id': self.id, 
            'data': {
                'x': self.x / screen_width,
                'y': self.y / screen_height,
                'p_id': self.p_id,
                'draging': self.draging,
                'order': self.order,
                'face': self.face,
                'area': self.area,
                'discarded': self.discarded
            }
        }
    
    def set_info(self, card_info, screen_width, screen_height):
        card_info['x'] = card_info['x'] * screen_width
        card_info['y'] = card_info['y'] * screen_height
        for attr, value in card_info.items():
            # recebe um dicionario onde as chaves necessáriamente devem ser atributos da classe card
            setattr(self, attr, value)
            if attr == 'x':
                self.rect.x = value
            if attr == 'y':
                self.rect.y = value
