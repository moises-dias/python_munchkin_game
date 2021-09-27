from network import Network
from card_deck.game import play
from card_deck.game import listen
from threading import Thread
import re

def main():
    with open('client/conf.txt', encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
        name = lines[0]
        name = re.sub('[^A-Za-z]+', '', name)
        name = name.lower()
        name = name[:6]
        ip = lines[1]
        port = int(lines[2])
    network = Network(name, ip, port)
    #play(network)
    Thread(target = play, args=(network,)).start()
    Thread(target = listen, args=(network,)).start()

main()