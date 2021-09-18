import socket
from _thread import *
import pickle
import time
from datetime import datetime, timedelta
from random import randrange
import threading
import sys

server = "192.168.1.72"
# server = "192.168.1.23"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print("Waiting for a connection, Server Started")

lock = threading.Lock()

max_order = 0

cards = {}
for i in range(280):
    cards[i] = {
            'x': 0.404,
            'y': 0.7575,
            'p_id': -1,
            'draging': False,
            'order': 0,
            'face': False,
            'area': 'deck',
            'discarded': False
    }
    if i >= 140:
        cards[i]['x'] = 0.504

print('size', sys.getsizeof(cards))

clients = []
ids = []
def threaded_client(conn, player):
    # ver se precisa desses globals
    global clients
    global cards
    global ids
    global max_order

    #na hr de criar nome tirar esse codigo feio aqui
    # pegar o nome na hr de iniciar o jogo, tratar aqui duplicados
    if player == 0:
        player = 'moises'
    elif player == 1:
        player = 'carol'
    elif player == 2:
        player = 'zella'
    elif player == 3:
        player = 'thiago'
    elif player == 4:
        player = 'rafael'
    elif player == 5:
        player = 'paulo'


    # mandar um id ou nome do cliente aqui?
    ids.append(player)
    conn.send(pickle.dumps({'player_id': player, 'players': ids}))
    for i, c in enumerate(clients):
        if c == conn:
            continue
        message = {'message_type': 'players_update', 'message': player}
        c.sendall(pickle.dumps(message))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if data['message_type'] == 'init':
                print('size', sys.getsizeof(cards))
                conn.sendall(pickle.dumps(cards))

            elif data['message_type'] == 'quit':
                for c_id, card in cards.items():
                    if card['p_id'] == player and not card['discarded']:
                        card['x'] = 0.604
                        if c_id >= 140:
                            card['x'] = 0.704
                        card['y'] = 0.7575
                        card['draging'] = False
                        card['face'] = True
                        card['area'] = 'deck'
                        card['discarded'] = True
                break

            else:
                if data['message_type'] == 'card_update':
                    cards[data['message']['id']] = data['message']['data']
                with lock:
                    for i, c in enumerate(clients):
                        if c == conn:
                            continue
                        message = {'message_type': 'card_update', 'message': data['message']}
                        c.sendall(pickle.dumps(message))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    ids.remove(player)
    with lock: #precisa do global la em cima? testar isso num jupyter com dicionario e variaveis
        clients.remove(conn)
        for i, c in enumerate(clients):
            # if c == conn: #fazer depois de tirar o conn dai n precisa desse if
            #     continue
            message = {'message_type': 'player_disconnected', 'message': player}
            c.sendall(pickle.dumps(message))
        
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    with lock:
        clients.append(conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1