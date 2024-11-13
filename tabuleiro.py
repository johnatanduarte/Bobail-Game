# Importação de constantes e classes necessárias
from constants import TAMANHO_TABULEIRO  # Importa o tamanho do tabuleiro definido em constants.py
from enums import TipoPeca  # Importa o tipo das peças (como vermelha, verde, Bobail)
from peca import Peca  # Importa a classe Piece, que representa uma peça no tabuleiro

# Classe que representa o tabuleiro de jogo
class Tabuleiro:
    # Método construtor que inicializa o tabuleiro, seleciona peças e configura o estado inicial
    def __init__(self):
        # Cria uma matriz bidimensional de tamanho definido para representar o tabuleiro
        # Cada posição inicia como None (sem peça)
        self.tabuleiro = [[None for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
        
        # Atributo para armazenar uma peça selecionada (None por padrão)
        self.peca_selecionada = None
        
        # Lista para armazenar movimentos válidos da peça selecionada
        self.movimentos_validos = []
        
        # Configura o tabuleiro com as peças iniciais
        self.configurar_tabuleiro()

    # Método para configurar as peças no tabuleiro no início do jogo
    def configurar_tabuleiro(self):
        # Coloca peças verdes na primeira linha do tabuleiro
        for coluna in range(TAMANHO_TABULEIRO):
            self.tabuleiro[0][coluna] = Peca(TipoPeca.VERDE, 0, coluna)

        # Coloca peças vermelhas na última linha do tabuleiro
        for coluna in range(TAMANHO_TABULEIRO):
            self.tabuleiro[TAMANHO_TABULEIRO-1][coluna] = Peca(TipoPeca.VERMELHA, TAMANHO_TABULEIRO-1, coluna)

        # Coloca a peça especial Bobail no centro do tabuleiro
        centro = TAMANHO_TABULEIRO // 2 #// retorna apenas a parte inteira da divisão
        self.tabuleiro[centro][centro] = Peca(TipoPeca.BOBAIL, centro, centro)

    # Método para obter a peça na posição (linha, coluna) especificada
    def obter_peca(self, linha, coluna):
        return self.tabuleiro[linha][coluna]

    # Método para mover uma peça para uma nova posição no tabuleiro
    def mover_peca(self, peca, nova_linha, nova_coluna):
        antiga_linha, antiga_coluna = peca.linha, peca.coluna  # Posição antiga da peça
        
        # Remove a peça da posição antiga e a coloca na nova posição
        self.tabuleiro[antiga_linha][antiga_coluna] = None
        self.tabuleiro[nova_linha][nova_coluna] = peca
        
        # Atualiza a posição da peça
        peca.mover(nova_linha, nova_coluna)

    # Método para obter os movimentos válidos para uma peça específica
    def obter_movimentos_validos(self, peca):
        movimentos_validos = []  # Lista para armazenar movimentos válidos
        if not peca:  # Retorna uma lista vazia se não houver peça
            return movimentos_validos

        # Direções possíveis para movimentação: ortogonais e diagonais
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Ortogonais
                    (1, 1), (-1, -1), (1, -1), (-1, 1)] # Diagonais

        # Condição para o Bobail, que só pode mover uma casa por vez
        if peca.tipo_peca == TipoPeca.BOBAIL:
            for dr, dc in direcoes:
                nova_linha = peca.linha + dr
                nova_coluna = peca.coluna + dc
                
                # Verifica se a nova posição está dentro dos limites do tabuleiro e está vazia
                if (0 <= nova_linha < TAMANHO_TABULEIRO and 
                    0 <= nova_coluna < TAMANHO_TABULEIRO and 
                    self.tabuleiro[nova_linha][nova_coluna] is None):
                    movimentos_validos.append((nova_linha, nova_coluna))
        
        # Condição para outras peças, que se movem até o final em cada direção
        else:
            for dr, dc in direcoes:
                nova_linha = peca.linha
                nova_coluna = peca.coluna
                ultima_valida = None
                
                # Continua movendo na mesma direção até encontrar um obstáculo
                while True:
                    nova_linha += dr
                    nova_coluna += dc
                    
                    # Verifica se a nova posição está fora dos limites do tabuleiro
                    if not (0 <= nova_linha < TAMANHO_TABULEIRO and 0 <= nova_coluna < TAMANHO_TABULEIRO):
                        if ultima_valida is not None:
                            movimentos_validos.append(ultima_valida)
                        break
                    
                    # Verifica se encontrou outra peça na nova posição
                    if self.tabuleiro[nova_linha][nova_coluna] is not None:
                        if ultima_valida is not None:
                            movimentos_validos.append(ultima_valida)
                        break
                    
                    # Atualiza a última posição válida para o movimento
                    ultima_valida = (nova_linha, nova_coluna)
                
                # Adiciona o movimento se chegou ao final da direção sem obstáculos
                if ultima_valida is not None:
                    movimentos_validos.append(ultima_valida)

        return movimentos_validos  # Retorna a lista de movimentos válidos

    def bobail_cercado(self):
        # Inicializa a variável para armazenar a peça Bobail
        bobail = None
        
        # Percorre cada posição no tabuleiro para encontrar a peça Bobail
        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                # Verifica se há uma peça na posição e se é do tipo Bobail
                if (self.tabuleiro[linha][coluna] and 
                    self.tabuleiro[linha][coluna].tipo_peca == TipoPeca.BOBAIL):
                    # Armazena a peça Bobail encontrada
                    bobail = self.tabuleiro[linha][coluna]
                    break  # Sai do loop interno ao encontrar o Bobail

        # Se não encontrou o Bobail, retorna False (não cercado)
        if not bobail:
            return False

        # Retorna True se o Bobail estiver cercado, ou seja, sem movimentos válidos
        return len(self.obter_movimentos_validos(bobail)) == 0