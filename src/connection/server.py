import socket
import threading

# Sender thread to send commands
# Listener thread to listen for commands

class Server():
    PORT = 4477
    MAX_PLAYERS = 2
    
    def __init__(self):
        self._acceptingPlayers = True
        self._connectedPlayers = []
        try:
            self._s = socket.socket()
            self._s.bind(('', Server.PORT))
            self._s.listen(Server.MAX_PLAYERS)
        except:
            print("error establishing server.")
        
        while self._acceptingPlayers:
            conn, addr = self._s.accept()
            print("connection from", addr[0])
            
            currPlayer = Player(conn, len(self._connectedPlayers), self._connectedPlayers)
            self._connectedPlayers.append(currPlayer)
            
            threading.Thread(target=currPlayer.run, args=()).start()
            
            self._acceptingPlayers = len(self._connectedPlayers) < Server.MAX_PLAYERS

class Player():
    #conn will be closed in this class
    def __init__(self, conn, playerNumber, connectedPlayers):
        self._conn = conn
        self._connectedPlayers = connectedPlayers
        self._playerNumber = playerNumber
        return
        
    def run(self):
        threading.Thread(target=self.listener, args=()).start()
        
        print("sending player number: " + str(self._playerNumber))
        self.sendPlayerNumber()
        
        if (self._playerNumber + 1 == Server.MAX_PLAYERS):
            self.startGame()
    
    def listener(self):
        while True:
            print("Listening...")
            #print("RECV: " + self._conn.recv(1024).decode())
            #self.parseCommands(line)
    
    def parseCommands(self, line):
        commands = line.split(";")
        for command in commands:
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
            self._conn.send(commandString.encode())
        except:
            print("failed to send command.")
            
    def makeCommandString(self, command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString):
        cmdArr = commandString.split(":")
        command = cmdArr[0]
        value = cmdArr[1]
        
        if command == "set-location":
            self.pushToOthers(self._playerNumber, "update-location:" + value)
        elif command == "set-dead":
            self.pushToOthers(self._playerNumber, "dead:" + value)

    # Commands
    def startGame(self):
        self.pushToAll(self.makeCommandString("start-game", "true"))
        
    def sendPlayerNumber(self):
        self.send(self.makeCommandString("set-number", str(self._playerNumber)))