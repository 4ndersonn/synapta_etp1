# Catálogo de Legendas dos Gráficos

Este documento apresenta a listagem de todos os gráficos gerados para a análise do World Happiness Report 2019. Todos os números abaixo são lidos das tabelas em `outputs/tables/`.

---

| Arquivo | Título do Gráfico | Descrição Analítica Baseada em Dados |
| :--- | :--- | :--- |
| **`01_distribuicao_pontuacao.png`** | Distribuição da Pontuação de Felicidade | Histograma com curva de densidade dos 156 países, com média (5.41) e mediana (5.38) muito próximas, sugerindo simetria. |
| **`02_top10_bottom10.png`** | 10 Países com Menor e 10 com Maior Pontuação | Comparação entre os extremos da distribuição, com Finland (7.77) no topo e South Sudan (2.85) na base. |
| **`03_pib_vs_felicidade.png`** | Associação entre PIB per capita e Pontuação | Dispersão com linha de tendência linear indicando associação positiva forte entre PIB per capita e pontuação (r = 0.79). |
| **`04_apoio_social_vs_felicidade.png`** | Associação entre Apoio Social e Pontuação | Dispersão com linha de ajuste linear indicando associação positiva forte entre apoio social e pontuação (r = 0.78). |
| **`05_matriz_correlacao.png`** | Matriz de Correlação de Pearson | Heatmap triangular com as correlações entre a pontuação e os seis fatores. A maior correlação entre dois fatores é `pib_per_capita` x `expectativa_vida_saudavel` (r = 0.84). |
| **`06_fatores_por_quartil.png`** | Média dos Fatores por Quartil de Pontuação | Barras agrupadas com a média de cada fator em cada quartil de pontuação. Maioria dos fatores cresce do Q1 ao Q4, exceto `generosidade`, `percepcao_corrupcao`, que não crescem de forma contínua. |

---
*Catálogo gerado automaticamente pelo script `src/03_graficos.py`.*
