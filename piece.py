# piece.py
from constants import RED, GREEN, YELLOW
from enums import PieceType

class Piece:
    def __init__(self, piece_type, row, col):
        self.piece_type = piece_type
        self.row = row
        self.col = col

    def move(self, row, col):
        self.row = row
        self.col = col

    def get_color(self):
        if self.piece_type == PieceType.RED:
            return RED
        elif self.piece_type == PieceType.GREEN:
            return GREEN
        elif self.piece_type == PieceType.BOBAIL:
            return YELLOW
        return None