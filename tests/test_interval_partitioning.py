import unittest
from datetime import time

from atividade import Atividade
from interval_partitioning import alocar_salas
from pico_simultaneidade import calcular_pico_simultaneidade

def atividade(id: str, inicio: str, fim: str) -> Atividade:
    h1, m1 = map(int, inicio.split(":"))
    h2, m2 = map(int, fim.split(":"))
    return Atividade(id, f"Atividade {id}", time(h1, m1), time(h2, m2))

class IntervalPartitioningTest(unittest.TestCase):
    def assertSemConflitos(self, salas):
        for sala in salas:
            for anterior, atual in zip(sala.atividades, sala.atividades[1:]):
                self.assertLessEqual(anterior.fim, atual.inicio)

    def test_sem_sobreposicao(self):
        atividades = [
            atividade("1", "08:00", "09:00"),
            atividade("2", "09:30", "10:30"),
            atividade("3", "11:00", "12:00"),
        ]

        salas = alocar_salas(atividades)

        self.assertEqual(1, len(salas))
        self.assertEqual(1, calcular_pico_simultaneidade(atividades))

    def test_sobreposicao_total(self):
        atividades = [atividade(str(i), "08:00", "10:00") for i in range(1, 5)]

        salas = alocar_salas(atividades)

        self.assertEqual(4, len(salas))
        self.assertEqual(4, calcular_pico_simultaneidade(atividades))
        self.assertSemConflitos(salas)

    def test_sobreposicao_parcial(self):
        atividades = [
            atividade("1", "08:00", "10:00"),
            atividade("2", "08:30", "10:30"),
            atividade("3", "09:00", "11:00"),
            atividade("4", "10:00", "12:00"),
            atividade("5", "11:00", "13:00"),
        ]

        salas = alocar_salas(atividades)

        self.assertEqual(calcular_pico_simultaneidade(atividades), len(salas))
        self.assertSemConflitos(salas)

    def test_fronteira_reutiliza_sala(self):
        atividades = [
            atividade("1", "08:00", "10:00"),
            atividade("2", "10:00", "12:00"),
        ]

        salas = alocar_salas(atividades)

        self.assertEqual(1, len(salas))
        self.assertEqual(["1", "2"], [a.id for a in salas[0].atividades])

    def test_uma_atividade(self):
        atividades = [atividade("1", "08:00", "10:00")]

        self.assertEqual(1, len(alocar_salas(atividades)))
        self.assertEqual(1, calcular_pico_simultaneidade(atividades))

    def test_sem_atividades(self):
        self.assertEqual([], alocar_salas([]))
        self.assertEqual(0, calcular_pico_simultaneidade([]))

    def test_entrada_fora_de_ordem(self):
        atividades = [
            atividade("1", "10:00", "11:00"),
            atividade("2", "08:00", "10:00"),
        ]

        salas = alocar_salas(atividades)

        self.assertEqual(1, len(salas))
        self.assertEqual(["2", "1"], [a.id for a in salas[0].atividades])

if __name__ == "__main__":
    unittest.main()
