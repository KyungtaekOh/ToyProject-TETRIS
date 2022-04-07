import socket 
import pickle


class Client:
    def __init__(self, ip=None, port=8080):
        self.__SIZE = 512
        self.__connection = False
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__addr = (ip, port)

    def is_connect(self):
        return self.__connection
    
    def connect(self):
        try:
            self.__socket.connect(self.__addr)
            self.__connection = True
            print("Successful Connect!")
        except socket.error as err:
            str(err)

    def receive(self, verbose=True):
        data = self.__socket.recv(self.__SIZE)
        data = pickle.loads(data)
        if verbose:
            print("Receive :", data)
        return data

    def send(self, data, verbose=True):
        self.__socket.send(pickle.dumps(data))
        if verbose:
            print("Send : ", data)
