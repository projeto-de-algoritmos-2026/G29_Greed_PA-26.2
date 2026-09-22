import csv
from datetime import datetime, time
from pathlib import Path

from atividade import Atividade

def converter_horario(horario: str) -> time:
    return datetime.strptime(horario.strip(), "%H:%M").time()

def ler_atividades_csv(caminho: str | Path) -> list[Atividade]:
    atividades = []

    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            atividade = Atividade(
                id=linha["id"].strip(),
                nome=linha["nome"].strip(),
                inicio=converter_horario(linha["inicio"]),
                fim=converter_horario(linha["fim"]),
            )
            atividades.append(atividade)

    return atividades
