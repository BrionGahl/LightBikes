from PyQt5.QtWidgets import *

import sys

from driver.window import Window

def main():
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()