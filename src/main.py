import sys

from leitor_csv import ErroValidacaoCSV, ler_atividades_csv

def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <arquivo.csv>")
        return 1

    try:
        atividades = ler_atividades_csv(sys.argv[1])
    except ErroValidacaoCSV as erro:
        print("Nao foi possivel ler o arquivo:")
        for mensagem in erro.erros:
            print(f"- {mensagem}")
        return 1
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {sys.argv[1]}")
        return 1
    except OSError as erro:
        print(f"Nao foi possivel abrir o arquivo: {erro}")
        return 1

    for atividade in atividades:
        inicio = atividade.inicio.strftime("%H:%M")
        fim = atividade.fim.strftime("%H:%M")
        print(f"{atividade.id} - {atividade.nome}: {inicio} - {fim}")

    return 0

if __name__ == "__main__":
    sys.exit(main())