# Importa a classe Game do arquivo game.py
from jogo import Jogo

# Garante que o código dentro desse bloco seja executado
# somente quando main.py é executado diretamente.
if __name__ == "__main__":
    # Cria uma instância do jogo
    jogo = Jogo()
    
    # Inicia o loop principal do jogo
    jogo.executar()