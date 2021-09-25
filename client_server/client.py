from network import Network
from card_deck.game import play
from card_deck.game import listen
from threading import Thread

def main():
    with open('client_server/conf.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        name = lines[0][:6].lower()
        ip = lines[1]
    network = Network(name, ip)
    #play(network)
    Thread(target = play, args=(network,)).start()
    Thread(target = listen, args=(network,)).start()

main()