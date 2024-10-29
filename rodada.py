from subrodada import Subrodada

class Rodada():
    CARTAS_FAMILIA = {'Q', 'J', 'K', 'A'}

    def __init__(self, jogadores, equipes, baralho, pontos_da_rodada=1):
        self.jogadores = jogadores
        self.equipes = equipes # Equipes A e B são passadas uma vez pela classe Jogo
        self.baralho = baralho
        self.maos_descartadas = []
        self.ultimo_pedido_aumento = None
        self.pontos_da_rodada = 1 # Sempre começa valendo 1 ponto

    def distribuirMaos(self, ordem_jogadores):
        jogador_anterior = ordem_jogadores[-1] # Jogador anterior ao primeiro a jogar

        metodo_distribuicao = jogador_anterior.escolherMetodoDistribuicao(jogador_anterior) # Pede para o jogador anterior escolher o método de distribuição

        for jogador in self.jogadores:  
            cartas = self.baralho.distribuirCartas(3, metodo_distribuicao) # Distribui 3 cartas para cada jogador com base no método escolhido
            jogador.receberCartas(cartas)

    # ----------

    def realizarPreRodada(self, rodadas_jogadas, pontuacao_jogo, ordem_jogadores):
        for jogador in self.jogadores: # Esvazia as mãos dos jogadores antes de distribuir novas cartas
            jogador.mao.clear()

        self.distribuirMaos(ordem_jogadores)
        jogadores_pediram_familia = False

        equipe_a = self.equipes['Equipe A']
        equipe_b = self.equipes['Equipe B']

        # Fase 1: Decisões individuais de manter ou pedir Família
        for jogador in ordem_jogadores:
            print(f'\n----- PRÉ-RODADA (RODADA {rodadas_jogadas}) - {jogador.nome} ({jogador.equipe.nome}) -----\n--- Veja sua mão e decida se quer ficar com ela ou pedir uma nova ---')
            jogador.mostrarMao()
            mao_descartada = jogador.exibirMenuAcoes(self.equipes, None, self.baralho, pre_rodada=True, maos_descartadas=self.maos_descartadas)

            if mao_descartada:
                self.maos_descartadas.append((jogador, mao_descartada))
                jogadores_pediram_familia = True
                print(f'\n{jogador.nome} ({jogador.equipe.nome}) pediu Família.\nFamílias pedidas: {len(self.maos_descartadas)}/3'.upper())
        
        # Fase 2: Verificar famílias
        for jogador in ordem_jogadores:
            if self.maos_descartadas:
                print(f'\n----- VERIFICAÇÃO DE FAMÍLIAS - {jogador.nome} ({jogador.equipe.nome}) -----\n--- Você pode abrir a(s) mão(s) descartadas pelos jogadores da equipe adversária. Se não forem famílias (constituídas por Q, J, K ou A), sua equipe ganha 1 ponto. Se forem, a equipe adversária ganha 1 ponto. ---')
                jogador.verificarFamilias(self.maos_descartadas, self.equipes)
                print(f'\nPontuação atual: {pontuacao_jogo}')

        print(f'\nA PRÉ-RODADA TERMINOU. A MD3 COMEÇARÁ AGORA.')
    
    def realizarRodada(self, rodadas_jogadas, ordem_jogadores):
        self.pontos_da_rodada = 1

        vitorias_equipes = {'Equipe A': 0, 'Equipe B': 0}

        equipe_a = self.equipes['Equipe A']
        equipe_b = self.equipes['Equipe B']

        for i in range(3): # Melhor de 3 subrodadas
            print(f'\n----- RODADA {rodadas_jogadas} -----')
            print(f'--- Subrodada {i + 1} de 3 ---')

            # Cria uma nova subrodada
            subrodada = Subrodada(ordem_jogadores, self.equipes)
            # Realiza a subrodada
            resultado_subrodada = subrodada.realizarSubrodada(self.pontos_da_rodada)

            # Atualiza a pontuação da rodada se houver um pedido de Truco, Seis, etc
            if isinstance(resultado_subrodada, tuple):
                resultado_subrodada, self.pontos_da_rodada = resultado_subrodada
            
            # Se houve desistência, encerra a rodada inteira
            if resultado_subrodada == 'desistencia':
                equipe_desistiu = subrodada.jogadores[0].equipe.nome # Usa qualquer jogador para descobrir quem desistiu
                equipe_adversaria = 'Equipe A' if equipe_desistiu == 'Equipe B' else 'Equipe B'

                print(f'\nA {equipe_adversaria} venceu a rodada por desistência da {equipe_desistiu}!')
                return self.equipe_adversaria.nome, self.pontos_da_rodada # A equipe adversária ganha os pontos
            
            # Verifica se houve um vencedor ou um empate na subrodada
            if resultado_subrodada is None:
                vitorias_equipes['Equipe A'] += 1
                vitorias_equipes['Equipe B'] += 1
                print(f'A {i + 1}ª subrodada terminou em empate!')
            elif resultado_subrodada in vitorias_equipes:
                vitorias_equipes[resultado_subrodada] += 1
                print(f'\nA {resultado_subrodada} venceu a {i + 1}ª subrodada!')

            # Verifica se a MD3 terminou empatada (sequência de 1 vitória para ambas equipes e um empate)
            if vitorias_equipes['Equipe A'] == 1 and vitorias_equipes['Equipe B'] == 1 and i == 2:
                print(f'\nA rodada terminou empatada! Nenhuma equipe receberá pontos.')
                return None, 0 # Empate na rodada, ninguém ganha pontos

            # Verifica se ambas as equipes estão com 2 pontos (sequência de 2 empates)
            if vitorias_equipes['Equipe A'] == 2 and vitorias_equipes['Equipe B'] == 2:
                print(f'\nAmbas as equipes estão com 2 pontos de subrodada. A próxima subrodada será decisiva!')
                continue # Pula o código abaixo e vai para a próxima iteração do loop
                
            # Verifica se uma das Equipes já venceu 2 subrodadas
            if vitorias_equipes['Equipe A'] >= 2:
                print(f'\nEquipe A venceu a rodada por {vitorias_equipes['Equipe A']} a {vitorias_equipes['Equipe B']}!')
                return 'Equipe A', self.pontos_da_rodada # Retorna a equipe vencedora e os pontos da rodada
            elif vitorias_equipes['Equipe B'] >= 2:
                print(f'\nEquipe B venceu a rodada por {vitorias_equipes['Equipe B']} a {vitorias_equipes['Equipe A']}!')
                return 'Equipe B', self.pontos_da_rodada # Retorna a equipe vencedora e os pontos da rodada
        
        return None, self.pontos_da_rodada # Caso todas as subrodadas sejam jogadas sem um vencedor antecipado