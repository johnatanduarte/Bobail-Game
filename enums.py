# enums.py
from enum import Enum

class TipoPeca(Enum):
    VAZIA = 0
    VERMELHA = 1
    VERDE = 2
    BOBAIL = 3

class EstadoJogo(Enum):
    MOVIMENTO_VERMELHO = 1      # Jogador 1 move peça vermelha
    BOBAIL_VERDE = 2  # Jogador 2 move Bobail
    MOVIMENTO_VERDE = 3    # Jogador 2 move peça verde
    BOBAIL_VERMELHO = 4    # Jogador 1 move Bobail