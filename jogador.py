from carta import Carta
from baralho import Baralho

class Jogador():
    def __init__(self, nome, equipe=None, jogador_anterior=None, proximo_jogador=None):
        self.nome = nome
        self.equipe = equipe # É atribuída mais tarde no jogo
        self.mao = []
        self.jogador_anterior = jogador_anterior # O jogador sabe quem foi o último a jogar antes dele
        self.proximo_jogador = proximo_jogador # O jogador sabe quem é o próximo a jogar após ele
    
    def receberCartas(self, cartas):
        self.mao.extend(cartas) # Recebe as cartas distribuídas pelo Baralho
    
    def mostrarMao(self):
        return self.mao
    
    def escolherMetodoDistribuicao(self, jogador_anterior):
        escolha = input(f'{jogador_anterior.nome}, escolha um método de distribuição:\n1. Descendo (de cima para baixo)\n2. Subindo (de baixo para cima)\nInsira sua escolha: ')
        if escolha == '1':
            return 'descendo'
        elif escolha == '2':
            return 'subindo'
        else:
            print('Opção inválida. Usando o método padrão: Descendo.')
            return 'descendo'
    
    def pedirAumento(self, proximo_jogador, tipo_aumento, pontos_da_rodada, carta_escolhida=None):
        # Dicionário para determinar o próximo aumento e os pontos equivalentes
        # 'tipo_aumento': ('proximo_aumento', pontos)
        aumentos = {
            'Truco': ('Seis', 3),
            'Seis': ('Nove', 6),
            'Nove': ('Doze', 9),
            'Doze': (None, 12) # Nenhum aumento após Doze
        }
        
        prox_aumento, pontos = aumentos.get(tipo_aumento, (None, pontos_da_rodada))
        
        while True:
            resposta_aumento = input(f'\nGostaria de pedir {tipo_aumento}?\n1. Sim\n2. Não, voltar\n3. O que é pedir {tipo_aumento}?\nInsira sua escolha: ')

            if resposta_aumento == '1':
                print(f'{self.nome} pediu {tipo_aumento}!')
                resposta = proximo_jogador.responderAumento(self, tipo_aumento) # Resposta do próximo jogador ao aumento
                
                if resposta is True: # Aceitou o aumento
                    print(f'{proximo_jogador.nome} ({proximo_jogador.equipe.nome}) aceitou o {tipo_aumento}! A rodada agora vale {pontos} pontos.')
                    carta_jogada = self.jogarCarta(carta_escolhida)
                    return carta_jogada, pontos # Retorna a carta jogada e pontos atualizados
                
                elif resposta == prox_aumento: # Próximo jogador pede aumento maior
                    tipo_aumento = prox_aumento # Atualiza o tipo de aumento atual
                    prox_aumento, pontos = aumentos.get(tipo_aumento, (None, pontos)) # Atualiza o próximo aumento e os pontos
                    nova_resposta = self.responderAumento(proximo_jogador, tipo_aumento)
                    
                    if nova_resposta is True: # Aceitou o próximo aumento
                        print(f'{self.nome} aceitou o {tipo_aumento}! A rodada agora vale {pontos} pontos.')
                        carta_jogada = self.jogarCarta(carta_escolhida)
                        return carta_jogada, pontos
                    
                    elif nova_resposta is False: # Recusou o aumento
                        print(f'{self.nome} recusou o {tipo_aumento}. A rodada acabou, e vocês ganharam {pontos_da_rodada} pontos.')
                        self.equipe.adicionarPonto(pontos_da_rodada)
                        return pontos_da_rodada
                
                elif resposta is False: # Recusou o aumento
                    print(f'{proximo_jogador.nome} recusou o {tipo_aumento}. A rodada acabou, e vocês ganharam {pontos_da_rodada} pontos.')
                    self.equipe.adicionarPonto(pontos_da_rodada)
                    return pontos_da_rodada
            
            elif resposta_aumento == '2':
                break
            elif resposta_aumento == '3':
                explicacoes = {
                    'Truco': 'Pedir Truco é desafiar a equipe adversária a jogar a rodada atual valendo 3 pontos ao invés de 1.',
                    'Seis': 'Pedir Seis é desafiar a equipe adversária a jogar a rodada atual valendo 6 pontos ao invés de 3.',
                    'Nove': 'Pedir Nove é desafiar a equipe adversária a jogar a rodada atual valendo 9 pontos ao invés de 6.',
                    'Doze': 'Pedir Doze é desafiar a equipe adversária a jogar a rodada atual valendo 12 pontos ao invés de 9.',
                }
                print(explicacoes.get(tipo_aumento, 'Ação inválida.'))


    '''
    def replicarAumento(self, jogador_anterior, proximo_aumento):
        resposta = input(f'{}')
    '''
    def responderAumento(self, jogador_anterior, tipo_aumento):
        #proximo_aumento = None
        if tipo_aumento == 'Truco':
            proximo_aumento = 'Seis'
        elif tipo_aumento == 'Seis':
            proximo_aumento = 'Nove'
        elif tipo_aumento == 'Nove':
            proximo_aumento = 'Doze'
        
        resposta = input(f'\n{self.nome}, {jogador_anterior.nome} ({jogador_anterior.equipe.nome}) está pedindo {tipo_aumento}!\n1. Aceitar\n2. Pedir {proximo_aumento}\n3. Recusar\n4. O que está acontecendo?\nInsira sua escolha: ')
        if resposta == '1':
            return True # Aceitou o aumento
        elif resposta == '2':
            return proximo_aumento
        else:
            return False # Recusou o aumento
    
    def pedirFamilia(self, baralho):
        while True:
            escolha_familia = input(f'\nGostaria de pedir Família?\n1. Sim\n2. Não\n3. O que é pedir Família?\nInsira sua escolha: ')
            if escolha_familia == '1':
                print(f'\nVocê pediu Família.')
                mao_descartada = self.mao[:]
                self.mao.clear()
                self.receberCartas(baralho.distribuirCartas(3))
                print(f'Suas novas cartas: {self.mostrarMao()}')
                return mao_descartada # Retorna a mão descartada
            elif escolha_familia == '2':
                return None # Indica que o jogador não pediu família e encerra
            elif escolha_familia == '3':
                print(f'Pedir Família é solicitar uma nova mão para você, caso perceba que sua mão atual está fraca.\nFamílias são constituídas pelas cartas Q, J, K e A.')
            else:
                print('Opção inválida. Tente novamente.')
    
    def verificarFamilias(self, maos_descartadas, equipes):
        jogadores_descartaram = [
                (jogador, mao) for jogador, mao in maos_descartadas if jogador.equipe != self.equipe
            ]

        if not jogadores_descartaram:
            print('Não há mãos para verificar.')
            return None
        
        while jogadores_descartaram:
            print(f'\nA equipe adversária pediu {len(jogadores_descartaram)} Família(s):')
            for i, (jogador, _) in enumerate(jogadores_descartaram):
                print(f'{i+1}. Verificar Família de {jogador.nome} ({jogador.equipe.nome})')
            print(f'{len(jogadores_descartaram) + 1}. Prosseguir')

            escolha = input(f'Insira sua escolha: ')

            if escolha.isdigit() and 1 <= int(escolha) <= len(jogadores_descartaram):
                jogador_escolhido, mao_escolhida = jogadores_descartaram[int(escolha) - 1]
                self.verificarFamilia(jogador_escolhido, mao_escolhida, equipes)

                if (jogador_escolhido, mao_escolhida) in maos_descartadas:
                    maos_descartadas.remove((jogador_escolhido, mao_escolhida))
                    jogadores_descartaram.remove(jogadores_descartaram[int(escolha) - 1]) # Remove a mão verificada das opções disponíveis para verificar
                    print(f'A mão descartada pelo {jogador_escolhido.nome} ({jogador_escolhido.equipe.nome}) foi removida das opções.')
                else:
                    print(f'ERRO: A mão de {jogador_escolhido.nome} já foi removida ou não está mais disponível.')
            elif escolha == str(len(jogadores_descartaram) + 1):
                break # Volta para o menu principal
            else:
                print('Opção inválida. Tente novamente.')

    def verificarFamilia(self, jogador_escolhido, mao_escolhida, equipes): # Função que verifica se uma mão descartada é família
        CARTAS_FAMILIA = {'Q', 'J', 'K', 'A'}

        print(f'\nMão descartada por {jogador_escolhido.nome} ({jogador_escolhido.equipe.nome}): {mao_escolhida}')

        if all(carta.valor in CARTAS_FAMILIA for carta in mao_escolhida):
            print(f'A mão descartada por {jogador_escolhido.nome} era uma Família! A {jogador_escolhido.equipe.nome} ganhou 1 ponto.')
            equipes[jogador_escolhido.equipe.nome].adicionarPonto(1)
            return True
        else:
            print(f'A mão descartada por {jogador_escolhido.nome} ({jogador_escolhido.equipe.nome}) não era uma Família! Sua equipe ({self.equipe.nome}) ganhou 1 ponto.')
            equipes[self.equipe.nome].adicionarPonto(1)
            return False
    
    def pedirDesistencia(self, pontos_da_rodada):
        print(f'Você pediu para desistir dessa rodada.')
        return self.equipe.registrarPedidoDesistencia(self, pontos_da_rodada)
    
    def confirmarDesistencia(self, pontos_da_rodada):
        resposta = input(f'\n{self.nome}, seu companheiro quer desistir dessa rodada. Confirmar desistência? (s/n): ')
        if resposta.lower() == 's':
            print(f'Você aceitou o pedido de desistência. A rodada atual foi encerrada, e a equipe adversária ganhou {pontos_da_rodada} pontos.')
            return True # Aceitou a Desistência
        else:
            print(f'Você recusou o pedido de desistência. A rodada atual continuará.')
            return False # Recusou a Desistência

    def jogarCarta(self, carta_escolhida=None):
        while True:  
            qtd_cartas = len(self.mao)  
            if qtd_cartas == 0:  
                print("Você não tem cartas para jogar.")  
                return None
            
            print(f'{self.nome}, você tem {qtd_cartas} carta(s) em sua mão')
            
            for i, carta in enumerate(self.mao):
                print(f'{i+1}. {carta}')
            
            escolha_carta = input(f'Escolha uma carta para jogar (1 a {qtd_cartas}): ')

            if escolha_carta.isdigit() and 1 <= int(escolha_carta) <= qtd_cartas:  
                carta_escolhida = self.mao[int(escolha_carta) - 1]
                if isinstance(carta_escolhida, Carta):
                    self.mao.remove(carta_escolhida)
                    print(f'\nVocê jogou a carta: {carta_escolhida}\n')
                    return carta_escolhida # Retorna a carta jogada para uso posterior
                else:
                    print('ERRO: Carta inválida.')
            else:  
                print('Opção inválida. Tente novamente.')
    
    def exibirMenuAcoes(self, equipes, carta_escolhida=None, baralho=None, pre_rodada=False, pontos_da_rodada=1, maos_descartadas=None): # ORIGINALMENTE SEM `pontos_da_rodada`
        while True:
            i = 1

            if pre_rodada:
                print(f'\nSuas cartas: {self.mostrarMao()}')
                print(f'{i}. Manter minhas cartas')
                i += 1

                print(f'{i}. Pedir Família ({len(maos_descartadas)}/3)')
                i += 1

            else:
                print(f'\nVez de {self.nome} ({self.equipe.nome}). Selecione uma ação abaixo.')
                print(f'{i}. Jogar uma carta')
                i += 1

                print(f'{i}. Ver minhas cartas')
                i += 1

                if pontos_da_rodada == 1:
                    print(f'{i}. Pedir Truco')
                elif pontos_da_rodada == 3:
                    print(f'{i}. Pedir Seis')
                elif pontos_da_rodada == 6:
                    print(f'{i}. Pedir Nove')
                elif pontos_da_rodada == 12:
                    print(f'{i}. Pedir Doze')
                i += 1

                print(f'{i}. Pedir para desistir da rodada')

            escolha_acao = input(f'\nInsira sua escolha (1 a {i}): ')

            # Ações de pré-rodada
            if escolha_acao == '1' and pre_rodada:
                return None
            if escolha_acao == '2' and pre_rodada:
                while len(maos_descartadas) < 3:
                    return self.pedirFamilia(baralho)
                
                print(f'\nNão é possível pedir mais Famílias.')
            
            # Ações normais
            if escolha_acao == '1' and not pre_rodada:
                return self.jogarCarta(carta_escolhida)
            elif escolha_acao == '2' and not pre_rodada:
                return self.mostrarMao()
            elif escolha_acao == '3' and not pre_rodada:
                if pontos_da_rodada == 1:
                    return self.pedirAumento(self.proximo_jogador, 'Truco', pontos_da_rodada)
                elif pontos_da_rodada == 3:
                    return self.pedirAumento(self.proximo_jogador, 'Seis', pontos_da_rodada)
                elif pontos_da_rodada == 6:
                    return self.pedirAumento(self.proximo_jogador, 'Nove', pontos_da_rodada)
                elif pontos_da_rodada == 9:
                    return self.pedirAumento(self.proximo_jogador, 'Doze', pontos_da_rodada)
            elif escolha_acao == '4' and not pre_rodada:
                if self.pedirDesistencia(pontos_da_rodada):
                    return 'desistencia'
            else:
                print('Opção inválida. Tente novamente.')