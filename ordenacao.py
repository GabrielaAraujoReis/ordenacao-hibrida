"""Quick Sort aleatória de três vias e versão híbrida com Insertion Sort."""

import random


def insertion_sort(valores: list[int], inicio: int, fim: int) -> None:
    """Ordena, na própria lista, o intervalo inclusivo [inicio, fim]."""
    for i in range(inicio + 1, fim + 1):
        atual = valores[i]
        j = i - 1
        while j >= inicio and valores[j] > atual:
            valores[j + 1] = valores[j]
            j -= 1
        valores[j + 1] = atual


def quicksort_hibrida(
    valores: list[int], corte: int, seed: int | None = None
) -> None:
    """Usa inserção somente em trechos com tamanho estritamente menor que corte."""
    if not isinstance(corte, int) or isinstance(corte, bool) or corte < 1:
        raise ValueError("corte deve ser um inteiro positivo")

    gerador = random.Random(seed)

    def ordenar(inicio: int, fim: int) -> None:
        while inicio < fim:
            if fim - inicio + 1 < corte:
                insertion_sort(valores, inicio, fim)
                return

            pivo = valores[gerador.randint(inicio, fim)]
            menores = inicio
            atual = inicio
            maiores = fim

            # [inicio, menores): menores; [menores, atual): iguais;
            # (maiores, fim]: maiores. [atual, maiores] ainda não foi examinado.
            while atual <= maiores:
                if valores[atual] < pivo:
                    valores[menores], valores[atual] = valores[atual], valores[menores]
                    menores += 1
                    atual += 1
                elif valores[atual] > pivo:
                    valores[atual], valores[maiores] = valores[maiores], valores[atual]
                    maiores -= 1
                else:
                    atual += 1

            # Recorrer no lado menor limita a profundidade da pilha.
            if menores - inicio < fim - maiores:
                ordenar(inicio, menores - 1)
                inicio = maiores + 1
            else:
                ordenar(maiores + 1, fim)
                fim = menores - 1

    ordenar(0, len(valores) - 1)


def quicksort_pura(valores: list[int], seed: int | None = None) -> None:
    """Mesmo algoritmo, com corte 1: nenhum trecho útil usa inserção."""
    quicksort_hibrida(valores, corte=1, seed=seed)
