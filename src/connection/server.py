import socket
import threading
import sys
# Sender thread to send commands
# Listener thread to listen for commands

class Server():
    PORT = 4477
    MAX_PLAYERS = 2
    
    BYTES = 1024
    
    def __init__(self):
        self._acceptingPlayers = True
        self._connectedPlayers = []
        self._moves = [0, 0]
        
        try:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self._s.bind(("", Server.PORT))
            self._s.listen(Server.MAX_PLAYERS)
        except:
            print("SERVER: error establishing server.")
            sys.exit()
        
        while self._acceptingPlayers:
            conn, addr = self._s.accept()
            print("SERVER: connection from", addr[0])
            
            currPlayer = Player(conn, len(self._connectedPlayers), self._moves, self._connectedPlayers)
            self._connectedPlayers.append(currPlayer)
            
            threading.Thread(target=currPlayer.run, args=()).start()
            
            self._acceptingPlayers = len(self._connectedPlayers) < Server.MAX_PLAYERS
        

class Player():
    #conn will be closed in this class
    def __init__(self, conn, playerNumber, moves, connectedPlayers):
        self._conn = conn
        self._connectedPlayers = connectedPlayers
        self._playerNumber = playerNumber
        self._moves = moves
        
        return
        
    def run(self):
        print("SERVER: sending player number: " + str(self._playerNumber))
        self.sendPlayerNumber()
        
        threading.Thread(target=self.listener, args=()).start()
        if (self._playerNumber + 1 == Server.MAX_PLAYERS):
            print("SERVER: maximum players joined, starting game\n\n")
            self.startGame()
    
    def listener(self):
        line = ""
        while True:
            try:
                data = self._conn.recv(1024)
                line = data.decode()
            except Exception as error: # most often occurs when closing a client / server
                #print("SERVER: " + str(error))
                print("SERVER: Shutting down...")
                sys.exit()
            self.parseCommands(line)
    
    def parseCommands(self, line):
        commands = line.split(";")
        for command in commands:
            if command == "":
                continue
            self.processCommand(command)
    
    def getNumber(self):
        return self._playerNumber
    
    def pushToAll(self, commandString):
        for player in self._connectedPlayers:
            player.send(commandString)
            
    def pushToOthers(self, playerNumber, commandString):
        for player in self._connectedPlayers:
            if player.getNumber() != playerNumber:
                player.send(commandString)
               
    def send(self, commandString):
        try:
            self._conn.sendall(commandString.encode())
        except Exception as error:
            print("SERVER: " + str(error))
            
    def makeCommandString(self, command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString):
        cmdArr = commandString.split(":")
        command = cmdArr[0]
        value = cmdArr[1]
        
        if command == "set-location":
            while self._moves[self._playerNumber] > self._moves[1-self._playerNumber]:
                continue
            self.pushToOthers(self._playerNumber, "update-location:" + value + ";")
            self._moves[self._playerNumber] += 1
            print(f"Player: {str(self._playerNumber)} -> {str(self._moves[0])},{str(self._moves[1])}")
        elif command == "set-dead":
            self.pushToOthers(self._playerNumber, "set-dead:" + value)
        elif command == "set-draw":
            self.pushToOthers(self._playerNumber, "set-draw:" + value)

    # Commands
    def startGame(self):
        self.pushToAll(self.makeCommandString("start-game", "true"))
        
    def sendPlayerNumber(self):
        self.send(self.makeCommandString("set-number", str(self._playerNumber)))