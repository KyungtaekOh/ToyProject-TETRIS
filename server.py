import socket
import pickle


class Server:
    def __init__(self, port=8080):
        self.__PORT = port
        self.__SIZE = 512
        self.__set_ip()
        self.__connection = False

    def __set_ip(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.connect(("8.8.8.8", 80))
        self.__IP = self.__socket.getsockname()[0]
        self.__socket.close()
        self.__ADDR = (self.__IP, self.__PORT)

    def get_ip(self):
        return self.__IP
    
    def is_connect(self):
        return self.__connection

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.bind(self.__ADDR)
        except socket.error as err:
            str(err)
        self.__socket.listen(2)
        print("Waiting for a connection...")

        self.__connect, self.__addr = self.__socket.accept()
        print("Connect with", self.__addr)
        self.__connection = True
        

    def send(self, data, verbose=True):
        self.__connect.send(pickle.dumps(data))
        if verbose:
            print("Send : ", data)

    def receive(self, verbose=True):
        data = self.__connect.recv(self.__SIZE)
        data = pickle.loads(data)
        if verbose:
            print("Received :", data)
        return data


if __name__=="__main__":
    s = Server()
    s.connect()
    s.send()
    s.receive()
    