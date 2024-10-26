import random
from baralho import Baralho
from jogador import Jogador
from equipe import Equipe
from rodada import Rodada

class Jogo():
    def __init__(self, nomes_jogadores):
        if len(nomes_jogadores) != 4:  
            raise ValueError("O jogo deve ter exatamente 4 jogadores.")
        
        self.baralho = Baralho()
        self.baralho.embaralhar()

        # Criando os jogadores e os embaralhando
        self.jogadores = [Jogador(nome) for nome in nomes_jogadores]
        random.shuffle(self.jogadores)

        # Criando as equipes
        self.equipe_A = Equipe('Equipe A', self.jogadores[:2], None) # Primeiros 2 jogadores na Equipe A
        self.equipe_B = Equipe('Equipe B', self.jogadores[2:], None) # Últimos 2 jogadores na Equipe B

        # Definindo adversários
        self.equipe_A.equipe_adversaria = self.equipe_B
        self.equipe_B.equipe_adversaria = self.equipe_A

        # Definindo as equipes nos jogadores
        for jogador in self.equipe_A.jogadores:
            jogador.equipe = self.equipe_A
        for jogador in self.equipe_B.jogadores:
            jogador.equipe = self.equipe_B

        self.equipes = {'Equipe A': self.equipe_A, 'Equipe B': self.equipe_B}
        self.pontuacao = {'Equipe A': 0, 'Equipe B': 0}
        self.rodadas = []
    
    def verificarVencedorJogo(self): # Verifica se alguma equipe chegou aos 12 pontos e venceu o jogo
        for equipe, pontos in self.pontuacao.items():
            if pontos >= 12:
                print(f'\n{equipe} venceu o jogo com {pontos} pontos!')
                return True
        
        return False
    
    def jogar(self):
        pontos_da_rodada = 1
        rodadas_jogadas = 1
        while not self.verificarVencedorJogo(): # Enquanto não houver um vencedor
            #print(f'Vamos jogar Truco! Para começar, informe o nome de 4 jogadores:\n')
            print(f'\n----- INICIANDO NOVA RODADA ({rodadas_jogadas}) -----\n')

            # Criando uma nova rodada
            nova_rodada = Rodada(self.jogadores, self.equipes, self.baralho, 1)
            nova_rodada.realizarPreRodada(rodadas_jogadas, self.pontuacao) # Distribui as mãos e pede Famílias
            vencedor_rodada, pontos_da_rodada = nova_rodada.realizarRodada(rodadas_jogadas) # Obtém o vencedor e os pontos da rodada

            # Atualizando a pontuação da equipe vencedora
            if vencedor_rodada:
                self.pontuacao[vencedor_rodada] += pontos_da_rodada
                print(f'\nPontuação atual: {self.pontuacao}')
            
            self.baralho.resetarBaralho()

            rodadas_jogadas = rodadas_jogadas + 1
            
            if self.verificarVencedorJogo(): # Se houver uma equipe vencedora no jogo, ele acaba
                break

# Exemplo de nomes de jogadores
nomes_jogadores = ['Jogador 1', 'Jogador 2', 'Jogador 3', 'Jogador 4']
jogo = Jogo(nomes_jogadores)

# Inicia o jogo
jogo.jogar()