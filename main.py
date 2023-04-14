import socket
from socket_server import server

#HOST = '127.0.0.1'

HOST = '10.65.4.32'
PORT = 5001


if __name__ == '__main__':
    s = server.Server(HOST, PORT)



