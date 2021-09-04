import pygame
from card import Card

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tracking System")
clock = pygame.time.Clock()
running = True

im_x = 0
im_y = 0
im_w = 500
im_h = 809

my_image = pygame.image.load("workspace/teste2.jpeg")

screen_size = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
players_size = (int(0.9*SCREEN_WIDTH), int(0.9*SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)
logs_size = (int(0.9*SCREEN_WIDTH), int(0.9*SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT) 
deck_size = (int(0.9*SCREEN_WIDTH), int(0.9*SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)

cards = []

cards.append(Card(pygame.transform.scale(my_image.subsurface((0, 0, im_w, im_h)), (250, 404)), 0, 0, 250, 404))
cards.append(Card(pygame.transform.scale(my_image.subsurface((0, im_h, im_w, im_h)), (250, 404)), 100, 0, 250, 404))
cards.append(Card(pygame.transform.scale(my_image.subsurface((im_w, 0, im_w, im_h)), (250, 404)), 0, 100, 250, 404))
cards.append(Card(pygame.transform.scale(my_image.subsurface((im_w, im_h, im_w, im_h)), (250, 404)), 100, 100, 250, 404))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:     
                for card in cards:     
                    card.click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                for card in cards:
                    card.release()       

        elif event.type == pygame.MOUSEMOTION:
            for card in cards:
                card.move(event.pos, screen_size, players_size, logs_size, deck_size)
    
    screen.fill(WHITE)
    for card in cards:
        card.draw(screen)
    #screen.blit(my_image, (im_x, im_y), (0, 0, im_w, im_h))

    #test = my_image.subsurface((0, 0, im_w, im_h))
    #test = pygame.transform.scale(test, (250, 404))
    #screen.blit(test, (0,0))

    #foo = pygame.transform.scale(my_image.subsurface((0, 0, im_w, im_h)), (250, 404))
    
    #for i in range(100):
    #    screen.blit(test, (randrange(100), randrange(100)))
    
    pygame.draw.rect(screen, (255,   0,   0), pygame.rect.Rect((700, 50, 200, 200)))
    pygame.draw.rect(screen, (255,   0,   0), pygame.rect.Rect(50, 700, 200, 200))
    pygame.draw.rect(screen, (255,   0,   0), pygame.rect.Rect(700, 700, 200, 200))
    pygame.display.flip()
    clock.tick(FPS)
    # print(pygame.mouse.get_focused())
    if not (pygame.mouse.get_focused()): # trocar para mouse.x e y > 1000 ou < 0?
        for card in cards:
            card.release()

pygame.quit()