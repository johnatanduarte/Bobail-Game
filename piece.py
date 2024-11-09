# Importa as constantes de cores e os tipos de peças do jogo
from constants import RED, GREEN, YELLOW
from enums import PieceType

# Classe que representa uma peça no jogo
class Piece:
    # O método __init__ inicializa a peça com seu tipo, linha e coluna
    def __init__(self, piece_type, row, col):
        # Define o tipo da peça (vermelha, verde ou Bobail)
        self.piece_type = piece_type
        # Define a posição da peça no tabuleiro (linha e coluna)
        self.row = row
        self.col = col

    # Método para mover a peça para uma nova posição no tabuleiro
    def move(self, row, col):
        # Atualiza as coordenadas (linha e coluna) da peça
        self.row = row
        self.col = col

    # Método que retorna a cor da peça com base no tipo da peça
    def get_color(self):
        # Verifica o tipo da peça e retorna a cor correspondente
        if self.piece_type == PieceType.RED:
            return RED  # Retorna a cor vermelha (do jogador 1)
        elif self.piece_type == PieceType.GREEN:
            return GREEN  # Retorna a cor verde (do jogador 2)
        elif self.piece_type == PieceType.BOBAIL:
            return YELLOW  # Retorna a cor amarela (do Bobail)
        return None  # Caso não seja um tipo válido de peça, retorna None
