# Relatório de Decisões de Limpeza e Qualidade de Dados

Este documento registra de forma transparente e reprodutível o diagnóstico, as verificações de qualidade e as decisões de tratamento aplicadas ao dataset do World Happiness Report 2019 (`2019.csv`), em conformidade com as diretrizes do projeto SYNAPTA 2026.

---

## 1. Dimensões do Dataset

- **Antes da Limpeza**: 156 linhas (países) e 9 colunas (variáveis).
- **Depois da Limpeza**: 156 linhas (países) e 9 colunas (variáveis).
- **Registros Removidos**: 0 registros.

---

## 2. Tabela de Checagens de Diagnóstico e Ações Tomadas

| Verificação | Resultado Real do Diagnóstico | Ação Tomada | Justificativa Analítica |
| :--- | :--- | :--- | :--- |
| **Valores Ausentes** | 0 valores ausentes encontrados | Nenhuma (ou remoção se aplicável) | Nenhum valor ausente detectado; preservou-se 100% da amostra. |
| **Linhas Duplicadas** | 0 linhas duplicadas | Nenhuma | Nenhuma linha duplicada na base original. |
| **Países Duplicados** | 0 ocorrências | Nenhuma | Cada país possui registro único. |
| **Espaços nos Nomes** | 0 países com espaços extras | Nenhuma | Nomes de países já estavam limpos. |
| **Pontuação Inválida** | 0 fora de [0, 10] | Nenhuma | Todos os valores de pontuação respeitam a escala oficial de 0 a 10. |
| **Fatores Negativos** | 0 valores negativos | Nenhuma | Nenhum fator socioeconômico apresentou valor menor que zero. |
| **Empates de Pontuação** | 2 países compartilham pontuação idêntica | Nenhuma | Empates são legítimos; a checagem de ranking usa ordenação estável para não depender da ordem arbitrária entre eles. |
| **Coerência de Ranking** | Coerente: True | Nenhuma | O ranking oficial é consistente com a ordenação decrescente do score (empates mantêm a ordem do arquivo). |

---

## 3. Mapeamento de Colunas (Inglês -> Português snake_case)

Para padronizar o código e atender às normas do projeto, as colunas originais foram renomeadas conforme o dicionário `MAPA_COLUNAS`:

| Coluna Original (Kaggle) | Coluna Renomeada (`snake_case`) |
| :--- | :--- |
| `"Overall rank"` | `"ranking"` |
| `"Country or region"` | `"pais"` |
| `"Score"` | `"pontuacao"` |
| `"GDP per capita"` | `"pib_per_capita"` |
| `"Social support"` | `"apoio_social"` |
| `"Healthy life expectancy"` | `"expectativa_vida_saudavel"` |
| `"Freedom to make life choices"` | `"liberdade"` |
| `"Generosity"` | `"generosidade"` |
| `"Perceptions of corruption"` | `"percepcao_corrupcao"` |

