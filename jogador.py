from carta import Carta
from baralho import Baralho

class Jogador():
    def __init__(self, nome, equipe=None, jogador_anterior=None, proximo_jogador=None):
        self.nome = nome
        self.equipe = equipe # É atribuída mais tarde no jogo
        self.mao = []
        #self.jogador_anterior = jogador_anterior # FUTURAMENTE PARA BOTS # O jogador sabe quem foi o último a jogar antes dele
        self.proximo_jogador = proximo_jogador # O jogador sabe quem é o próximo a jogar após ele
    
    def receberCartas(self, cartas):
        self.mao.extend(cartas)  # Recebe as cartas distribuídas pelo Baralho
    
    def mostrarMao(self):
        return self.mao
    
    def escolherMetodoDistribuicao(self):
        escolha = input(f'Escolha um método de distribuição:\n1. Descendo (de cima para baixo)\n2. Subindo (de baixo para cima)\n')
        if escolha == '1':
            return 'descendo'
        elif escolha == '2':
            return 'subindo'
        else:
            print('Opção inválida. Usando o método padrão: Descendo.')
            return 'descendo'
    
    def pedirAumento(self, proximo_jogador, tipo_aumento, pontos_atual, carta_escolhida=None): # ORIGINALMENTE SEM `carta_escolhia=None` # Pedir Truco ou Seis
        if tipo_aumento == 'Truco':
            pontos = 3
        elif tipo_aumento == 'Seis':
            if pontos_atual < 3:
                print(f'Você não pode pedir Seis se a rodada ainda não estiver Trucada.')
                return pontos_atual
            pontos = 6
        elif tipo_aumento == 'Nove':
            if pontos_atual < 6:
                print(f'Você não pode pedir Nove se a rodada ainda não estiver valendo Seis.')
                return pontos_atual
            pontos = 9
        elif tipo_aumento == 'Doze':
            if pontos_atual < 9:
                print(f'Você não pode pedir Doze se a rodada ainda não estiver valendo Nove.')
                return pontos_atual
            pontos = 12
        else:
            return pontos_atual
        
        while True:
            resposta = input(f'\nGostaria de pedir {tipo_aumento}?\n1. Sim\n2. Não, voltar\n3. O que é pedir {tipo_aumento}?\n')
            if resposta == '1':
                print(f'{self.nome} pediu {tipo_aumento}!')

                aceitou_aumento = proximo_jogador.responderAumento(self.nome, tipo_aumento)
                if aceitou_aumento:
                    print(f'{proximo_jogador.nome} aceitou o {tipo_aumento}! A rodada agora vale {pontos} pontos.')
                    
                    carta_jogada = self.jogarCarta(carta_escolhida)
                    if carta_jogada:
                        return carta_jogada, pontos # Retorna a carta jogada para uso posterior
                else:
                    print(f'{proximo_jogador.nome} recusou o {tipo_aumento}. A rodada acabou, e vocês ganharam {pontos_atual} pontos.')
                    self.equipe.adicionarPonto(pontos_atual)
                    return pontos_atual
            elif resposta == '2':
                break
            elif resposta == '3':
                if tipo_aumento == 'Truco':
                    print(f'Pedir Truco é desafiar a equipe adversária a jogar a rodada atual valendo 3 pontos ao invés de 1, caso você esteja confiante de que pode vencê-la.')
                elif tipo_aumento == 'Seis':
                    print(f'Pedir Seis é desafiar a equipe adversária a jogar a rodada atual valendo 6 pontos ao invés de 3.')
                elif tipo_aumento == 'Nove':
                    print(f'Pedir Nove é desafiar a equipe adversária a jogar a rodada atual valendo 9 pontos ao invés de 6.')
                elif tipo_aumento == 'Doze':
                    print(f'Pedir Doze é desafiar a equipe adversária a jogar a rodada atual valendo 12 pontos ao invés de 9.')
    
    def responderAumento(self, nome_desafiante, tipo_aumento):
        resposta = input(f'\n{self.nome}, {nome_desafiante} está pedindo {tipo_aumento}! Aceitar? (s/n): ')
        if resposta.lower() == 's':
            return True # Aceitou o aumento
        else:
            return False # Recusou o aumento
    
    def pedirFamilia(self, baralho):
        if baralho is None:
            print(f'Erro: o baralho não foi passado corretamente.')
        
        while True:
            escolha_familia = input(f'\nGostaria de pedir Família?\n1. Sim\n2. Não\n3. O que é pedir Família?\nInsira sua escolha: ')
            if escolha_familia == '1':
                print(f'\n{self.nome} pediu Família.')
                mao_descartada = self.mao[:]
                self.mao.clear()
                self.receberCartas(baralho.distribuirCartas(3))
                print(f'Sua nova mão: {self.mostrarMao()}')
                return mao_descartada # Retorna a mão descartada para ser registrada na rodada
            elif escolha_familia == '2':
                break
            elif escolha_familia == '3':
                print(f'Pedir família é solicitar uma nova mão para você, caso perceba que sua mão atual está fraca. As cartas que constituem uma Família são Q, J, K e A.\nAo pedir família, a equipe adversária pode optar por abrir sua mão descartada para conferir se de fato era uma família. Se for verdade, sua equipe ganha 1 ponto. Se não for, a equipe adversária ganha 1 ponto.\nNo máximo 3 famílias podem ser solicitadas antes de o jogo começar, e todos os jogadores podem pedir quantas famílias quiserem até atingir esse limite.')
            else:
                print('Opção inválida. Tente novamente.')
                pass
    
    def verificarFamilias(self, maos_descartadas, equipes): # Interface do jogador para verificar famílias
        jogadores_descartaram = [
                (jogador, mao) for jogador, mao in maos_descartadas if jogador.equipe != self.equipe
            ]

        if not jogadores_descartaram:
            print('Não há mãos para verificar.') # ORIGINALMENTE 'Nenhuma família foi pedida pela equipe adversária'
            return None
        
        while jogadores_descartaram:
            print(f'\nA equipe adversária pediu {len(jogadores_descartaram)} família(s):')
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
                    print(f'A mão descartada pelo {jogador_escolhido.nome} foi removida das opções.')
                else:
                    print(f'ERRO: A mão de {jogador_escolhido.nome} já foi removida ou não está mais disponível.')
            elif escolha == str(len(jogadores_descartaram) + 1):
                break # Volta para o menu principal
            else:
                print('Opção inválida. Tente novamente.')

    def verificarFamilia(self, jogador_verificado, mao_descartada, equipes): # Função que verifica se uma mão descartada é família
        familias = {'Q', 'J', 'K', 'A'}

        print(f'Mão descartada por {jogador_verificado.nome}: {mao_descartada}')

        if all(carta.valor in familias for carta in mao_descartada):
            print(f'A mão descartada por {jogador_verificado.nome} era uma família! A {jogador_verificado.equipe.nome} ganhou 1 ponto.')
            equipes[jogador_verificado.equipe.nome].adicionarPonto(1)
            return True
        else:
            print(f'A mão descartada por {jogador_verificado.nome} ({jogador_verificado.equipe.nome}) não era uma família! Sua equipe ({self.equipe}) ganhou 1 ponto.')
            equipes[self.equipe.nome].adicionarPonto(1)
            return False
    
    def pedirDesistencia(self, pontos_da_rodada):
        print(f'Você pediu para desistir dessa rodada.')
        return self.equipe.registrarPedidoDesistencia(self, pontos_da_rodada)
    
    def confirmarDesistencia(self):
        resposta = input(f'{self.nome}, seu companheiro quer desistir dessa rodada. Confirmar desistência? (s/n): ')
        if resposta.lower() == 's':
            print(f'Você aceitou o pedido de desistência.')
            return True # Aceitou a Desistência
        else:
            print(f'Você recusou o pedido de desistência.')
            return False # Recusou a Desistência

    def jogarCarta(self, carta_escolhida=None):
        while True:  
            qtd_cartas = len(self.mao)  
            if qtd_cartas == 0:  
                print("Você não tem cartas para jogar.")  
                return None
            
            print(f'Você tem {qtd_cartas} carta(s) em sua mão')
            
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

                print(f'{i}. Pedir Família')
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
                return self.pedirFamilia(baralho)
            
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