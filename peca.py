# Importa as constantes de cores e os tipos de peças do jogo
from constants import VERMELHO, VERDE, AMARELO
from enums import TipoPeca

# Classe que representa uma peça no jogo
class Peca:
    # Método construtor que inicializa uma peça com seu tipo, linha e coluna
    def __init__(self, tipo_peca, linha, coluna):
        self.tipo_peca = tipo_peca  # Define o tipo da peça (VERMELHA, VERDE ou BOBAIL)
        self.linha = linha          # Define a posição inicial da peça na linha do tabuleiro
        self.coluna = coluna        # Define a posição inicial da peça na coluna do tabuleiro

    # Método para mover a peça para uma nova posição
    def mover(self, nova_linha, nova_coluna):
        self.linha = nova_linha     # Atualiza a linha da peça com a nova posição
        self.coluna = nova_coluna   # Atualiza a coluna da peça com a nova posição

    # Método para obter a cor correspondente ao tipo da peça
    def obter_cor(self):
        if self.tipo_peca == TipoPeca.VERMELHA:
            return VERMELHO         # Retorna a cor vermelha para peças do tipo VERMELHA
        elif self.tipo_peca == TipoPeca.VERDE:
            return VERDE            # Retorna a cor verde para peças do tipo VERDE
        elif self.tipo_peca == TipoPeca.BOBAIL:
            return AMARELO          # Retorna a cor amarela para a peça do tipo BOBAIL
        return None                 # Retorna None se o tipo da peça não for reconhecido
