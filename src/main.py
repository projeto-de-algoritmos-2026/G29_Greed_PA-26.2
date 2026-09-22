import sys

from leitor_csv import ler_atividades_csv

def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <arquivo.csv>")
        return

    atividades = ler_atividades_csv(sys.argv[1])

    for atividade in atividades:
        inicio = atividade.inicio.strftime("%H:%M")
        fim = atividade.fim.strftime("%H:%M")
        print(f"{atividade.id} - {atividade.nome}: {inicio} - {fim}")

if __name__ == "__main__":
    main()
