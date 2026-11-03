"""
Script de geração de visualizações gráficas (plots) para o World Happiness Report 2019.
Lê os dados limpos e tabelas consolidadas, gerando gráficos padronizados em images/
e o catálogo de legendas em outputs/legendas_graficos.md.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") # Garante execução sem interface gráfica (headless)
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    DIR_PROCESSED,
    DIR_TABLES,
    DIR_OUTPUTS,
    DIR_IMAGES,
    garantir_pastas,
)


def configurar_estilo_visual() -> None:
    """
    Configura o tema visual global utilizando seaborn e matplotlib:
    - Tema 'whitegrid'
    - Paleta de cores consistente
    - Tamanhos de fonte legíveis
    """
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 16,
    })


def gerar_grafico_distribuicao_pontuacao(df: pd.DataFrame) -> Path:
    """
    Gera images/01_distribuicao_pontuacao.png:
    Histograma com curva de densidade (KDE) da pontuação de felicidade,
    incluindo linhas verticais tracejadas para a média e a mediana com seus valores na legenda.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "01_distribuicao_pontuacao.png"

    media = df["pontuacao"].mean()
    mediana = df["pontuacao"].median()

    plt.figure(figsize=(10, 6))
    ax = sns.histplot(
        df["pontuacao"],
        kde=True,
        color="steelblue",
        bins=15,
        edgecolor="black",
        alpha=0.6,
    )

    # Linhas verticais para média e mediana
    plt.axvline(
        media,
        color="darkred",
        linestyle="--",
        linewidth=2,
        label=f"Média: {media:.2f}",
    )
    plt.axvline(
        mediana,
        color="darkgreen",
        linestyle=":",
        linewidth=2.5,
        label=f"Mediana: {mediana:.2f}",
    )

    plt.title("Distribuição da Pontuação de Felicidade (World Happiness Report 2019)", pad=15)
    plt.xlabel("Pontuação de Felicidade (Score 0-10)")
    plt.ylabel("Número de Países (Frequência)")
    plt.legend(loc="upper right", frameon=True)
    plt.tight_layout()

    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_grafico_top_bottom(df: pd.DataFrame) -> Path:
    """
    Gera images/02_top10_bottom10.png:
    Gráfico de barras horizontais combinando os 10 países mais felizes e os 10 menos felizes,
    com cores distintas e os valores da pontuação rotulados em cada barra.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "02_top10_bottom10.png"

    df_ordenado = df.sort_values(by="pontuacao", ascending=True)
    top_10 = df_ordenado.tail(10)
    bottom_10 = df_ordenado.head(10)
    df_extremos = pd.concat([bottom_10, top_10])

    fig, ax = plt.subplots(figsize=(12, 8))

    # Cores distintas para Bottom 10 (coral) e Top 10 (teal/forest)
    cores = ["indianred"] * 10 + ["seagreen"] * 10

    barras = ax.barh(
        df_extremos["pais"],
        df_extremos["pontuacao"],
        color=cores,
        edgecolor="black",
        alpha=0.85,
    )

    # Rotular valores em cada barra
    for barra in barras:
        largura = barra.get_width()
        ax.text(
            largura + 0.1,
            barra.get_y() + barra.get_height() / 2,
            f"{largura:.2f}",
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title("10 Países com Menor (Vermelho) e 10 com Maior (Verde) Pontuação de Felicidade", pad=15)
    ax.set_xlabel("Pontuação de Felicidade (Score)")
    ax.set_ylabel("País")
    ax.set_xlim(0, 9.5)

    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_grafico_dispersao_pib(df: pd.DataFrame) -> Path:
    """
    Gera images/03_pib_vs_felicidade.png:
    Dispersão de pib_per_capita vs pontuacao, com linha de tendência linear (regplot)
    e coeficiente de Pearson lido de outputs/tables/correlacoes_pontuacao.csv.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "03_pib_vs_felicidade.png"

    # Ler correlação do CSV gerado na etapa anterior para garantir consistência
    caminho_corr = DIR_TABLES / "correlacoes_pontuacao.csv"
    if caminho_corr.exists():
        df_corr = pd.read_csv(caminho_corr)
        r_pib = df_corr.loc[df_corr["fator"] == "pib_per_capita", "correlacao_pearson"].values[0]
    else:
        r_pib = df["pontuacao"].corr(df["pib_per_capita"], method="pearson")

    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df,
        x="pib_per_capita",
        y="pontuacao",
        color="royalblue",
        scatter_kws={"alpha": 0.7, "s": 50},
        line_kws={"color": "darkred", "linewidth": 2},
    )

    plt.title(f"Associação entre PIB per capita e Pontuação de Felicidade (r = {r_pib:.4f})", pad=15)
    plt.xlabel("PIB per capita (contribuição na escala do WHR)")
    plt.ylabel("Pontuação de Felicidade (Score)")
    plt.tight_layout()

    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_grafico_dispersao_apoio(df: pd.DataFrame) -> Path:
    """
    Gera images/04_apoio_social_vs_felicidade.png:
    Dispersão de apoio_social vs pontuacao, com linha de tendência linear (regplot)
    e coeficiente de Pearson lido de outputs/tables/correlacoes_pontuacao.csv.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "04_apoio_social_vs_felicidade.png"

    caminho_corr = DIR_TABLES / "correlacoes_pontuacao.csv"
    if caminho_corr.exists():
        df_corr = pd.read_csv(caminho_corr)
        r_apoio = df_corr.loc[df_corr["fator"] == "apoio_social", "correlacao_pearson"].values[0]
    else:
        r_apoio = df["pontuacao"].corr(df["apoio_social"], method="pearson")

    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df,
        x="apoio_social",
        y="pontuacao",
        color="darkcyan",
        scatter_kws={"alpha": 0.7, "s": 50},
        line_kws={"color": "darkred", "linewidth": 2},
    )

    plt.title(f"Associação entre Apoio Social e Pontuação de Felicidade (r = {r_apoio:.4f})", pad=15)
    plt.xlabel("Apoio Social (contribuição na escala do WHR)")
    plt.ylabel("Pontuação de Felicidade (Score)")
    plt.tight_layout()

    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_grafico_matriz_correlacao() -> Path:
    """
    Gera images/05_matriz_correlacao.png:
    Heatmap anotado da matriz de correlação (excluindo a coluna ranking),
    com paleta divergente centrada em zero e máscara no triângulo superior.
    Lê a matriz de outputs/tables/matriz_correlacao.csv.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "05_matriz_correlacao.png"
    caminho_matriz = DIR_TABLES / "matriz_correlacao.csv"

    if not caminho_matriz.exists():
        raise FileNotFoundError(f"Matriz de correlação não encontrada em {caminho_matriz}. Execute src/02_analises.py primeiro.")

    matriz = pd.read_csv(caminho_matriz, index_col=0)
    # Excluir a coluna/linha 'ranking' se presente para foco nas variáveis analíticas
    if "ranking" in matriz.columns:
        matriz = matriz.drop(index=["ranking"], columns=["ranking"])

    # POR QUÊ cortar a primeira linha e a última coluna: numa matriz simétrica, o triângulo inferior
    # já contém todos os pares únicos. Sem o corte, sobrava uma linha e uma coluna totalmente vazias.
    matriz_triangular = matriz.iloc[1:, :-1]
    # k=1 mantém a diagonal visível (onde ficam os pares únicos da borda do triângulo)
    mask = np.triu(np.ones_like(matriz_triangular, dtype=bool), k=1)

    plt.figure(figsize=(10, 8))

    # Estilo "white" apenas neste gráfico: a grade do tema whitegrid aparecia por cima das células mascaradas
    with sns.axes_style("white"):
        sns.heatmap(
            matriz_triangular,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )

    plt.title("Matriz de Correlação de Pearson entre Variáveis Numéricas", pad=15)
    plt.tight_layout()

    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_grafico_fatores_por_quartil() -> Path:
    """
    Gera images/06_fatores_por_quartil.png:
    Gráfico de barras agrupadas com a média de cada fator por quartil de pontuação,
    lido de outputs/tables/fatores_por_quartil.csv.
    """
    garantir_pastas()
    caminho_saida = DIR_IMAGES / "06_fatores_por_quartil.png"
    caminho_quartis = DIR_TABLES / "fatores_por_quartil.csv"

    if not caminho_quartis.exists():
        raise FileNotFoundError(f"Arquivo de quartis não encontrado em {caminho_quartis}. Execute src/02_analises.py primeiro.")

    df_quartis = pd.read_csv(caminho_quartis)

    # Preparar dados em formato longo (melt) para barras agrupadas no seaborn
    fatores = [
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]

    df_longo = df_quartis.melt(
        id_vars=["quartil", "pontuacao"],
        value_vars=fatores,
        var_name="fator",
        value_name="media_fator",
    )

    # Traduzir nomes dos fatores para exibição legível
    traducao_fatores = {
        "pib_per_capita": "PIB per capita",
        "apoio_social": "Apoio Social",
        "expectativa_vida_saudavel": "Expectativa de Vida",
        "liberdade": "Liberdade",
        "generosidade": "Generosidade",
        "percepcao_corrupcao": "Percepção de Corrupção (maior = menos)",
    }
    df_longo["fator_legivel"] = df_longo["fator"].map(traducao_fatores)

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=df_longo,
        x="quartil",
        y="media_fator",
        hue="fator_legivel",
        palette="tab10",
        edgecolor="black",
        alpha=0.85,
    )

    plt.title("Média dos Fatores Socioeconômicos por Quartil de Pontuação de Felicidade", pad=15)
    plt.xlabel("Quartil de Pontuação de Felicidade")
    plt.ylabel("Média da contribuição do fator (escala do WHR)")
    plt.legend(title="Fatores", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[SUCESSO] Gráfico salvo: {caminho_saida}")
    return caminho_saida


def gerar_catalogo_legendas(df: pd.DataFrame) -> Path:
    """
    Gera outputs/legendas_graficos.md com uma linha por gráfico:
    nome do arquivo, título e explicação curta.
    POR QUÊ lê das tabelas: todos os números das legendas vêm de outputs/tables/ (ou do próprio
    dataset limpo), nunca de texto digitado à mão. Assim, se os dados mudarem, as legendas
    acompanham automaticamente e a regra "nunca inventar números" é respeitada.
    """
    garantir_pastas()
    caminho_md = DIR_OUTPUTS / "legendas_graficos.md"

    arquivos_necessarios = [
        "estatisticas_pontuacao.csv",
        "top10.csv",
        "bottom10.csv",
        "correlacoes_pontuacao.csv",
        "fatores_por_quartil.csv",
        "matriz_correlacao.csv",
    ]
    for nome in arquivos_necessarios:
        if not (DIR_TABLES / nome).exists():
            raise FileNotFoundError(f"Tabela {nome} não encontrada em {DIR_TABLES}. Execute src/02_analises.py primeiro.")

    estatisticas = pd.read_csv(DIR_TABLES / "estatisticas_pontuacao.csv").set_index("metrica")["valor"]
    top10 = pd.read_csv(DIR_TABLES / "top10.csv")
    bottom10 = pd.read_csv(DIR_TABLES / "bottom10.csv")
    correlacoes = pd.read_csv(DIR_TABLES / "correlacoes_pontuacao.csv").set_index("fator")["correlacao_pearson"]
    quartis = pd.read_csv(DIR_TABLES / "fatores_por_quartil.csv")
    matriz = pd.read_csv(DIR_TABLES / "matriz_correlacao.csv", index_col=0)

    total_paises = len(df)
    media = estatisticas["Media"]
    mediana = estatisticas["Mediana"]

    pais_topo, nota_topo = top10.iloc[0]["pais"], top10.iloc[0]["pontuacao"]
    pais_base, nota_base = bottom10.iloc[0]["pais"], bottom10.iloc[0]["pontuacao"]

    # Maior correlação entre dois FATORES (excluindo pontuação e ranking), calculada a partir da matriz
    fatores = [
        "pib_per_capita", "apoio_social", "expectativa_vida_saudavel",
        "liberdade", "generosidade", "percepcao_corrupcao",
    ]
    matriz_fatores = matriz.loc[fatores, fatores]
    maior_par, maior_corr = None, -2.0
    for i, f1 in enumerate(fatores):
        for f2 in fatores[i + 1:]:
            if matriz_fatores.loc[f1, f2] > maior_corr:
                maior_par, maior_corr = (f1, f2), matriz_fatores.loc[f1, f2]

    # Fatores que NÃO crescem de forma contínua de Q1 a Q4 (para não afirmar crescimento falso)
    nao_monotonicos = [f for f in fatores if not quartis[f].is_monotonic_increasing]
    if nao_monotonicos:
        texto_quartis = (
            "Maioria dos fatores cresce do Q1 ao Q4, exceto "
            + ", ".join(f"`{f}`" for f in nao_monotonicos)
            + ", que não crescem de forma contínua."
        )
    else:
        texto_quartis = "Todos os fatores crescem de forma contínua do Q1 ao Q4."

    conteudo = f"""# Catálogo de Legendas dos Gráficos

Este documento apresenta a listagem de todos os gráficos gerados para a análise do World Happiness Report 2019. Todos os números abaixo são lidos das tabelas em `outputs/tables/`.

---

| Arquivo | Título do Gráfico | Descrição Analítica Baseada em Dados |
| :--- | :--- | :--- |
| **`01_distribuicao_pontuacao.png`** | Distribuição da Pontuação de Felicidade | Histograma com curva de densidade dos {total_paises} países, com média ({media:.2f}) e mediana ({mediana:.2f}) muito próximas, sugerindo simetria. |
| **`02_top10_bottom10.png`** | 10 Países com Menor e 10 com Maior Pontuação | Comparação entre os extremos da distribuição, com {pais_topo} ({nota_topo:.2f}) no topo e {pais_base} ({nota_base:.2f}) na base. |
| **`03_pib_vs_felicidade.png`** | Associação entre PIB per capita e Pontuação | Dispersão com linha de tendência linear indicando associação positiva forte entre PIB per capita e pontuação (r = {correlacoes['pib_per_capita']:.2f}). |
| **`04_apoio_social_vs_felicidade.png`** | Associação entre Apoio Social e Pontuação | Dispersão com linha de ajuste linear indicando associação positiva forte entre apoio social e pontuação (r = {correlacoes['apoio_social']:.2f}). |
| **`05_matriz_correlacao.png`** | Matriz de Correlação de Pearson | Heatmap triangular com as correlações entre a pontuação e os seis fatores. A maior correlação entre dois fatores é `{maior_par[0]}` x `{maior_par[1]}` (r = {maior_corr:.2f}). |
| **`06_fatores_por_quartil.png`** | Média dos Fatores por Quartil de Pontuação | Barras agrupadas com a média de cada fator em cada quartil de pontuação. {texto_quartis} |

---
*Catálogo gerado automaticamente pelo script `src/03_graficos.py`.*
"""

    caminho_md.write_text(conteudo, encoding="utf-8")
    print(f"[SUCESSO] Catálogo de legendas gerado em: {caminho_md}")
    return caminho_md


def executar_pipeline_graficos() -> None:
    """
    Orquestra a execução da geração de todos os gráficos obrigatórios
    e do catálogo de legendas em Markdown.
    """
    print("=== INÍCIO DO PIPELINE DE GERAÇÃO DE GRÁFICOS (SYNAPTA 2026) ===")

    caminho_csv = DIR_PROCESSED / "happiness_2019_limpo.csv"
    if not caminho_csv.exists():
        raise FileNotFoundError(f"Dataset limpo não encontrado em {caminho_csv}. Execute src/01_ingestao_limpeza.py primeiro.")

    df = pd.read_csv(caminho_csv)
    configurar_estilo_visual()

    gerar_grafico_distribuicao_pontuacao(df)
    gerar_grafico_top_bottom(df)
    gerar_grafico_dispersao_pib(df)
    gerar_grafico_dispersao_apoio(df)
    gerar_grafico_matriz_correlacao()
    gerar_grafico_fatores_por_quartil()
    gerar_catalogo_legendas(df)

    print("=== PIPELINE DE GRÁFICOS EXECUTADO COM SUCESSO! ===")


if __name__ == "__main__":
    executar_pipeline_graficos()
