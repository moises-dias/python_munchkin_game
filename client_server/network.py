import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.72"
        # self.server = "192.168.1.23"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)

    def send(self, message):
        try:
            self.client.send(pickle.dumps(message))
        except Exception as e:
            print(e)

    def receive(self):
        data = pickle.loads(self.client.recv(2048))
        return data

    def get_all_cards(self):
        self.client.send(pickle.dumps({'message_type': 'init'}))
        cards_info = pickle.loads(self.client.recv(16384))
        return cards_info

    def get_player_id(self):
        return self.p['player_id']

    def get_player_list(self):
        return self.p['players']
