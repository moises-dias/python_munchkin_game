import socket
import pickle
import select
from random import randrange
letters = ['a', 'b', 'c']

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.72"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            #self.client.send(pickle.dumps(letters[randrange(3)]))
            ready = select.select([self.client], [], [], 0)
            if ready[0]:
                data = pickle.loads(self.client.recv(4096))
                print(data)
            else:
                print('no data')
                
            # return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)