# Ordenação híbrida: Quick Sort + Insertion Sort

Atividade de Gabriela de Araújo Reis. A Ordenação Hibrida usa pivô aleatório e partição em três grupos: menores, iguais e maiores. A versão híbrida usa Insertion Sort quando um trecho tem **menos de `corte` elementos**.

## Arquivos

- `ordenacao.py`: algoritmos.
- `testes.py`: testes de correção e da regra do corte.
- `experimento.py`: mede os tempos, grava a tabela e desenha o gráfico.
- `resultados_benchmark.csv`: medições desta execução.
- `grafico_cortes.svg`: tempo em função do corte.
- `RELATORIO.md`: método, resultados e análise.

## Executar

No terminal, dentro da pasta do projeto:

```powershell
python testes.py
python experimento.py
```

Se `python` não funcionar, experimente `py` no lugar. O experimento usa apenas a biblioteca padrão do Python. Ele executa sete repetições por configuração com 20.000 elementos, imprime os resultados e atualiza o CSV e o SVG. Ao repetir, atualize também a tabela e a análise do `RELATORIO.md` com os **seus** números.

As funções de ordenação alteram a lista recebida e retornam `None`. Para preservar a entrada, passe `lista.copy()`.
