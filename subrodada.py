from carta import Carta

class Subrodada():
    def __init__(self, jogadores, equipes):
        self.jogadores = jogadores # Lista dos jogadores, na ordem de jogada
        self.equipes = equipes # Equipes são fornecidas pela `Rodada`
        self.cartas_jogadas = []

        for i, jogador in enumerate(self.jogadores):
            jogador.jogador_anterior = self.jogadores[(i - 1) % len(self.jogadores)]
            jogador.proximo_jogador = self.jogadores[(i + 1) % len(self.jogadores)]
    
    def exibirCartasJogadasAte(self):
        print(f'\nCartas jogadas até o momento nesta subrodada:')
        for jogada in self.cartas_jogadas:
            print(f'{jogada['jogador']} ({jogada['equipe']}) jogou {jogada['carta']}')
        
        if not self.cartas_jogadas:
            print(f'Nenhuma carta foi jogada ainda')
            return
        
        carta_vencedora = max(self.cartas_jogadas, key=lambda jogada: (
            jogada['carta'].manilha[1] if isinstance(jogada['carta'], Carta) and jogada['carta'].manilha
            else Carta.valores[jogada['carta'].valor] if isinstance(jogada['carta'], Carta) else 0
        ), default=None)

        if carta_vencedora:
            print(f'\n{carta_vencedora['jogador']} está vencendo a subrodada para a {carta_vencedora['equipe']} com um {carta_vencedora['carta']}!\n')
        else:
            cartas_com_mesmo_valor = [
                jogada for jogada in self.cartas_jogadas
                if (
                    jogada['carta'].manilha and carta_vencedora['carta'].manilha and jogada['carta'].manilha[1] == carta_vencedora['carta'].manilha[1]
                ) or (
                    not jogada['carta'].manilha and not carta_vencedora['carta'].manilha and Carta.valores[jogada['carta'].valor] == Carta.valores[carta_vencedora['carta'].valor]
                )
            ]

            if len(cartas_com_mesmo_valor) > 1 and len({jogada['equipe'] for jogada in cartas_com_mesmo_valor}) > 1:
                jogadores_em_empate = [jogada['jogador'] for jogada in cartas_com_mesmo_valor]
                cartas_em_empate = [jogada['carta'] for jogada in cartas_com_mesmo_valor]

                # Gerar a mensagem de empate no formato sugerido
                if len(jogadores_em_empate) == 2:
                    print(f'\n{jogadores_em_empate[0]} e {jogadores_em_empate[1]} estão empatando essa subrodada com um {cartas_em_empate[0]} e um {cartas_em_empate[1]}!\n')
                else:
                    # Se houver mais de dois jogadores envolvidos no empate
                    jogadores = ' e '.join(jogadores_em_empate[:-1]) + f', {jogadores_em_empate[-1]}'
                    cartas = ' e '.join(map(str, cartas_em_empate[:-1])) + f', {cartas_em_empate[-1]}'
                    print(f'\n{jogadores} estão empatando essa subrodada com {cartas}!\n')

    def exibirCartasJogadas(self): # Mostra as cartas jogadas até o momento e quem jogou
        print("\nCartas jogadas nesta subrodada:")
        for jogada in self.cartas_jogadas:
            print(f"{jogada['jogador']} (Equipe {jogada['equipe']}) jogou {jogada['carta']}")
    
    def determinarVencedor(self): # Determina a carta vencedora da subrodada
        if not self.cartas_jogadas: # Se não houver cartas jogadas, não pode haver um vencedor
            return None
        
        # Encontrar a carta com o maior valor
        carta_vencedora = max(self.cartas_jogadas, key=lambda jogada: (
            jogada['carta'].manilha[1] if jogada['carta'].manilha else Carta.valores[jogada['carta'].valor]
        ))

        # Verificar se houve empate (cartas mais fortes da subrodada com o mesmo valor)
        cartas_com_mesmo_valor = [
            jogada for jogada in self.cartas_jogadas
            if (
                jogada['carta'].manilha and carta_vencedora['carta'].manilha and jogada['carta'].manilha[1] == carta_vencedora['carta'].manilha[1]
            ) or (
                not jogada['carta'].manilha and not carta_vencedora['carta'].manilha and Carta.valores[jogada['carta'].valor] == Carta.valores[carta_vencedora['carta'].valor]
            )
        ]

        if len(cartas_com_mesmo_valor) > 1 and len({jogada['equipe'] for jogada in cartas_com_mesmo_valor}) > 1:
            print(f'\nEmpate detectado!')
            return None

        return carta_vencedora
    
    def realizarSubrodada(self, pontos_da_rodada):
        for jogador in self.jogadores:
            self.exibirCartasJogadasAte() # Exibe as cartas jogadas até o momento antes do próximo jogador

            carta_escolhida = None # Define uma carta inicial nula
            acao_resultado = jogador.exibirMenuAcoes(carta_escolhida, None, pre_rodada=False, pontos_da_rodada=pontos_da_rodada) or jogador.jogarCarta(carta_escolhida)

            if acao_resultado == 'desistencia':
                return 'desistencia', pontos_da_rodada

            if isinstance(acao_resultado, tuple):
                carta_jogada, pontos_atualizados = acao_resultado
                pontos_da_rodada = pontos_atualizados
            else:
                carta_jogada = acao_resultado
            
            if carta_jogada and isinstance(carta_jogada, Carta):
                self.cartas_jogadas.append({
                    'jogador': jogador.nome,
                    'carta': carta_jogada,
                    'equipe': jogador.equipe.nome
                })
            else:
                print(f'ERRO: Carta jogada inválida ou não registrada corretamente para o jogador {jogador.nome}.')
        
        self.exibirCartasJogadas() # Mostra as cartas jogadas

        vencedor = self.determinarVencedor() # Determina o vencedor da subrodada
        return (vencedor['equipe'], pontos_da_rodada) if vencedor else None