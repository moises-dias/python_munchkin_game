import socket
import pickle

class Network:
    def __init__(self, player_name, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 3389
        # self.server = "192.168.1.72"
        # self.port = 5555
        self.addr = (self.server, self.port)
        self.bytes_message = b''
        self.buffersize = 1024
        self.footersize = 10 #endmessage
        self.p = self.connect(player_name)

    def connect(self, player_name):
        try:
            self.client.connect(self.addr)
            self.send(player_name)
            # return pickle.loads(self.client.recv(2048))
            return self.process()
        except Exception as e:
            print('NETWORK 1', e)
            self.send({'message_type': 'quit'})
            raise e

    def send(self, message):
        try:
            to_send = pickle.dumps(message) + bytes(f'endmessage', "utf-8")
            self.client.send(to_send)
        except Exception as e:
            print('NETWORK 2', e)
            self.send({'message_type': 'quit'})

    def receive(self):
        # data = pickle.loads(self.client.recv(2048))
        # return data
        #talvez n precisa do if else, só chamar process direto
        if len(self.bytes_message) > 0:
            return self.process()
        else:
            try:
                self.bytes_message = self.client.recv(self.buffersize)
            except Exception as e:
                print('NETWORK 3', e)
                self.send({'message_type': 'quit'})
            return self.process()

    def get_all_cards(self):
        try:
            self.client.send(pickle.dumps({'message_type': 'init'}) + bytes(f'endmessage', "utf-8"))
        except Exception as e:
            print('NETWORK 4', e)
            self.send({'message_type': 'quit'})

        # antes desses process perdidos limpar a bytes_message ?
        cards_info = self.process()
        return cards_info

    def get_player_id(self):
        return self.p['player_id']

    def get_player_list(self):
        return self.p['players']
    
    def get_player_levels(self):
        return self.p['levels']
    
    def process(self):    
        while self.bytes_message.find(b'endmessage') == -1:
            try:
                new_msg = self.client.recv(self.buffersize)
            except Exception as e:
                print('NETWORK 5', e)
            self.bytes_message += new_msg
        to_return = self.bytes_message[:self.bytes_message.find(b'endmessage')]
        self.bytes_message = self.bytes_message[self.bytes_message.find(b'endmessage') + self.footersize:]
        return pickle.loads(to_return)
