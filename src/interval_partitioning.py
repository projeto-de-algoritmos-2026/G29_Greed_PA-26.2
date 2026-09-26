import heapq

from atividade import Atividade
from sala import Sala

def alocar_salas(atividades: list[Atividade]) -> list[Sala]:
    salas = []
    # heap com (horario em que a sala fica livre, id da sala)
    heap = []

    for atividade in sorted(atividades, key=lambda atividade: atividade.inicio):
        if heap and heap[0][0] <= atividade.inicio:
            _, id_sala = heapq.heappop(heap)
            sala = salas[id_sala - 1]
        else:
            sala = Sala(len(salas) + 1)
            salas.append(sala)

        sala.alocar(atividade)
        heapq.heappush(heap, (sala.livre_a_partir, sala.id))

    return salas
