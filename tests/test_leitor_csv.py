import tempfile
import unittest
from pathlib import Path

from leitor_csv import ErroValidacaoCSV, ler_atividades_csv

class LeitorCSVTest(unittest.TestCase):
    def criar_csv(self, conteudo: str) -> Path:
        diretorio = tempfile.TemporaryDirectory()
        self.addCleanup(diretorio.cleanup)

        caminho = Path(diretorio.name) / "atividades.csv"
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    def test_le_csv_valido(self):
        caminho = self.criar_csv(
            "id,nome,inicio,fim\n"
            "1,EDA2,08:00,09:50\n"
            "2,PA,10:00,11:50\n"
        )

        atividades = ler_atividades_csv(caminho)

        self.assertEqual(2, len(atividades))
        self.assertEqual("1", atividades[0].id)
        self.assertEqual("EDA2", atividades[0].nome)
        self.assertEqual("08:00", atividades[0].inicio.strftime("%H:%M"))
        self.assertEqual("09:50", atividades[0].fim.strftime("%H:%M"))

    def test_rejeita_csv_vazio(self):
        caminho = self.criar_csv("")

        with self.assertRaisesRegex(ErroValidacaoCSV, "arquivo CSV está vazio"):
            ler_atividades_csv(caminho)

    def test_rejeita_coluna_obrigatoria_ausente(self):
        caminho = self.criar_csv("id,nome,inicio\n1,EDA2,08:00\n")

        with self.assertRaisesRegex(ErroValidacaoCSV, "fim"):
            ler_atividades_csv(caminho)

    def test_rejeita_linha_com_quantidade_incorreta_de_campos(self):
        caminho = self.criar_csv(
            "id,nome,inicio,fim\n"
            "3,Redes,08:00\n"
        )

        with self.assertRaisesRegex(
            ErroValidacaoCSV,
            "Linha 2: esperados 4 campos, mas foram encontrados 3",
        ):
            ler_atividades_csv(caminho)

    def test_rejeita_id_vazio(self):
        caminho = self.criar_csv("id,nome,inicio,fim\n,EDA2,08:00,09:50\n")

        with self.assertRaisesRegex(ErroValidacaoCSV, "ID não pode estar vazio"):
            ler_atividades_csv(caminho)

    def test_rejeita_nome_vazio(self):
        caminho = self.criar_csv("id,nome,inicio,fim\n1,,08:00,09:50\n")

        with self.assertRaisesRegex(ErroValidacaoCSV, "nome não pode estar vazio"):
            ler_atividades_csv(caminho)

    def test_rejeita_id_duplicado(self):
        caminho = self.criar_csv(
            "id,nome,inicio,fim\n"
            "1,EDA2,08:00,09:50\n"
            "1,PA,10:00,11:50\n"
        )

        with self.assertRaisesRegex(ErroValidacaoCSV, "ID '1' está duplicado"):
            ler_atividades_csv(caminho)

    def test_rejeita_horario_fora_do_formato(self):
        caminho = self.criar_csv(
            "id,nome,inicio,fim\n"
            "1,EDA2,8 horas,09:50\n"
        )

        with self.assertRaisesRegex(ErroValidacaoCSV, "formato HH:MM"):
            ler_atividades_csv(caminho)

    def test_rejeita_inicio_igual_ao_fim(self):
        caminho = self.criar_csv("id,nome,inicio,fim\n1,EDA2,09:50,09:50\n")

        with self.assertRaisesRegex(
            ErroValidacaoCSV,
            "início deve ser anterior ao fim",
        ):
            ler_atividades_csv(caminho)

    def test_rejeita_inicio_posterior_ao_fim(self):
        caminho = self.criar_csv("id,nome,inicio,fim\n1,EDA2,10:00,09:50\n")

        with self.assertRaisesRegex(
            ErroValidacaoCSV,
            "início deve ser anterior ao fim",
        ):
            ler_atividades_csv(caminho)

if __name__ == "__main__":
    unittest.main()