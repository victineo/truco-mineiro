class Carta():
    valores = {
        '4': 1,
        '5': 2,
        '6': 3,
        '7': 4,
        'Q': 5,
        'J': 6,
        'K': 7,
        'A': 8,
        '2': 9,
        '3': 10
    }

    naipes = {
        'Ouros',
        'Espadas',
        'Copas',
        'Paus',
    }

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        self.manilha = None

        if valor == '4' and naipe == 'Paus':
            self.manilha = ('Zap', 14)
        elif valor == '7' and naipe == 'Copas':
            self.manilha = ('Sete de Copas', 13)
        elif self.valor == 'A' and naipe == 'Espadas':
            self.manilha = ('Espadilha', 12)
        elif valor == '7' and naipe == 'Ouros':
            self.manilha = ('Sete de Ouros', 11)

    def __repr__(self):
        if self.manilha:
            return f'{self.valor} de {self.naipe} ({self.manilha[0]})'
        else:
            return f'{self.valor} de {self.naipe}'