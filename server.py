import socket
from _thread import start_new_thread
from thread import *
import sys
from REALGAME import Game

#defines the IP address for the server and the port
server = "127.0.0.1"
port = 5555

#creates a socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Bind the socket to the server address and port, creating a connection
try:
    s.bind((server,port))

except socket.error as e:
    str(e)

s.listen(2)  #listening for connection (2 clients in this case)
print("waiting for connection,server started")


#The threadedclient function sends a "connected" message to the client,
# then continuously receives and sends messages until the client disconnects.

def threadedclient(conn,addr):
    conn.send(str.encode("connected"))


    reply = ""
    while True:
        try:
            data =  conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ",reply)#reply
                print('sending:',reply)

            conn.sendall(str.encode(reply))
        except:
            break
    print('lost connection')
    conn.close()


#continuosly looks for connection
while True:
    conn,addr = s.accept()
    print("connected to : ",addr)

    start_new_thread(threadedclient, (conn,addr))






