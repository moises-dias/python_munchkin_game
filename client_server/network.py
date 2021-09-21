import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.72"
        # self.server = "192.168.1.23"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.bytes_message = b''
        self.buffersize = 1024
        self.footersize = 10 #endmessage
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            # return pickle.loads(self.client.recv(2048))
            return self.process()
        except Exception as e:
            print(e)

    def send(self, message):
        try:
            to_send = pickle.dumps(message) + bytes(f'endmessage', "utf-8")
            self.client.send(to_send)
        except Exception as e:
            print(e)

    def receive(self):
        # data = pickle.loads(self.client.recv(2048))
        # return data
        #talvez n precisa do if else, só chamar process direto
        if len(self.bytes_message) > 0:
            return self.process()
        else:
            self.bytes_message = self.client.recv(self.buffersize)
            return self.process()

    def get_all_cards(self):
        self.client.send(pickle.dumps({'message_type': 'init'}) + bytes(f'endmessage', "utf-8"))
        # cards_info = pickle.loads(self.client.recv(16384))

        # antes desses process perdidos limpar a bytes_message ?
        cards_info = self.process()
        return cards_info

    def get_player_id(self):
        return self.p['player_id']

    def get_player_list(self):
        return self.p['players']
    
    def process(self):    
        while self.bytes_message.find(b'endmessage') == -1:
            new_msg = self.client.recv(self.buffersize)
            self.bytes_message += new_msg
        to_return = self.bytes_message[:self.bytes_message.find(b'endmessage')]
        self.bytes_message = self.bytes_message[self.bytes_message.find(b'endmessage') + self.footersize:]
        return pickle.loads(to_return)
