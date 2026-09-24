import csv

from datetime import datetime, time
from pathlib import Path
from atividade import Atividade

COLUNAS_OBRIGATORIAS = ("id", "nome", "inicio", "fim")

class ErroValidacaoCSV(ValueError):
    def __init__(self, erros: list[str]):
        self.erros = erros
        super().__init__("\n".join(erros))

def converter_horario(horario: str) -> time:
    return datetime.strptime(horario.strip(), "%H:%M").time()

def ler_atividades_csv(caminho: str | Path) -> list[Atividade]:
    atividades = []
    ids_encontrados = set()
    erros = []

    with open(caminho, mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.reader(arquivo)

        try:
            cabecalho = [coluna.strip() for coluna in next(leitor)]
        except StopIteration:
            raise ErroValidacaoCSV(["O arquivo CSV está vazio."])

        colunas_ausentes = [
            coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in cabecalho
        ]
        if colunas_ausentes:
            raise ErroValidacaoCSV(
                [
                    "Colunas obrigatórias ausentes: "
                    + ", ".join(colunas_ausentes)
                    + "."
                ]
            )

        for numero_linha, valores in enumerate(leitor, start=2):
            if len(valores) != len(cabecalho):
                erros.append(
                    f"Linha {numero_linha}: esperados {len(cabecalho)} campos, "
                    f"mas foram encontrados {len(valores)}."
                )
                continue

            linha = dict(zip(cabecalho, valores))
            id_atividade = linha["id"].strip()
            nome = linha["nome"].strip()
            inicio_texto = linha["inicio"].strip()
            fim_texto = linha["fim"].strip()
            erros_linha = []

            if not id_atividade:
                erros_linha.append(f"Linha {numero_linha}: o ID não pode estar vazio.")
            elif id_atividade in ids_encontrados:
                erros_linha.append(
                    f"Linha {numero_linha}: o ID '{id_atividade}' está duplicado."
                )
            else:
                ids_encontrados.add(id_atividade)

            if not nome:
                erros_linha.append(
                    f"Linha {numero_linha}: o nome não pode estar vazio."
                )

            inicio = None
            fim = None

            try:
                inicio = converter_horario(inicio_texto)
            except ValueError:
                erros_linha.append(
                    f"Linha {numero_linha}: o início '{inicio_texto}' "
                    "deve estar no formato HH:MM."
                )

            try:
                fim = converter_horario(fim_texto)
            except ValueError:
                erros_linha.append(
                    f"Linha {numero_linha}: o fim '{fim_texto}' "
                    "deve estar no formato HH:MM."
                )

            if inicio is not None and fim is not None and inicio >= fim:
                erros_linha.append(
                    f"Linha {numero_linha}: o início deve ser anterior ao fim."
                )

            if erros_linha:
                erros.extend(erros_linha)
                continue

            atividades.append(Atividade(id_atividade, nome, inicio, fim))

    if erros:
        raise ErroValidacaoCSV(erros)

    return atividades