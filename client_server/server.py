import socket
from _thread import *
from player import Player
import pickle
import time
from datetime import datetime, timedelta
from random import randrange
import threading
server = "192.168.1.72"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print("Waiting for a connection, Server Started")

lock = threading.Lock()

clients = []
players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
cards = {
    'a': {'data': 'foo'},
    'b': {'data': 'foo'},
    'c': {'data': 'foo'}
}
cards = {k:{'data': randrange(100)} for (k,v) in cards.items()}
count = 0
def threaded_client(conn, player):
    global cards
    global count
    global clients
    conn.send(pickle.dumps(players[0]))

    # to_update = {
    #     'a': datetime.now() - timedelta(minutes=1),
    #     'b': datetime.now() - timedelta(minutes=1),
    #     'c': datetime.now() - timedelta(minutes=1)
    # }
    to_update = {}
    reply = ""
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print('recebido ' + str(data))
            # for c in data:
            #     to_update[c] = datetime.now()
            
            # to_update = {k:v for (k,v) in to_update.items() if (datetime.now() - v).seconds == 0}

            # cards = {k:{'data': randrange(100)} for (k,v) in cards.items()}

            # # time.sleep(0.2)
            # count = count + 1
            # print(count)
            # # conn.sendall(pickle.dumps({k:v for (k,v) in cards.items() if k in to_update.keys()}))
            with lock:
                for i, c in enumerate(clients):
                    # print('index ' + str(i))
                    # print(c)
                    c.sendall(pickle.dumps(data))
            # ready = select.select([conn], [], [], 0)
            # print(ready)
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    with lock:
        clients.append(conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1