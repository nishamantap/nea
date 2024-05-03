import socket

class Network:
    def __init__(self):
        #Initializes the network connection by creating a socket (self.client)
        # using the given server address (self.server) and port number (self.port).
        print('initialising')
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = '127.0.0.1'
        self.port = 5555
        #Retrieves an ID from the server upon successful connection and stores it in the id attribute.
        # Prints the initialized ID.
        self.addr = (self.server,self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
         #establishes a connection to the server address (self.addr) using the socket's connect method.
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self,data):
        #Sends data (data) to the server using the socket's sendall method after encoding it as bytes.
        #Waits to receive a response from the server (with a maximum buffer size of 2048 bytes).
        #Decodes the received response and returns it.
        try:
            self.client.sendall(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
