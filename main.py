import socket
from socket_server import server

#HOST = '127.0.0.1'

HOST = '192.168.1.27'
PORT = 5001


if __name__ == '__main__':
    server.Server(HOST, PORT)



