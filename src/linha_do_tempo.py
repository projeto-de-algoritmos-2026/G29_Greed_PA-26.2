from sala import Sala

def gerar_linha_do_tempo(salas: list[Sala]) -> str:
    linhas = []

    for sala in salas:
        intervalos = [
            f"{a.inicio.strftime('%H:%M')}-{a.fim.strftime('%H:%M')} {a.nome}"
            for a in sala.atividades
        ]
        linhas.append(f"Sala {sala.id} | " + " | ".join(intervalos))

    return "\n".join(linhas)
