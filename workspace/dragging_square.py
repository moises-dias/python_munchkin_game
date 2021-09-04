import pygame

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 410

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 30

# --- classses --- (CamelCase names)

# empty

# --- functions --- (lower_case names)

# empty

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("Tracking System")

# - objects -

rectangle = pygame.rect.Rect(176, 134, 17, 17)
rectangle_draging = False

# - mainloop -

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, rectangle)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()