import socket
from _thread import *
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

cards = {}
for i in range(280):
    cards[i] = {
            'x': 0.404,
            'y': 0.7575,
            'last_x': 0,
            'last_y': 0,
            'type': 'treasure',
            'order': 0,
            'last_order': 0,
            'face': False
    }
    if i >= 140:
        cards[i]['x'] = 0.504
        cards[i]['type'] = 'door'

clients = []
def threaded_client(conn, player):
    global clients

    # mandar um id ou nome do cliente aqui?
    conn.send(pickle.dumps(player))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print('recebido ' + str(data))
            with lock:
                for i, c in enumerate(clients):
                    # print('index ' + str(i))
                    # print(c)
                    c.sendall(pickle.dumps(data))
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