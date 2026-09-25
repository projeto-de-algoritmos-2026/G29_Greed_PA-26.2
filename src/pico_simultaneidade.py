from atividade import Atividade

def calcular_pico_simultaneidade(atividades: list[Atividade]) -> int:
    eventos = []

    for atividade in atividades:
        eventos.append((atividade.inicio, 1))
        eventos.append((atividade.fim, -1))

    eventos.sort()

    atividades_ativas = 0
    pico = 0

    for _, variacao in eventos:
        atividades_ativas += variacao
        pico = max(pico, atividades_ativas)

    return pico