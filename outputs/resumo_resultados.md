# Resumo de Resultados - World Happiness Report 2019

Este documento compila os principais indicadores estatísticos e achados analíticos extraídos do dataset de 2019, servindo como base factual para a elaboração do relatório final e do `README.md`.

---

## 1. Estatísticas Descritivas da Pontuação de Felicidade

- **Total de países/regiões analisados**: 156
- **Média**: 5.4071
- **Mediana**: 5.3795
- **Desvio Padrão**: 1.1131
- **Mínimo**: 2.8530
- **Máximo**: 7.7690
- **Diferença (Média - Mediana)**: 0.0276

> **Nota sobre a Distribuição**: A proximidade entre a média e a mediana (diferença de apenas 0.0276) indica uma distribuição relativamente simétrica da pontuação de felicidade entre os países analisados, sem forte assimetria ou desvio acentuado provocado por valores extremos.

---

## 2. Países nos Extremos do Ranking

- **País com Maior Pontuação (Top 1)**: Finland (Score: 7.7690)
- **País com Menor Pontuação (Bottom 1)**: South Sudan (Score: 2.8530)

### 5 Países com Maior Pontuação
| Ranking | País | Pontuação |
| :---: | :--- | :---: |
| 1 | Finland | 7.7690 |
| 2 | Denmark | 7.6000 |
| 3 | Norway | 7.5540 |
| 4 | Iceland | 7.4940 |
| 5 | Netherlands | 7.4880 |

### 5 Países com Menor Pontuação (do menor para o maior)
| Ranking | País | Pontuação |
| :---: | :--- | :---: |
| 156 | South Sudan | 2.8530 |
| 155 | Central African Republic | 3.0830 |
| 154 | Afghanistan | 3.2030 |
| 153 | Tanzania | 3.2310 |
| 152 | Rwanda | 3.3340 |

---

## 3. Associação entre Fatores e Pontuação (Correlações de Pearson e Spearman)

A análise de correlação demonstra o grau de associação linear (`Pearson`) e monotônica (`Spearman`) entre os fatores socioeconômicos e a pontuação de felicidade. Nota-se linguagem estritamente de associação (sem inferência causal).

| Fator Socioeconômico | Correlação de Pearson | Correlação de Spearman |
| :--- | :---: | :---: |
| pib_per_capita | 0.7939 | 0.8145 |
| expectativa_vida_saudavel | 0.7799 | 0.8073 |
| apoio_social | 0.7771 | 0.8162 |
| liberdade | 0.5667 | 0.5520 |
| percepcao_corrupcao | 0.3856 | 0.2173 |
| generosidade | 0.0758 | 0.0705 |

- **Fator com maior associação**: `pib_per_capita` (Pearson: 0.7939).
- **Fator com menor associação**: `generosidade` (Pearson: 0.0758).

---

## 4. Comparação entre Grupos (Médias dos Fatores por Quartil de Pontuação)

Dividindo os países em quartis com base na pontuação de felicidade, observa-se como os fatores socioeconômicos acompanham a elevação do nível de felicidade médio de cada grupo:

| Quartil | Pontuação Média | PIB per capita | Apoio Social | Expectativa de Vida | Liberdade | Generosidade | Percepção de Corrupção |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1º Quartil (Q1 - Menor Felicidade) | 4.0051 | 0.4734 | 0.8919 | 0.4651 | 0.2975 | 0.2029 | 0.0974 |
| 2º Quartil (Q2) | 4.9763 | 0.7966 | 1.1343 | 0.6465 | 0.3605 | 0.1680 | 0.0790 |
| 3º Quartil (Q3) | 5.8183 | 1.0405 | 1.3453 | 0.8393 | 0.4180 | 0.1540 | 0.0767 |
| 4º Quartil (Q4 - Maior Felicidade) | 6.8287 | 1.3102 | 1.4638 | 0.9501 | 0.4943 | 0.2144 | 0.1893 |

> **Atenção**: os fatores que **não** crescem de forma contínua de Q1 a Q4 são: `generosidade`, `percepcao_corrupcao`. Para eles, não é correto falar em "crescimento progressivo" com a pontuação.

---

## 5. Nota Metodológica sobre os Fatores

As colunas de fatores do World Happiness Report representam a contribuição estimada de cada componente para a pontuação. A soma dos seis fatores tem correlação de Pearson de **0.8799** com a pontuação (diferença média de 1.8799 entre a pontuação e a soma dos fatores, que no relatório corresponde à referência "Distopia" mais um resíduo). Portanto, parte da associação observada entre cada fator e a pontuação já é esperada pela construção do indicador, e os resultados devem ser lidos como **associação com os componentes do modelo do relatório**, não como evidência causal.

---
*Relatório gerado automaticamente pelo script `src/02_analises.py`.*
