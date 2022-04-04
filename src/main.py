from PyQt5.QtWidgets import *
import sys
import argparse
import threading

from driver.window import Window

from connection.server import Server

def runServer():
    print("Hosting server...")
    Server()
    return


def main():
    parser = argparse.ArgumentParser(description="Multiplayer LightBikes, developed in Python.")
    parser.add_argument(dest="ip", metavar="ip", type=str, nargs="?", default="localhost", help="ip address of server, default is localhost")
    parser.add_argument("-s", "--server", dest="server", action="store_true", help="run as host server")
    args = parser.parse_args()
        
    ip = args.ip
    if args.server:
        server = threading.Thread(target=runServer, args=(), daemon=True)
        server.start()
        ip = "localhost"
        
    app = QApplication([])
    window = Window(ip)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()