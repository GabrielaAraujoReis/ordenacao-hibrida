"""Mede os algoritmos com a mesma entrada e gera CSV e SVG."""

import argparse
import csv
import random
import statistics
import time
from pathlib import Path

from ordenacao import quicksort_hibrida, quicksort_pura


CORTES = (1, 5, 10, 16, 20, 32, 50, 100, 200)
PASTA = Path(__file__).resolve().parent


def medir(n: int = 20_000, repeticoes: int = 7) -> list[tuple[str, float]]:
    if n < 1 or repeticoes < 1:
        raise ValueError("n e repeticoes devem ser positivos")

    gerador = random.Random(20261022)
    entrada = [gerador.randrange(1_000_000) for _ in range(n)]
    esperado = sorted(entrada)
    configuracoes = [(str(c), c) for c in CORTES] + [("pura", None)]
    amostras = {nome: [] for nome, _ in configuracoes}

    # A ordem muda por repetição, para reduzir a influência de aquecimento/carga.
    for repeticao in range(repeticoes):
        ordem = configuracoes.copy()
        random.Random(9000 + repeticao).shuffle(ordem)
        for nome, corte in ordem:
            valores = entrada.copy()  # A cópia fica fora do tempo medido.
            inicio = time.perf_counter()
            if corte is None:
                quicksort_pura(valores, seed=1000 + repeticao)
            else:
                quicksort_hibrida(valores, corte, seed=1000 + repeticao)
            segundos = time.perf_counter() - inicio
            if valores != esperado:
                raise AssertionError(f"ordenação incorreta em {nome}")
            amostras[nome].append(segundos * 1000)

    return [(nome, statistics.median(amostras[nome])) for nome, _ in configuracoes]


def salvar_csv(resultados: list[tuple[str, float]]) -> None:
    with (PASTA / "resultados_benchmark.csv").open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(("corte", "tempo_mediano_ms"))
        for nome, ms in resultados:
            escritor.writerow((nome, f"{ms:.6f}"))


def salvar_grafico(resultados: list[tuple[str, float]]) -> None:
    pontos = [(int(nome), ms) for nome, ms in resultados if nome != "pura"]
    pura = next(ms for nome, ms in resultados if nome == "pura")
    largura, altura = 760, 450
    esquerda, direita, topo, baixo = 80, 35, 45, 75
    area_x = largura - esquerda - direita
    area_y = altura - topo - baixo
    max_y = max(ms for _, ms in resultados) * 1.15

    def x(corte: int) -> float:
        return esquerda + corte / 200 * area_x

    def y(ms: float) -> float:
        return topo + (1 - ms / max_y) * area_y

    linhas = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="380" y="25" text-anchor="middle" font-family="Arial" font-size="19">Tempo mediano por corte</text>',
        f'<line x1="{esquerda}" y1="{topo}" x2="{esquerda}" y2="{topo+area_y}" stroke="#333"/>',
        f'<line x1="{esquerda}" y1="{topo+area_y}" x2="{esquerda+area_x}" y2="{topo+area_y}" stroke="#333"/>',
    ]
    for i in range(6):
        ms = max_y * i / 5
        yy = y(ms)
        linhas += [
            f'<line x1="{esquerda}" y1="{yy:.2f}" x2="{esquerda+area_x}" y2="{yy:.2f}" stroke="#e6e6e6"/>',
            f'<text x="{esquerda-9}" y="{yy+4:.2f}" text-anchor="end" font-family="Arial" font-size="12">{ms:.1f}</text>',
        ]
    for corte, _ in pontos:
        xx = x(corte)
        linhas += [
            f'<line x1="{xx:.2f}" y1="{topo+area_y}" x2="{xx:.2f}" y2="{topo+area_y+5}" stroke="#333"/>',
            f'<text x="{xx:.2f}" y="{topo+area_y+20}" text-anchor="middle" font-family="Arial" font-size="11">{corte}</text>',
        ]
    linhas += [
        f'<line x1="{esquerda}" y1="{y(pura):.2f}" x2="{esquerda+area_x}" y2="{y(pura):.2f}" stroke="#d97706" stroke-width="2" stroke-dasharray="7 5"/>',
        f'<polyline points="{" ".join(f"{x(c):.2f},{y(ms):.2f}" for c, ms in pontos)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>',
    ]
    for corte, ms in pontos:
        linhas.append(f'<circle cx="{x(corte):.2f}" cy="{y(ms):.2f}" r="4" fill="#2563eb"/>')
    linhas += [
        '<text x="400" y="437" text-anchor="middle" font-family="Arial" font-size="14">Corte (elementos)</text>',
        '<text x="20" y="220" text-anchor="middle" transform="rotate(-90 20 220)" font-family="Arial" font-size="14">Tempo mediano (ms)</text>',
        '<line x1="510" y1="50" x2="540" y2="50" stroke="#2563eb" stroke-width="2.5"/>',
        '<text x="548" y="54" font-family="Arial" font-size="12">Híbrida</text>',
        '<line x1="610" y1="50" x2="640" y2="50" stroke="#d97706" stroke-width="2" stroke-dasharray="7 5"/>',
        '<text x="648" y="54" font-family="Arial" font-size="12">Pura</text>',
        '</svg>',
    ]
    (PASTA / "grafico_cortes.svg").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=20_000)
    parser.add_argument("--repeticoes", type=int, default=7)
    args = parser.parse_args()
    resultados = medir(args.n, args.repeticoes)
    salvar_csv(resultados)
    salvar_grafico(resultados)
    for nome, ms in resultados:
        print(f"{nome:>4}: {ms:.6f} ms")
    melhor = min((par for par in resultados if par[0] != "pura"), key=lambda par: par[1])
    pura = dict(resultados)["pura"]
    ganho = (pura - melhor[1]) / pura * 100
    print(f"Melhor corte: {melhor[0]}; ganho sobre a pura: {ganho:.2f}%")


if __name__ == "__main__":
    main()
