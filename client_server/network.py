import socket
import pickle
import select
from random import randrange

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.72"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            # return pickle.loads(self.client.recv(2048))
            return 0
        except Exception as e:
            print(e)

    def send(self, message):
        try:
            # number = randrange(30)
            # print('sending ' + str(number))
            self.client.send(pickle.dumps(message))
        except Exception as e:
            print(e)
    def receive(self):
        ready = select.select([self.client], [], [], 0)
        if ready[0]:
            # print('receiving...')
            # tamanho para a primeira consulta do status das cartas
            data = pickle.loads(self.client.recv(2048))
            # print(f"receiving {len(data)}")
            return data
        else:
            # print('no data')
            return None
    def get_all_cards(self):
        self.client.send(pickle.dumps(['iniciar']))
        cards_info = pickle.loads(self.client.recv(16384))
        return cards_info
    
    def move(self, info):
        try:
            self.client.send(pickle.dumps(['move', info]))
        except Exception as e:
            print(e)