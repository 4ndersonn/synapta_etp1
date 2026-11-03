"""
Script de análises descritivas, correlações, agrupamentos por quartis e resumo de resultados
do World Happiness Report 2019.
Lê o dataset limpo em data/processed/happiness_2019_limpo.csv e gera tabelas e relatórios.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from config import (
    DIR_PROCESSED,
    DIR_TABLES,
    DIR_OUTPUTS,
    garantir_pastas,
)


def carregar_dados_limpos() -> pd.DataFrame:
    """
    Carrega o dataset limpo de data/processed/happiness_2019_limpo.csv.
    Caso o arquivo não exista, encerra a execução com uma mensagem clara
    orientando o usuário a executar o script src/01_ingestao_limpeza.py primeiro.
    """
    caminho_arquivo = DIR_PROCESSED / "happiness_2019_limpo.csv"
    if not caminho_arquivo.exists():
        mensagem_erro = (
            f"[ERRO CRÍTICO] Arquivo de dados limpos não encontrado em: {caminho_arquivo}\n"
            f"Por favor, execute primeiro o script de ingestão e limpeza:\n"
            f"  python src/01_ingestao_limpeza.py"
        )
        print(mensagem_erro)
        raise SystemExit(1)

    df = pd.read_csv(caminho_arquivo)
    print(f"[SUCESSO] Dados carregados com sucesso de {caminho_arquivo}. Total de registros: {len(df)}")
    return df


def analisar_estatisticas_pontuacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula as estatísticas descritivas da pontuação de felicidade (pontuacao):
    média, mediana, desvio padrão, mínimo, máximo e a diferença entre média e mediana.
    Salva o resultado em outputs/tables/estatisticas_pontuacao.csv e exibe no terminal.
    """
    print("\n[ANÁLISE 1] Estatísticas Descritivas da Pontuação de Felicidade")
    serie_pontuacao = df["pontuacao"]

    media = serie_pontuacao.mean()
    mediana = serie_pontuacao.median()
    desvio_padrao = serie_pontuacao.std()
    minimo = serie_pontuacao.min()
    maximo = serie_pontuacao.max()
    diferenca_media_mediana = media - mediana

    dados_estatisticas = {
        "metrica": [
            "Media",
            "Mediana",
            "Desvio Padrao",
            "Minimo",
            "Maximo",
            "Diferenca (Media - Mediana)",
        ],
        "valor": [
            media,
            mediana,
            desvio_padrao,
            minimo,
            maximo,
            diferenca_media_mediana,
        ],
    }

    df_estatisticas = pd.DataFrame(dados_estatisticas)
    
    garantir_pastas()
    caminho_saida = DIR_TABLES / "estatisticas_pontuacao.csv"
    df_estatisticas.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(df_estatisticas.to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_saida}")

    return df_estatisticas


def analisar_extremos_top_bottom(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifica os 10 países com maior pontuação (Top 10) e os 10 com menor pontuação (Bottom 10),
    incluindo ranking, país, pontuação e os 6 fatores socioeconômicos.
    Salva os resultados em outputs/tables/top10.csv e outputs/tables/bottom10.csv.
    """
    print("\n[ANÁLISE 2] Países nos Extremos (Top 10 e Bottom 10)")

    # O dataset já vem ordenado por ranking, mas garantimos a ordenação correta por pontuação decrescente
    df_ordenado = df.sort_values(by="pontuacao", ascending=False).reset_index(drop=True)

    colunas_interesse = [
        "ranking",
        "pais",
        "pontuacao",
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]

    top_10 = df_ordenado.head(10)[colunas_interesse]
    bottom_10 = df_ordenado.tail(10)[colunas_interesse].sort_values(by="pontuacao", ascending=True)

    garantir_pastas()
    caminho_top10 = DIR_TABLES / "top10.csv"
    caminho_bottom10 = DIR_TABLES / "bottom10.csv"

    top_10.to_csv(caminho_top10, index=False, encoding="utf-8")
    bottom_10.to_csv(caminho_bottom10, index=False, encoding="utf-8")

    print("--- TOP 10 PAÍSES MAIS FELICES ---")
    print(top_10[["ranking", "pais", "pontuacao"]].to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_top10}")

    print("\n--- BOTTOM 10 PAÍSES MENOS FELICES ---")
    print(bottom_10[["ranking", "pais", "pontuacao"]].to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_bottom10}")

    return top_10, bottom_10


def analisar_correlacoes(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calcula as correlações de Pearson e de Spearman entre cada um dos 6 fatores e a pontuação,
    ordenando da mais forte para a mais fraca (com base no valor absoluto de Pearson).
    Salva a tabela de correlações em outputs/tables/correlacoes_pontuacao.csv
    e a matriz de correlação completa em outputs/tables/matriz_correlacao.csv.
    """
    print("\n[ANÁLISE 3] Associação entre Fatores e Pontuação (Correlações)")

    fatores = [
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]

    resultados_correlacao = []
    for fator in fatores:
        corr_pearson = df["pontuacao"].corr(df[fator], method="pearson")
        # Spearman calculado como a correlação de Pearson entre os rankings das variáveis (não requer scipy)
        corr_spearman = df["pontuacao"].rank().corr(df[fator].rank(), method="pearson")
        resultados_correlacao.append(
            {
                "fator": fator,
                "correlacao_pearson": corr_pearson,
                "correlacao_spearman": corr_spearman,
                "abs_pearson": abs(corr_pearson),
            }
        )

    df_correlacoes = pd.DataFrame(resultados_correlacao)
    # Ordenar da mais forte para a mais fraca pelo valor absoluto de Pearson
    df_correlacoes = df_correlacoes.sort_values(by="abs_pearson", ascending=False).drop(columns=["abs_pearson"]).reset_index(drop=True)

    garantir_pastas()
    caminho_corr = DIR_TABLES / "correlacoes_pontuacao.csv"
    df_correlacoes.to_csv(caminho_corr, index=False, encoding="utf-8")

    print("--- CORRELAÇÕES COM A PONTUAÇÃO (ORDENADAS) ---")
    print(df_correlacoes.to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_corr}")

    # Matriz de correlação completa (Pearson) entre todas as variáveis numéricas
    colunas_numericas = ["ranking", "pontuacao"] + fatores
    matriz_pearson = df[colunas_numericas].corr(method="pearson")

    caminho_matriz = DIR_TABLES / "matriz_correlacao.csv"
    matriz_pearson.to_csv(caminho_matriz, encoding="utf-8")
    print(f"[SUCESSO] Matriz de correlação completa salva em: {caminho_matriz}")

    return df_correlacoes, matriz_pearson


def analisar_grupos_quartis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Divide os países em quartis de pontuação usando pd.qcut com rótulos claros
    e calcula a média de cada fator socioeconômico por quartil.
    Salva o resultado em outputs/tables/fatores_por_quartil.csv.
    """
    print("\n[ANÁLISE 4] Comparação entre Grupos (Quartis de Pontuação)")

    rotulos_quartis = [
        "1º Quartil (Q1 - Menor Felicidade)",
        "2º Quartil (Q2)",
        "3º Quartil (Q3)",
        "4º Quartil (Q4 - Maior Felicidade)",
    ]

    # Criar coluna categórica de quartis
    df_analise = df.copy()
    df_analise["quartil"] = pd.qcut(df_analise["pontuacao"], q=4, labels=rotulos_quartis)

    fatores = [
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]

    # Calcular a média da pontuação e dos fatores por quartil
    colunas_agregacao = ["pontuacao"] + fatores
    df_quartis = df_analise.groupby("quartil", observed=False)[colunas_agregacao].mean().reset_index()

    garantir_pastas()
    caminho_quartis = DIR_TABLES / "fatores_por_quartil.csv"
    df_quartis.to_csv(caminho_quartis, index=False, encoding="utf-8")

    print(df_quartis.to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_quartis}")

    return df_quartis


def analisar_soma_fatores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica o quanto a pontuação já é "explicada" pela soma dos seis fatores.
    POR QUÊ: no World Happiness Report, as colunas de fatores representam a contribuição estimada
    de cada componente para a pontuação (o restante vem de uma referência chamada "Distopia" e de
    um resíduo). Logo, parte da correlação entre cada fator e a pontuação é esperada pela própria
    construção do indicador. Medir isso deixa a interpretação honesta e defensável na entrevista.
    Salva o resultado em outputs/tables/soma_fatores_vs_pontuacao.csv.
    """
    print("\n[ANÁLISE 5] Soma dos Fatores vs Pontuação (contexto metodológico)")

    fatores = [
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]

    soma_fatores = df[fatores].sum(axis=1)
    residuo = df["pontuacao"] - soma_fatores
    corr_soma = df["pontuacao"].corr(soma_fatores, method="pearson")

    df_soma = pd.DataFrame(
        {
            "metrica": [
                "Correlacao Pearson (Pontuacao x Soma dos 6 fatores)",
                "Residuo Medio (Pontuacao - Soma)",
                "Residuo Minimo",
                "Residuo Maximo",
            ],
            "valor": [corr_soma, residuo.mean(), residuo.min(), residuo.max()],
        }
    )

    garantir_pastas()
    caminho_saida = DIR_TABLES / "soma_fatores_vs_pontuacao.csv"
    df_soma.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(df_soma.to_string(index=False))
    print(f"[SUCESSO] Salvo em: {caminho_saida}")
    return df_soma


def gerar_resumo_resultados(
    df: pd.DataFrame,
    df_estatisticas: pd.DataFrame,
    top_10: pd.DataFrame,
    bottom_10: pd.DataFrame,
    df_correlacoes: pd.DataFrame,
    df_quartis: pd.DataFrame,
    df_soma: pd.DataFrame,
) -> Path:
    """
    Gera automaticamente o arquivo outputs/resumo_resultados.md em português,
    compilando os principais números extraídos das análises.
    Serve como fonte de verdade para o README, mantendo linguagem de associação.
    """
    print("\n[ANÁLISE 6] Gerando Resumo para Conclusões (outputs/resumo_resultados.md)...")
    garantir_pastas()
    caminho_resumo = DIR_OUTPUTS / "resumo_resultados.md"

    media = df_estatisticas.loc[df_estatisticas["metrica"] == "Media", "valor"].values[0]
    mediana = df_estatisticas.loc[df_estatisticas["metrica"] == "Mediana", "valor"].values[0]
    desvio_padrao = df_estatisticas.loc[df_estatisticas["metrica"] == "Desvio Padrao", "valor"].values[0]
    minimo = df_estatisticas.loc[df_estatisticas["metrica"] == "Minimo", "valor"].values[0]
    maximo = df_estatisticas.loc[df_estatisticas["metrica"] == "Maximo", "valor"].values[0]
    diferenca = df_estatisticas.loc[df_estatisticas["metrica"] == "Diferenca (Media - Mediana)", "valor"].values[0]

    pais_max = top_10.iloc[0]["pais"]
    score_max = top_10.iloc[0]["pontuacao"]
    pais_min = bottom_10.iloc[0]["pais"]
    score_min = bottom_10.iloc[0]["pontuacao"]

    fator_mais_forte = df_correlacoes.iloc[0]["fator"]
    corr_mais_forte = df_correlacoes.iloc[0]["correlacao_pearson"]
    fator_mais_fraco = df_correlacoes.iloc[-1]["fator"]
    corr_mais_fraco = df_correlacoes.iloc[-1]["correlacao_pearson"]

    corr_soma = df_soma.iloc[0]["valor"]
    residuo_medio = df_soma.iloc[1]["valor"]

    # Fatores cuja média NÃO cresce de forma contínua de Q1 a Q4 (calculado, não escrito à mão)
    fatores_quartil = [
        "pib_per_capita", "apoio_social", "expectativa_vida_saudavel",
        "liberdade", "generosidade", "percepcao_corrupcao",
    ]
    fatores_nao_monotonicos = [
        f for f in fatores_quartil if not df_quartis[f].is_monotonic_increasing
    ]
    texto_nao_monotonicos = (
        ", ".join(f"`{f}`" for f in fatores_nao_monotonicos) if fatores_nao_monotonicos else "nenhum"
    )
    total_paises = len(df)

    conteudo_md = f"""# Resumo de Resultados - World Happiness Report 2019

Este documento compila os principais indicadores estatísticos e achados analíticos extraídos do dataset de 2019, servindo como base factual para a elaboração do relatório final e do `README.md`.

---

## 1. Estatísticas Descritivas da Pontuação de Felicidade

- **Total de países/regiões analisados**: {total_paises}
- **Média**: {media:.4f}
- **Mediana**: {mediana:.4f}
- **Desvio Padrão**: {desvio_padrao:.4f}
- **Mínimo**: {minimo:.4f}
- **Máximo**: {maximo:.4f}
- **Diferença (Média - Mediana)**: {diferenca:.4f}

> **Nota sobre a Distribuição**: A proximidade entre a média e a mediana (diferença de apenas {diferenca:.4f}) indica uma distribuição relativamente simétrica da pontuação de felicidade entre os países analisados, sem forte assimetria ou desvio acentuado provocado por valores extremos.

---

## 2. Países nos Extremos do Ranking

- **País com Maior Pontuação (Top 1)**: {pais_max} (Score: {score_max:.4f})
- **País com Menor Pontuação (Bottom 1)**: {pais_min} (Score: {score_min:.4f})

### 5 Países com Maior Pontuação
| Ranking | País | Pontuação |
| :---: | :--- | :---: |
"""

    for _, row in top_10.head(5).iterrows():
        conteudo_md += f"| {int(row['ranking'])} | {row['pais']} | {row['pontuacao']:.4f} |\n"

    conteudo_md += f"""
### 5 Países com Menor Pontuação (do menor para o maior)
| Ranking | País | Pontuação |
| :---: | :--- | :---: |
"""

    for _, row in bottom_10.head(5).iterrows():
        conteudo_md += f"| {int(row['ranking'])} | {row['pais']} | {row['pontuacao']:.4f} |\n"

    conteudo_md += f"""
---

## 3. Associação entre Fatores e Pontuação (Correlações de Pearson e Spearman)

A análise de correlação demonstra o grau de associação linear (`Pearson`) e monotônica (`Spearman`) entre os fatores socioeconômicos e a pontuação de felicidade. Nota-se linguagem estritamente de associação (sem inferência causal).

| Fator Socioeconômico | Correlação de Pearson | Correlação de Spearman |
| :--- | :---: | :---: |
"""

    for _, row in df_correlacoes.iterrows():
        conteudo_md += f"| {row['fator']} | {row['correlacao_pearson']:.4f} | {row['correlacao_spearman']:.4f} |\n"

    conteudo_md += f"""
- **Fator com maior associação**: `{fator_mais_forte}` (Pearson: {corr_mais_forte:.4f}).
- **Fator com menor associação**: `{fator_mais_fraco}` (Pearson: {corr_mais_fraco:.4f}).

---

## 4. Comparação entre Grupos (Médias dos Fatores por Quartil de Pontuação)

Dividindo os países em quartis com base na pontuação de felicidade, observa-se como os fatores socioeconômicos acompanham a elevação do nível de felicidade médio de cada grupo:

| Quartil | Pontuação Média | PIB per capita | Apoio Social | Expectativa de Vida | Liberdade | Generosidade | Percepção de Corrupção |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""

    for _, row in df_quartis.iterrows():
        conteudo_md += (
            f"| {row['quartil']} | {row['pontuacao']:.4f} | {row['pib_per_capita']:.4f} | "
            f"{row['apoio_social']:.4f} | {row['expectativa_vida_saudavel']:.4f} | "
            f"{row['liberdade']:.4f} | {row['generosidade']:.4f} | {row['percepcao_corrupcao']:.4f} |\n"
        )

    conteudo_md += f"""
> **Atenção**: os fatores que **não** crescem de forma contínua de Q1 a Q4 são: {texto_nao_monotonicos}. Para eles, não é correto falar em "crescimento progressivo" com a pontuação.

---

## 5. Nota Metodológica sobre os Fatores

As colunas de fatores do World Happiness Report representam a contribuição estimada de cada componente para a pontuação. A soma dos seis fatores tem correlação de Pearson de **{corr_soma:.4f}** com a pontuação (diferença média de {residuo_medio:.4f} entre a pontuação e a soma dos fatores, que no relatório corresponde à referência "Distopia" mais um resíduo). Portanto, parte da associação observada entre cada fator e a pontuação já é esperada pela construção do indicador, e os resultados devem ser lidos como **associação com os componentes do modelo do relatório**, não como evidência causal.

---
*Relatório gerado automaticamente pelo script `src/02_analises.py`.*
"""

    caminho_resumo.write_text(conteudo_md, encoding="utf-8")
    print(f"[SUCESSO] Resumo de resultados gerado em: {caminho_resumo}")
    return caminho_resumo


def executar_pipeline_analises() -> None:
    """
    Orquestra a execução de todas as análises descritivas, correlações,
    agrupamentos e geração do resumo final.
    """
    print("=== INÍCIO DO PIPELINE DE ANÁLISES (SYNAPTA 2026) ===")
    
    df = carregar_dados_limpos()
    
    df_estatisticas = analisar_estatisticas_pontuacao(df)
    top_10, bottom_10 = analisar_extremos_top_bottom(df)
    df_correlacoes, matriz_pearson = analisar_correlacoes(df)
    df_quartis = analisar_grupos_quartis(df)
    df_soma = analisar_soma_fatores(df)
    
    gerar_resumo_resultados(df, df_estatisticas, top_10, bottom_10, df_correlacoes, df_quartis, df_soma)
    
    print("=== PIPELINE DE ANÁLISES EXECUTADO COM SUCESSO! ===")


if __name__ == "__main__":
    executar_pipeline_analises()
