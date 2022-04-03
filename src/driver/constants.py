from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    UP = 4

class Color(Enum):
    BLUE = 0x27AAFF
    ORANGE = 0xFF9727
    GREEN = 0x65EC40
    PINK = 0xF551FF

class Controller():
    SPEED = 80
    BLOCKWIDTH = 60
    BLOCKHEIGHT = 40