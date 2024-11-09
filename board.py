
# board.py
from constants import BOARD_SIZE
from enums import PieceType
from piece import Piece

class Board: #tabuleiro
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.valid_moves = []
        self.setup_board()

    def setup_board(self):
        # Colocar peças verdes na primeira linha
        for col in range(BOARD_SIZE):
            self.board[0][col] = Piece(PieceType.GREEN, 0, col)

        # Colocar peças vermelhas na última linha
        for col in range(BOARD_SIZE):
            self.board[BOARD_SIZE-1][col] = Piece(PieceType.RED, BOARD_SIZE-1, col)

        # Colocar Bobail no centro
        center = BOARD_SIZE // 2
        self.board[center][center] = Piece(PieceType.BOBAIL, center, center)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move_piece(self, piece, new_row, new_col):
        old_row, old_col = piece.row, piece.col
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.move(new_row, new_col)


    def get_valid_moves(self, piece):
        valid_moves = []
        if not piece:
            return valid_moves

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Ortogonal
                     (1, 1), (-1, -1), (1, -1), (-1, 1)] # Diagonal

        if piece.piece_type == PieceType.BOBAIL:
            # Bobail só pode mover uma casa
            for dr, dc in directions:
                new_row = piece.row + dr
                new_col = piece.col + dc
                if (0 <= new_row < BOARD_SIZE and 
                    0 <= new_col < BOARD_SIZE and 
                    self.board[new_row][new_col] is None):
                    valid_moves.append((new_row, new_col))
        else:
            # Outras peças devem mover até o final em cada direção
            for dr, dc in directions:
                new_row = piece.row
                new_col = piece.col
                last_valid = None
                
                # Continue movendo na mesma direção até encontrar um obstáculo
                while True:
                    new_row += dr
                    new_col += dc
                    
                    # Verifica se está fora do tabuleiro
                    if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                        if last_valid is not None:
                            valid_moves.append(last_valid)
                        break
                    
                    # Verifica se encontrou outra peça
                    if self.board[new_row][new_col] is not None:
                        if last_valid is not None:
                            valid_moves.append(last_valid)
                        break
                    
                    # Atualiza a última posição válida
                    last_valid = (new_row, new_col)
                
                # Se chegou ao final de uma direção sem obstáculos
                if last_valid is not None:
                    valid_moves.append(last_valid)

        return valid_moves


    def is_bobail_surrounded(self): #Bobail está cercado
        bobail = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.board[row][col] and 
                    self.board[row][col].piece_type == PieceType.BOBAIL):
                    bobail = self.board[row][col]
                    break
        
        if not bobail:
            return False

        return len(self.get_valid_moves(bobail)) == 0