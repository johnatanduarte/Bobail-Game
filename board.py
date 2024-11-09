# Importação de constantes e classes necessárias
from constants import BOARD_SIZE  # Importa o tamanho do tabuleiro definido em constants.py
from enums import PieceType  # Importa o tipo das peças (como vermelha, verde, Bobail)
from piece import Piece  # Importa a classe Piece, que representa uma peça no tabuleiro

# Classe que representa o tabuleiro de jogo
class Board:
    def __init__(self):
        # Inicializa o tabuleiro como uma matriz de BOARD_SIZE x BOARD_SIZE preenchida com None
        # None significa que não há peça naquela posição
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Inicializa a peça selecionada (caso o jogador selecione uma peça)
        self.selected_piece = None
        
        # Lista de movimentos válidos para a peça selecionada
        self.valid_moves = []
        
        # Configura o tabuleiro com as peças iniciais
        self.setup_board()

    def setup_board(self):
        """
        Configura o tabuleiro com as peças iniciais no jogo:
        - Peças verdes na primeira linha (jogador 2)
        - Peças vermelhas na última linha (jogador 1)
        - Bobail no centro do tabuleiro
        """
        # Coloca as peças verdes (jogador 2) na primeira linha
        for col in range(BOARD_SIZE):
            self.board[0][col] = Piece(PieceType.GREEN, 0, col)

        # Coloca as peças vermelhas (jogador 1) na última linha
        for col in range(BOARD_SIZE):
            self.board[BOARD_SIZE-1][col] = Piece(PieceType.RED, BOARD_SIZE-1, col)

        # Coloca o Bobail no centro do tabuleiro
        center = BOARD_SIZE // 2
        self.board[center][center] = Piece(PieceType.BOBAIL, center, center)

    def get_piece(self, row, col):
        """
        Retorna a peça presente na posição especificada (linha, coluna)
        """
        return self.board[row][col]

    def move_piece(self, piece, new_row, new_col):
        """
        Move uma peça para uma nova posição no tabuleiro.
        Atualiza a posição no tabuleiro e move a peça para a nova coordenada.
        """
        # Salva as posições antigas para limpar a célula original
        old_row, old_col = piece.row, piece.col
        
        # Limpa a posição antiga no tabuleiro
        self.board[old_row][old_col] = None
        
        # Coloca a peça na nova posição
        self.board[new_row][new_col] = piece
        
        # Atualiza as coordenadas da peça
        piece.move(new_row, new_col)

    def get_valid_moves(self, piece):
        """
        Calcula os movimentos válidos para uma peça, considerando as direções possíveis.
        A peça pode se mover ortogonalmente ou diagonalmente, conforme as regras do jogo.
        """
        valid_moves = []  # Lista para armazenar os movimentos válidos
        
        # Se a peça for None, não há movimentos válidos
        if not piece:
            return valid_moves

        # Direções possíveis de movimento (ortogonais e diagonais)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Ortogonal
                     (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Diagonal

        # Se a peça for o Bobail, ela pode se mover apenas uma casa em qualquer direção
        if piece.piece_type == PieceType.BOBAIL:
            for dr, dc in directions:
                # Calcula a nova posição a partir da direção
                new_row = piece.row + dr
                new_col = piece.col + dc
                
                # Verifica se a nova posição está dentro dos limites do tabuleiro e está vazia
                if (0 <= new_row < BOARD_SIZE and 
                    0 <= new_col < BOARD_SIZE and 
                    self.board[new_row][new_col] is None):
                    valid_moves.append((new_row, new_col))  # Adiciona o movimento válido
        else:
            # Para outras peças (não Bobail), elas podem mover até o final em cada direção
            for dr, dc in directions:
                new_row = piece.row
                new_col = piece.col
                last_valid = None  # Variável para armazenar a última posição válida
                
                # Continua movendo na direção enquanto não encontrar um obstáculo
                while True:
                    new_row += dr
                    new_col += dc
                    
                    # Se sair do tabuleiro, considera a última posição válida
                    if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                        if last_valid is not None:
                            valid_moves.append(last_valid)  # Adiciona a última posição válida
                        break
                    
                    # Se encontrar outra peça (obstáculo), encerra a busca
                    if self.board[new_row][new_col] is not None:
                        if last_valid is not None:
                            valid_moves.append(last_valid)  # Adiciona a última posição válida
                        break
                    
                    # Atualiza a última posição válida
                    last_valid = (new_row, new_col)
                
                # Se a peça chegou ao final sem obstáculos, adiciona a última posição válida
                if last_valid is not None:
                    valid_moves.append(last_valid)

        return valid_moves  # Retorna todos os movimentos válidos encontrados

    def is_bobail_surrounded(self):
        """
        Verifica se o Bobail está cercado, ou seja, se ele não tem mais movimentos válidos.
        Retorna True se o Bobail estiver cercado, caso contrário, False.
        """
        bobail = None
        
        # Procura o Bobail no tabuleiro
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.board[row][col] and 
                    self.board[row][col].piece_type == PieceType.BOBAIL):
                    bobail = self.board[row][col]  # Encontra o Bobail
                    break
        
        # Se o Bobail não foi encontrado, retorna False
        if not bobail:
            return False

        # Verifica se o Bobail está cercado (sem movimentos válidos)
        return len(self.get_valid_moves(bobail)) == 0
