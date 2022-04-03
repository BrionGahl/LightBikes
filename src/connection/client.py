import socket

class Client():
    PORT = 4477
    
    def __init__(self, ip):
        s = socket.socket()
        s.connect((ip, Client.PORT))
        
        print(s.recv(1024).decode())
        
        s.close()