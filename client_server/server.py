import socket
from _thread import *
import pickle
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

s.listen(3)
print("Waiting for a connection, Server Started")

# pesquisar threading lock
conn_lock = threading.Lock()
ids_lock = threading.Lock()
cards_lock = threading.Lock()

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
def threaded_client(conn):
    global cards
    bytes_message = b''
    buffersize = 1024
    footersize = 10 #endmessage
    # criar variavel footer com endmessage

    # pegar o nome na hr de iniciar o jogo, tratar aqui duplicados
    # if player == 0:
    #     player = 'moises'
    # elif player == 1:
    #     player = 'carol'
    # elif player == 2:
    #     player = 'zella'
    # elif player == 3:
    #     player = 'thiago'
    # elif player == 4:
    #     player = 'rafael'
    # elif player == 5:
    #     player = 'paulo'

    while bytes_message.find(b'endmessage') == -1:
        data = conn.recv(buffersize)
        bytes_message += data
    data = bytes_message[:bytes_message.find(b'endmessage')]
    player = pickle.loads(data)
    bytes_message = bytes_message[bytes_message.find(b'endmessage') + footersize:]
    
    if player in ids:
        count = 1
        while(player + str(count)) in ids:
            count += 1
        player = player + str(count)

    # mandar um id ou nome do cliente aqui?
    with ids_lock:
        with conn_lock:
            ids.append(player)
            conn.send(pickle.dumps({'player_id': player, 'players': ids}) + bytes(f'endmessage', "utf-8"))
    # with lock aqui
    with conn_lock:
        for c in clients:
            if c == conn:
                continue
            message = {'message_type': 'players_update', 'message': player}
            c.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))

    while True:
        try:
            # data = pickle.loads(conn.recv(2048))
            while bytes_message.find(b'endmessage') == -1:
                data = conn.recv(buffersize)
                bytes_message += data
            data = bytes_message[:bytes_message.find(b'endmessage')]
            data = pickle.loads(data)
            bytes_message = bytes_message[bytes_message.find(b'endmessage') + footersize:]
            # return pickle.loads(to_return)
            if data['message_type'] == 'init':
                # with lock
                with conn_lock:
                    with cards_lock:
                        conn.sendall(pickle.dumps(cards) + bytes(f'endmessage', "utf-8"))

            elif data['message_type'] == 'quit':
                with cards_lock:
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
            
            elif data['message_type'] == 'reset_game':
                with cards_lock:
                    # criar um metodo pra fazer isso tanto no init quanto aqui no reset
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
                with conn_lock:
                    for c in clients:
                        if c == conn:
                            continue
                        message = {'message_type': 'reset_game', 'message': data['message']}
                        c.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))
            
            elif data['message_type'] == 'dice_roll':
                with conn_lock:
                    for c in clients:
                        if c == conn:
                            continue
                        message = {'message_type': 'dice_roll', 'message': data['message']}
                        c.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))

            else:
                if data['message_type'] == 'card_update':
                    with cards_lock:
                        cards[data['message']['id']] = data['message']['data']
                # o trecho abaixo não tem que estar dentro do if acima? dar um tab nele
                with conn_lock:
                    for c in clients:
                        if c == conn:
                            continue
                        message = {'message_type': 'card_update', 'message': data['message']}
                        c.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    # passar pra dentro do with lock abaixo
    with ids_lock:
        ids.remove(player)
    with conn_lock: #lock precisa do global?
        clients.remove(conn)
        message = {'message_type': 'self_disconnected'}
        conn.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))
        for c in clients:
            message = {'message_type': 'player_disconnected', 'message': player}
            c.sendall(pickle.dumps(message) + bytes(f'endmessage', "utf-8"))
        
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    with conn_lock:
        clients.append(conn)
    start_new_thread(threaded_client, (conn,))