from atividade import Atividade
from sala import Sala

def alocar_salas(atividades: list[Atividade]) -> list[Sala]:
    salas = []

    for atividade in sorted(atividades, key=lambda atividade: atividade.inicio):
        sala = Sala(len(salas) + 1)
        sala.alocar(atividade)
        salas.append(sala)

    return salas
