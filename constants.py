# constants.py
import pygame

# Constantes do jogo
TAMANHO_JANELA = 800
TAMANHO_TABULEIRO = 5
TAMANHO_QUADRADO = TAMANHO_JANELA // (TAMANHO_TABULEIRO + 2)  # Margem de 1 quadrado em cada lado
RAIO_PECA = TAMANHO_QUADRADO // 2 - 10

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
COR_TABULEIRO = (240, 217, 181)
COR_DESTAQUE = (186, 202, 68)