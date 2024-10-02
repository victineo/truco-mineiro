class Equipe():
    def __init__(self, nome, jogadores, equipe_adversaria):
        self.nome = nome # Nome atribuído à equipe ('Equipe A', 'Equipe B')
        self.jogadores = jogadores
        self.pediu_desistencia = []
        self.equipe_adversaria = equipe_adversaria # Referência à equipe adversária
        self.pontos = 0 # Equipe inicia sem pontos
    
    def adicionarPonto(self, pontos):
        self.pontos += pontos # Originalmente `self.pontos += 1`

    def obterCompanheiro(self, jogador): # Retorna o companheiro de equipe do jogador
        return [j for j in self.jogadores if j != jogador][0]
    
    def registrarPedidoDesistencia(self, jogador, pontos_da_rodada): # Registra o pedido de desistência de um jogador e verifica a resposta do companheiro
        if self.pediu_desistencia: # Verifica se o jogador já pediu desistência na rodada atual
            print(f'Você já pediu para desistir dessa rodada.')
            return
        
        self.pediu_desistencia = jogador # Registra o jogador que pediu para desistir
        companheiro = self.obterCompanheiro(jogador) # Obtém o companheiro do jogador que pediu desistência

        if companheiro.confirmarDesistencia(): # Pergunta diretamente ao companheiro se ele aceita a desistência
            self.desistir(pontos_da_rodada)
            return True
        else:
            self.pediu_desistencia = None  # Reseta o pedido de desistência
            print(f'Seu companheiro {companheiro.nome} recusou o pedido de desistência.')
            return False
    
    def desistir(self, pontos_da_rodada): # A equipe oficialmente desiste da rodada e o adversário ganha 1 ponto
        print(f'A equipe {self.nome} desistiu da rodada.')
        self.equipe_adversaria.adicionarPonto(pontos_da_rodada)
        if pontos_da_rodada == 1:
            print(f'A equipe adversária ({self.equipe_adversaria.nome}) recebeu {pontos_da_rodada} ponto.')
        else:
            print(f'A equipe adversária ({self.equipe_adversaria.nome}) recebeu {pontos_da_rodada} pontos.')
        self.pediu_desistencia = None