import socket
import time

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.29", 5001))
    s.send(b'aaa')
    time.sleep(0.5)
    data = s.recv(1024).decode('utf-8')
    s.close()
    print(data)
except Exception as inst:
    print(inst)