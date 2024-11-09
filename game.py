# game.py
import pygame
import sys
from constants import *
from enums import GameState
from enums import PieceType
from board import Board

# Classe principal do jogo, que controla a lógica e a interface
class Game: 
    def __init__(self):
        # Inicializa o Pygame e configura a tela, relógio e objetos iniciais do jogo
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Bobail")  # Define o título da janela
        self.clock = pygame.time.Clock()  # Cria um relógio para controlar a taxa de atualização
        self.board = Board()  # Instancia o tabuleiro do jogo
        self.selected_piece = None  # Inicializa a peça selecionada pelo jogador
        self.valid_moves = []  # Lista de movimentos válidos para a peça selecionada
        self.game_over = False  # Variável que indica se o jogo acabou
        self.game_state = GameState.RED_MOVE  # Define o primeiro turno para o jogador vermelho
        self.first_turn = True  # Marca que é o primeiro turno do jogo

    # Retorna o jogador atual com base no estado do jogo
    def get_current_player(self):
        if self.game_state in [GameState.RED_MOVE, GameState.RED_BOBAIL]:
            return "Vermelho"
        return "Verde"

    # Retorna a ação atual com base no estado do jogo
    def get_current_action(self):
        if self.game_state in [GameState.RED_MOVE, GameState.GREEN_MOVE]:
            return "mover peça"
        return "mover Bobail"

    # Função principal para rodar o loop do jogo
    def run(self):
        while True:
            self.handle_events()  # Lida com eventos de entrada do usuário
            self.draw()  # Desenha o estado atual do jogo na tela
            self.clock.tick(60)  # Limita o loop do jogo a 60 FPS

    # Gerencia eventos, como fechar a janela e cliques do mouse
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Fecha o jogo se a janela for fechada
                pygame.quit()
                sys.exit()
            
            # Se o mouse foi pressionado e o jogo não acabou, lida com o clique
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.handle_click(event.pos)

    # Função para processar o clique do mouse
    def handle_click(self, pos):
        margin = SQUARE_SIZE
        row = (pos[1] - margin) // SQUARE_SIZE  # Calcula a linha do clique
        col = (pos[0] - margin) // SQUARE_SIZE  # Calcula a coluna do clique

        # Verifica se o clique está dentro do tabuleiro
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        clicked_piece = self.board.get_piece(row, col)  # Obtém a peça clicada

        # Se o jogador está selecionando uma peça
        if clicked_piece is not None:
            valid_selection = False
            
            # Define se a peça selecionada é válida com base no turno e no tipo de peça
            if self.first_turn and self.game_state == GameState.RED_MOVE:
                valid_selection = clicked_piece.piece_type == PieceType.RED
            elif self.game_state in [GameState.RED_BOBAIL, GameState.GREEN_BOBAIL]:
                valid_selection = clicked_piece.piece_type == PieceType.BOBAIL
            elif self.game_state == GameState.RED_MOVE:
                valid_selection = clicked_piece.piece_type == PieceType.RED
            elif self.game_state == GameState.GREEN_MOVE:
                valid_selection = clicked_piece.piece_type == PieceType.GREEN

            # Armazena a peça selecionada e os movimentos válidos
            if valid_selection:
                self.selected_piece = clicked_piece
                self.valid_moves = self.board.get_valid_moves(clicked_piece)

        # Se uma peça já foi selecionada e o jogador está tentando movê-la
        elif self.selected_piece and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected_piece, row, col)  # Move a peça para a nova posição
            
            # Verifica se o movimento causa vitória
            if self.selected_piece.piece_type == PieceType.BOBAIL:
                if row == 0 and self.get_current_player() == "Verde":
                    self.game_over = True
                elif row == BOARD_SIZE-1 and self.get_current_player() == "Vermelho":
                    self.game_over = True
            elif self.board.is_bobail_surrounded():
                # Se o Bobail está cercado, o jogador atual vence
                self.game_over = True
                return  # Importante retornar aqui para encerrar a jogada

            # Atualiza o estado do jogo para o próximo jogador ou ação
            if self.first_turn:
                self.first_turn = False
                self.game_state = GameState.GREEN_BOBAIL
            else:
                self.game_state = {
                    GameState.RED_MOVE: GameState.GREEN_BOBAIL,
                    GameState.GREEN_BOBAIL: GameState.GREEN_MOVE,
                    GameState.GREEN_MOVE: GameState.RED_BOBAIL,
                    GameState.RED_BOBAIL: GameState.RED_MOVE
                }[self.game_state]

            self.selected_piece = None  # Limpa a seleção de peça
            self.valid_moves = []  # Limpa os movimentos válidos

    # Desenha o tabuleiro, peças e informações do jogo
    def draw(self):
        self.screen.fill(WHITE)  # Preenche o fundo com a cor branca
        margin = SQUARE_SIZE

        # Desenha o tabuleiro com linhas e quadrados
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = margin + col * SQUARE_SIZE
                y = margin + row * SQUARE_SIZE
                pygame.draw.rect(self.screen, BOARD_COLOR, 
                               (x, y, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(self.screen, BLACK, 
                               (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

        # Destaca os movimentos válidos para a peça selecionada
        for row, col in self.valid_moves:
            x = margin + col * SQUARE_SIZE
            y = margin + row * SQUARE_SIZE
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, 
                           (x, y, SQUARE_SIZE, SQUARE_SIZE))

        # Desenha as peças no tabuleiro
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece:
                    x = margin + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = margin + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(self.screen, piece.get_color(), 
                                     (x, y), PIECE_RADIUS)
                    if piece == self.selected_piece:
                        pygame.draw.circle(self.screen, BLACK, 
                                         (x, y), PIECE_RADIUS, 3)

        # Exibe o turno atual ou mensagem de vitória
        font = pygame.font.Font(None, 36)
        if not self.game_over:
            turn_text = f"Jogador {self.get_current_player()} deve {self.get_current_action()}"
            text = font.render(turn_text, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE//2, SQUARE_SIZE//2))
            self.screen.blit(text, text_rect)
        else:
            text = font.render(f"Jogador {self.get_current_player()} Venceu!", 
                             True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()  # Atualiza a tela com o conteúdo desenhado