import socket
from _thread import *
from player import Player
import pickle
import time
from datetime import datetime, timedelta
from random import randrange
server = "192.168.1.72"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

clients = []
players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[0]))
    cards = {
        'a': {'data': 'foo'},
        'b': {'data': 'foo'},
        'c': {'data': 'foo'}
    }
    # to_update = {
    #     'a': datetime.now() - timedelta(minutes=1),
    #     'b': datetime.now() - timedelta(minutes=1),
    #     'c': datetime.now() - timedelta(minutes=1)
    # }
    to_update = {}
    reply = ""
    count = 0
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print('recebido ' + data)
            for c in data:
                to_update[c] = datetime.now()
            
            to_update = {k:v for (k,v) in to_update.items() if (datetime.now() - v).seconds == 0}

            cards = {k:{'data': randrange(100)} for (k,v) in cards.items()}

            # players[player] = data

            # if not data:
            #     print("Disconnected")
            #     break
            # else:
            #     if player == 1:
            #         reply = players[0]
            #     else:
            #         reply = players[1]

            #     print("Received: ", data)
            #     print("Sending : ", reply)
            # time.sleep(0.2)
            count = count + 1
            print(count)
            # conn.sendall(pickle.dumps({k:v for (k,v) in cards.items() if k in to_update.keys()}))

            for c in clients:
                c.sendall(pickle.dumps({k:v for (k,v) in cards.items() if k in to_update.keys()}))
            # ready = select.select([conn], [], [], 0)
            # print(ready)
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    clients.append(conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1