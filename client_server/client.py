from network import Network
from card_deck.game import play
from card_deck.game import listen
from threading import Thread

def main():
    network = Network()
    #play(network)
    Thread(target = play, args=(network,)).start()
    Thread(target = listen, args=(network,)).start()

main()