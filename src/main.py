from PyQt5.QtWidgets import *
import sys
import argparse

from driver.window import Window

def runServer():
    print("--server or -s was given.")
    return


def main():
    parser = argparse.ArgumentParser(description="Multiplayer LightBikes, developed in Python.")
    parser.add_argument(dest="ip", metavar="ip", type=str, nargs="?", default="localhost", help="ip address of server, default is localhost")
    parser.add_argument("-s", "--server", dest="server", action="store_true", help="run as host server")
    args = parser.parse_args()
    
    ip = args.ip
    if args.server:
        runServer()
        ip = "localhost"
    print(ip)
    
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()