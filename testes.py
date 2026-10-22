"""Testes de correção e do ponto de troca entre os algoritmos."""

import random
import unittest
from unittest.mock import patch

import ordenacao


class TestOrdenacao(unittest.TestCase):
    def test_resultado_em_entradas_variadas(self):
        gerador = random.Random(123)
        entradas = [
            [], [7], [4, 4, 4, 4], [3, -1, 3, 0, -1],
            list(range(100)), list(range(99, -1, -1)),
            [gerador.randrange(100) for _ in range(100)],
        ]
        for entrada in entradas:
            for corte in (1, 5, 16, 200):
                with self.subTest(entrada=entrada[:5], corte=corte):
                    valores = entrada.copy()
                    ordenacao.quicksort_hibrida(valores, corte, seed=42)
                    self.assertEqual(valores, sorted(entrada))
            valores = entrada.copy()
            ordenacao.quicksort_pura(valores, seed=42)
            self.assertEqual(valores, sorted(entrada))

    def test_corte_1_nunca_chama_insercao(self):
        with patch.object(ordenacao, "insertion_sort", wraps=ordenacao.insertion_sort) as insercao:
            valores = [5, 3, 1, 4, 2]
            ordenacao.quicksort_hibrida(valores, corte=1, seed=7)
            self.assertEqual(valores, [1, 2, 3, 4, 5])
            insercao.assert_not_called()

    def test_trecho_menor_que_corte_usa_insercao(self):
        with patch.object(ordenacao, "insertion_sort", wraps=ordenacao.insertion_sort) as insercao:
            valores = [4, 2, 3, 1]
            ordenacao.quicksort_hibrida(valores, corte=5, seed=7)
            self.assertEqual(valores, [1, 2, 3, 4])
            insercao.assert_called_once_with(valores, 0, 3)

    def test_corte_deve_ser_inteiro_positivo(self):
        for corte in (0, -1, 2.5, "16", True):
            with self.subTest(corte=corte), self.assertRaises(ValueError):
                ordenacao.quicksort_hibrida([2, 1], corte)


if __name__ == "__main__":
    unittest.main(verbosity=2)
