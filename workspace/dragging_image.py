import pygame
#from random import randrange
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 60
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tracking System")
image_draging = False
clock = pygame.time.Clock()
running = True
my_image = pygame.image.load("workspace/teste2.jpeg")

im_x = 0
im_y = 0
im_w = 500
im_h = 809

def collide(im_x, im_y, im_w, im_h, mouse_x, mouse_y):
    if im_x <= mouse_x <= im_x + im_w and im_y <= mouse_y <= im_y + im_h:
        return True
    return False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   
                mouse_x, mouse_y = event.pos         
                if collide(im_x, im_y, im_w, im_h, mouse_x, mouse_y):
                    image_draging = True
                    offset_x = im_x - mouse_x
                    offset_y = im_y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                image_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if image_draging:
                mouse_x, mouse_y = event.pos
                # print(mouse_x + offset_x)
                if 0 <= mouse_x + offset_x and mouse_x + offset_x + im_w <= SCREEN_WIDTH:
                    im_x = mouse_x + offset_x
                else:
                    offset_x = im_x - mouse_x
                if 0 <= mouse_y + offset_y and mouse_y + offset_y + im_h <= SCREEN_HEIGHT:
                    im_y = mouse_y + offset_y
                else:
                    offset_y = im_y - mouse_y

    screen.fill(WHITE)
    screen.blit(my_image, (im_x, im_y), (0, 0, im_w, im_h))

    test = my_image.subsurface((0, 0, im_w, im_h))
    test = pygame.transform.scale(test, (250, 404))
    screen.blit(test, (0,0))
    #for i in range(100):
    #    screen.blit(test, (randrange(100), randrange(100)))
    pygame.display.flip()
    clock.tick(FPS)
    # print(pygame.mouse.get_focused())
    if not (pygame.mouse.get_focused() and image_draging):
        image_draging = False

pygame.quit()