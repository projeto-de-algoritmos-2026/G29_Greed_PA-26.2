import sys

from interval_partitioning import alocar_salas
from leitor_csv import ErroValidacaoCSV, ler_atividades_csv
from linha_do_tempo import gerar_linha_do_tempo
from pico_simultaneidade import calcular_pico_simultaneidade

def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <arquivo_name.csv>")
        return 1

    try:
        atividades = ler_atividades_csv(sys.argv[1])
    except ErroValidacaoCSV as erro:
        print("Não foi possível ler o arquivo:")
        for mensagem in erro.erros:
            print(f"- {mensagem}")
        return 1
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {sys.argv[1]}")
        return 1
    except OSError as erro:
        print(f"Não foi possível abrir o arquivo: {erro}")
        return 1

    salas = alocar_salas(atividades)
    print(f"Quantidade minima de salas: {len(salas)}")

    for sala in salas:
        print(f"\nSala {sala.id}:")
        for atividade in sala.atividades:
            inicio = atividade.inicio.strftime("%H:%M")
            fim = atividade.fim.strftime("%H:%M")
            print(f"  {atividade.id} - {atividade.nome}: {inicio} - {fim}")
    print("\nLinha do tempo:")
    print(gerar_linha_do_tempo(salas))
    print()

    pico = calcular_pico_simultaneidade(atividades)
    print(f"Pico de atividades simultaneas: {pico}")

    # o pico e o minimo de salas que qualquer solucao precisa
    if len(salas) == pico:
        print("Salas = pico, a alocacao e otima.")
    else:
        print(f"Atencao: {len(salas)} salas para um pico de {pico}.")

    return 0

if __name__ == "__main__":
    sys.exit(main())