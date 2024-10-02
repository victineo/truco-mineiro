import pytest
from jogo import Jogo
from baralho import Baralho
from jogador import Jogador
from rodada import Rodada
from subrodada import Subrodada
from carta import Carta

@pytest.fixture
def setup_jogo():
    """Fixture para configurar o ambiente do jogo."""
    jogo = Jogo(['Jogador 1', 'Jogador 2', 'Jogador 3', 'Jogador 4'])
    rodada = Rodada(jogo.jogadores, jogo.equipes, jogo.baralho)
    return jogo, rodada

def simular_subrodada(rodada, cartas_jogadas):
    """Função auxiliar para simular as cartas jogadas na subrodada."""
    subrodada = Subrodada(rodada.jogadores, rodada.equipes)
    
    for idx, carta in enumerate(cartas_jogadas):
        jogador = rodada.jogadores[idx]
        subrodada.cartas_jogadas.append({
            'jogador': jogador.nome,
            'carta': carta,
            'equipe': jogador.equipe
        })
    
    return subrodada.determinarVencedor()

def test_rodada_empate(setup_jogo):
    jogo, rodada = setup_jogo

    # Simular a primeira subrodada: Equipe A vence
    cartas_primeira = [
        Carta('4', 'Copas'),   # Jogador 1
        Carta('7', 'Ouros'),   # Jogador 2 (Sete de Ouros - Manilha)
        Carta('3', 'Espadas'), # Jogador 3
        Carta('5', 'Copas')    # Jogador 4
    ]
    vencedor_primeira = simular_subrodada(rodada, cartas_primeira)
    assert vencedor_primeira == 'Equipe A'  # Equipe A vence

    # Simular a segunda subrodada: Equipe B vence
    cartas_segunda = [
        Carta('Q', 'Ouros'),   # Jogador 1 (Equipe B)
        Carta('6', 'Paus'),    # Jogador 2 (Equipe A)
        Carta('Q', 'Copas'),   # Jogador 3 (Equipe B)
        Carta('3', 'Ouros')    # Jogador 4 (Equipe A)
    ]
    vencedor_segunda = simular_subrodada(rodada, cartas_segunda)
    assert vencedor_segunda == 'Equipe B'  # Equipe B vence

    # Simular a terceira subrodada: Empate
    cartas_terceira = [
        Carta('A', 'Espadas'), # Jogador 1 (Equipe B)
        Carta('A', 'Paus'),    # Jogador 2 (Equipe A)
        Carta('A', 'Copas'),   # Jogador 3 (Equipe B)
        Carta('A', 'Ouros')    # Jogador 4 (Equipe A)
    ]
    vencedor_terceira = simular_subrodada(rodada, cartas_terceira)
    assert vencedor_terceira is None  # Deve resultar em empate

    # Simular o fim da rodada: Como houve uma vitória para cada equipe e um empate, a rodada deve terminar empatada.
    rodada_resultado, pontos = rodada.realizarRodada()
    assert rodada_resultado is None  # A rodada termina sem vencedor
    assert pontos == 0  # Nenhum ponto deve ser concedido