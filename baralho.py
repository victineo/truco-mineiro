import random
from carta import Carta

class Baralho():
    def __init__(self):
        self.cartas = self.criarBaralho()
        self.embaralhar()
    
    def criarBaralho(self):
        return [Carta(valor, naipe) for valor in Carta.valores for naipe in Carta.naipes]
    
    def embaralhar(self):
        random.shuffle(self.cartas)
    
    def distribuirCartas(self, num_cartas, metodo_distribuicao='descendo'):
        if num_cartas > len(self.cartas):
            return []
        
        if metodo_distribuicao == 'descendo':
            return [self.cartas.pop() for _ in range(num_cartas)] if num_cartas <= len(self.cartas) else []
        elif metodo_distribuicao == 'subindo':
            return [self.cartas.pop(0) for _ in range(num_cartas)] if num_cartas <= len(self.cartas) else []
    
    def resetarBaralho(self):
        self.cartas = self.criarBaralho() # Recria o baralho completo
        self.embaralhar() # Embaralha