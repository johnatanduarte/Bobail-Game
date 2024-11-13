# game.py
import pygame
import sys
from constants import *
from enums import EstadoJogo
from enums import TipoPeca
from tabuleiro import Tabuleiro

# Classe principal do jogo, que controla a lógica e a interface
class Jogo:
    def __init__(self):
        # Inicializa o Pygame e configura a janela e o título
        pygame.init()
        self.tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
        pygame.display.set_caption("Bobail")
        # Inicializa o relógio para controlar a taxa de atualização
        self.relogio = pygame.time.Clock()
        # Cria o tabuleiro e define variáveis de controle do jogo
        self.tabuleiro = Tabuleiro()
        self.peca_selecionada = None  # Peça atualmente selecionada
        self.movimentos_validos = []  # Movimentos válidos para a peça selecionada
        self.fim_de_jogo = False  # Indica se o jogo terminou
        # Define o estado inicial do jogo (jogador vermelho começa movendo uma peça)
        self.estado_jogo = EstadoJogo.MOVIMENTO_VERMELHO
        self.primeiro_turno = True  # Controla o primeiro turno

    def obter_jogador_atual(self):
        # Retorna o jogador atual com base no estado do jogo
        if self.estado_jogo in [EstadoJogo.MOVIMENTO_VERMELHO, EstadoJogo.BOBAIL_VERMELHO]:
            return "Vermelho"
        return "Verde"

    def obter_acao_atual(self):
        # Retorna a ação atual que o jogador deve executar (mover peça ou mover o Bobail)
        if self.estado_jogo in [EstadoJogo.MOVIMENTO_VERMELHO, EstadoJogo.MOVIMENTO_VERDE]:
            return "mover peça"
        return "mover Bobail"

    def executar(self):
        # Loop principal do jogo
        while True:
            self.lidar_com_eventos()  # Processa os eventos (como cliques do jogador)
            self.desenhar()  # Atualiza a tela com os gráficos do jogo
            self.relogio.tick(60)  # Controla a taxa de atualização para 60 FPS

    def lidar_com_eventos(self):
        # Processa eventos de Pygame, como fechar a janela ou clicar com o mouse
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Verifica se o jogador clicou na tela e o jogo ainda está em andamento
            if evento.type == pygame.MOUSEBUTTONDOWN and not self.fim_de_jogo:
                self.lidar_com_clique(evento.pos)  # Processa o clique

    def lidar_com_clique(self, pos):
        # Converte a posição do clique em coordenadas de linha e coluna do tabuleiro
        margem = TAMANHO_QUADRADO
        linha = (pos[1] - margem) // TAMANHO_QUADRADO
        coluna = (pos[0] - margem) // TAMANHO_QUADRADO

        # Verifica se o clique foi dentro do tabuleiro
        if not (0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO):
            return

        # Obtém a peça clicada, se houver
        peca_clicada = self.tabuleiro.obter_peca(linha, coluna)

        # Selecionando uma peça
        if peca_clicada is not None:
            selecao_valida = False
            
            # Verifica se a peça selecionada é válida para o estado atual do jogo
            if self.primeiro_turno and self.estado_jogo == EstadoJogo.MOVIMENTO_VERMELHO:
                selecao_valida = peca_clicada.tipo_peca == TipoPeca.VERMELHA
            elif self.estado_jogo in [EstadoJogo.BOBAIL_VERMELHO, EstadoJogo.BOBAIL_VERDE]:
                selecao_valida = peca_clicada.tipo_peca == TipoPeca.BOBAIL
            elif self.estado_jogo == EstadoJogo.MOVIMENTO_VERMELHO:
                selecao_valida = peca_clicada.tipo_peca == TipoPeca.VERMELHA
            elif self.estado_jogo == EstadoJogo.MOVIMENTO_VERDE:
                selecao_valida = peca_clicada.tipo_peca == TipoPeca.VERDE

            # Se a seleção for válida, define a peça selecionada e obtém os movimentos válidos
            if selecao_valida:
                self.peca_selecionada = peca_clicada
                self.movimentos_validos = self.tabuleiro.obter_movimentos_validos(peca_clicada)

        # Movendo uma peça selecionada
        elif self.peca_selecionada and (linha, coluna) in self.movimentos_validos:
            self.tabuleiro.mover_peca(self.peca_selecionada, linha, coluna)
            
            # Verificar condições de vitória ao mover o Bobail ou cercá-lo
            if self.peca_selecionada.tipo_peca == TipoPeca.BOBAIL:
                if linha == 0 and self.obter_jogador_atual() == "Verde":
                    self.fim_de_jogo = True  # Vitória do jogador verde
                elif linha == TAMANHO_TABULEIRO-1 and self.obter_jogador_atual() == "Vermelho":
                    self.fim_de_jogo = True  # Vitória do jogador vermelho
            elif self.tabuleiro.bobail_cercado():
                # Se o Bobail foi cercado, o jogador atual vence
                self.fim_de_jogo = True
                return  # Interrompe o processamento para manter o vencedor

            # Atualiza o estado do jogo para alternar os turnos
            if self.primeiro_turno:
                self.primeiro_turno = False
                self.estado_jogo = EstadoJogo.BOBAIL_VERDE
            else:
                # Alterna o estado do jogo entre as fases de movimento e de movimentação do Bobail
                self.estado_jogo = {
                    EstadoJogo.MOVIMENTO_VERMELHO: EstadoJogo.BOBAIL_VERDE,
                    EstadoJogo.BOBAIL_VERDE: EstadoJogo.MOVIMENTO_VERDE,
                    EstadoJogo.MOVIMENTO_VERDE: EstadoJogo.BOBAIL_VERMELHO,
                    EstadoJogo.BOBAIL_VERMELHO: EstadoJogo.MOVIMENTO_VERMELHO
                }[self.estado_jogo]

            # Limpa a seleção de peça e os movimentos válidos
            self.peca_selecionada = None
            self.movimentos_validos = []

    def desenhar(self):
        # Define o fundo da tela
        self.tela.fill(BRANCO)
        margem = TAMANHO_QUADRADO

        # Desenha o tabuleiro, linha por linha e coluna por coluna
        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                x = margem + coluna * TAMANHO_QUADRADO
                y = margem + linha * TAMANHO_QUADRADO
                pygame.draw.rect(self.tela, COR_TABULEIRO, 
                               (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
                pygame.draw.rect(self.tela, PRETO, 
                               (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 1)

        # Destaca os movimentos válidos para a peça selecionada
        for linha, coluna in self.movimentos_validos:
            x = margem + coluna * TAMANHO_QUADRADO
            y = margem + linha * TAMANHO_QUADRADO
            pygame.draw.rect(self.tela, COR_DESTAQUE, 
                           (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        # Desenha todas as peças no tabuleiro
        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                peca = self.tabuleiro.obter_peca(linha, coluna)
                if peca:
                    x = margem + coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                    y = margem + linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                    pygame.draw.circle(self.tela, peca.obter_cor(), 
                                     (x, y), RAIO_PECA)
                    if peca == self.peca_selecionada:
                        pygame.draw.circle(self.tela, PRETO, 
                                         (x, y), RAIO_PECA, 3)

        # Exibe o texto do turno atual ou o texto de vitória
        fonte = pygame.font.Font(None, 36)
        if not self.fim_de_jogo:
            texto_turno = f"Jogador {self.obter_jogador_atual()} deve {self.obter_acao_atual()}"
            texto = fonte.render(texto_turno, True, PRETO)
            retangulo_texto = texto.get_rect(center=(TAMANHO_JANELA//2, TAMANHO_QUADRADO//2))
            self.tela.blit(texto, retangulo_texto)
        else:
            texto = fonte.render(f"Jogador {self.obter_jogador_atual()} Venceu!", 
                             True, PRETO)
            retangulo_texto = texto.get_rect(center=(TAMANHO_JANELA//2, TAMANHO_QUADRADO//2))
            self.tela.blit(texto, retangulo_texto)

        # Atualiza a tela com o que foi desenhado
        pygame.display.flip()