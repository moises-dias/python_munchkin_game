import pygame
from network import Network
from card_deck.game import play
# play()

# width = 500
# height = 500
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Client")


def main():
    network = Network()
    play(network)
    # run = True
    # clock = pygame.time.Clock()

    # while run:
        # clock.tick(60)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()
        #     if event.type == pygame.KEYDOWN:
        #         n.send()
        # n.receive()

main()