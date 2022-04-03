import socket

class Server():
    PORT = 4477
    
    def __init__(self):
        s = socket.socket()
        s.bind(('', Server.PORT))
        
        s.listen(2)
        
        while True:
            conn, addr = s.accept()
            print("connection from ", addr)
            conn.send('Thanks for connecting'.encode())
            conn.close()