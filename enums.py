# enums.py
from enum import Enum

class PieceType(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2
    BOBAIL = 3

class GameState(Enum):
    RED_MOVE = 1
    GREEN_BOBAIL = 2
    GREEN_MOVE = 3
    RED_BOBAIL = 4