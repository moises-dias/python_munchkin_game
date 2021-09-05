import pygame
from card import Card

treasure_1_w = 245
treasure_1_h = 351
treasure_1 = pygame.image.load("card_deck/images/treasure1.jpeg")

treasure_2_w = 500
treasure_2_h = 809
treasure_2 = pygame.image.load("card_deck/images/treasure2.jpeg")

door_1_w = 378
door_1_h = 585
door_1 = pygame.image.load("card_deck/images/door1.jpg")

door_2_w = 245
door_2_h = 351
door_2 = pygame.image.load("card_deck/images/door2.jpeg")


class Cards:
    def __init__(self):
        self.cards = []
        self.door_back = None
        self.treasure_back = None

        #colocar id nas cartas
        for i in range(70):
            self.cards.append(Card(pygame.transform.smoothscale(treasure_1.subsurface((i%10 * treasure_1_w, i//10 * treasure_1_h, treasure_1_w, treasure_1_h)), (137, 222)), 40 * i, 0, 137, 222, i))
            self.cards.append(Card(pygame.transform.smoothscale(treasure_2.subsurface((i%10 * treasure_2_w, i//10 * treasure_2_h, treasure_2_w, treasure_2_h)), (137, 222)), 40 * i, 280, 137, 222, 70 + i))
            self.cards.append(Card(pygame.transform.smoothscale(door_1.subsurface((i%10 * door_1_w, i//10 * door_1_h, door_1_w, door_1_h)), (137, 222)), 40 * i, 560, 137, 222, 140 + i))
            self.cards.append(Card(pygame.transform.smoothscale(door_2.subsurface((i%10 * door_2_w, i//10 * door_2_h, door_2_w, door_2_h)), (137, 222)), 40 * i, 800, 137, 222, 210 + i))
    
    def draw(self, win):
        for card in self.cards:
            win.blit(card.image, (card.x, card.y))