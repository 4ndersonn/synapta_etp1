"""
Script de ingestão, diagnóstico, limpeza e validação do World Happiness Report 2019.
Este script funciona de forma isolada, gerando relatórios de diagnóstico e a base limpa.
"""

import shutil
from pathlib import Path
import pandas as pd
import numpy as np

from config import (
    DIR_RAW,
    DIR_PROCESSED,
    DIR_DOCS,
    IDENTIFICADOR_DATASET,
    NOME_ARQUIVO_DADOS,
    MAPA_COLUNAS,
    garantir_pastas,
)


def baixar_dataset() -> Path:
    """
    Realiza o download do dataset do World Happiness Report via kagglehub
    e copia o arquivo 2019.csv para o diretório de dados brutos (data/raw/).
    Caso o arquivo já exista em data/raw/, o download é ignorado por eficiência.
    Se ocorrer falha, orienta o usuário sobre o download manual conforme o data/README.md.
    """
    garantir_pastas()
    caminho_arquivo_destino = DIR_RAW / NOME_ARQUIVO_DADOS

    print("[INFO] Verificando arquivo de dados brutos...")
    if caminho_arquivo_destino.exists():
        print(f"[SUCESSO] Arquivo já existe em: {caminho_arquivo_destino}")
        return caminho_arquivo_destino

    print(f"[INFO] Arquivo não encontrado localmente. Baixando dataset '{IDENTIFICADOR_DATASET}' via kagglehub...")
    try:
        # O import fica aqui dentro de propósito: se o CSV já está em data/raw/, o script
        # não precisa do kagglehub instalado. Assim a ausência da biblioteca só atrapalha
        # quando o download realmente é necessário.
        import kagglehub

        caminho_dataset_baixado = Path(kagglehub.dataset_download(IDENTIFICADOR_DATASET))
        print(f"[INFO] Dataset baixado em cache temporário: {caminho_dataset_baixado}")

        # Buscar pelo arquivo 2019.csv no diretório baixado
        arquivos_encontrados = list(caminho_dataset_baixado.glob(f"**/{NOME_ARQUIVO_DADOS}"))
        if not arquivos_encontrados:
            raise FileNotFoundError(f"O arquivo {NOME_ARQUIVO_DADOS} não foi encontrado no dataset baixado.")

        caminho_origem = arquivos_encontrados[0]
        shutil.copy(caminho_origem, caminho_arquivo_destino)
        print(f"[SUCESSO] Arquivo {NOME_ARQUIVO_DADOS} copiado para {caminho_arquivo_destino}")

    except Exception as erro:
        mensagem_erro = (
            f"[ERRO CRÍTICO] Falha ao baixar o dataset automaticamente via kagglehub: {erro}\n"
            f"Por favor, siga as instruções em 'data/README.md' para baixar o arquivo '{NOME_ARQUIVO_DADOS}' "
            f"diretamente do Kaggle ({IDENTIFICADOR_DATASET}) e posicione-o em '{caminho_arquivo_destino}'."
        )
        print(mensagem_erro)
        raise SystemExit(1)

    return caminho_arquivo_destino


def diagnosticar_dados(caminho_csv: Path) -> dict:
    """
    Executa o diagnóstico completo da qualidade dos dados brutos sem alterá-los.
    Mede dimensões, tipos, ausentes, duplicados, valores fora de faixa e coerência do ranking.
    Retorna um dicionário com os resultados para uso na documentação.
    """
    print("\n[INÍCIO] Etapa de Diagnóstico de Qualidade dos Dados")
    df = pd.read_csv(caminho_csv)

    # 1. Dimensões
    total_linhas, total_colunas = df.shape
    print(f" - Dimensões do dataset: {total_linhas} linhas (países) e {total_colunas} colunas (variáveis).")

    # 2. Tipos de dados
    print(" - Tipos de dados por coluna:")
    print(df.dtypes)

    # 3. Valores ausentes
    ausentes_por_coluna = df.isnull().sum()
    total_ausentes = ausentes_por_coluna.sum()
    print(f" - Total de valores ausentes no dataset: {total_ausentes}")
    if total_ausentes > 0:
        print(ausentes_por_coluna[ausentes_por_coluna > 0])

    # 4. Duplicatas
    duplicados_linhas = df.duplicated().sum()
    duplicados_paises = df["Country or region"].duplicated().sum()
    print(f" - Linhas totalmente duplicadas: {duplicados_linhas}")
    print(f" - Países duplicados: {duplicados_paises}")

    # 5. Espaços extras em nomes de países
    paises_com_espacos = df["Country or region"].str.contains(r"^\s+|\s+$").sum()
    print(f" - Países com espaços extras nas extremidades: {paises_com_espacos}")

    coluna_ranking = "Overall rank"
    coluna_pontuacao = "Score"

    # 6. Valores fora de faixa plausível
    # Pontuação happiness de 0 a 10
    pontuacao_invalida = df[~df[coluna_pontuacao].between(0, 10)].shape[0]
    print(f" - Registros com pontuação fora do intervalo [0, 10]: {pontuacao_invalida}")

    # Fatores numéricos (GDP, Social support, etc.) não devem ser negativos
    colunas_fatores = [
        "GDP per capita",
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices",
        "Generosity",
        "Perceptions of corruption",
    ]
    fatores_negativos = 0
    for col in colunas_fatores:
        if col in df.columns:
            negativos = (df[col] < 0).sum()
            fatores_negativos += negativos
            if negativos > 0:
                print(f"   * Coluna '{col}' possui {negativos} valores negativos.")
    print(f" - Total de valores negativos em fatores socioeconômicos: {fatores_negativos}")

    # 7. Coerência do ranking
    # O ranking deve ser único e coincidir com a ordem decrescente da pontuação
    ranking_duplicado = df[coluna_ranking].duplicated().sum()
    # POR QUÊ kind="stable": quando dois países empatam na pontuação (ex.: Marrocos e Azerbaijão,
    # ambos com 5.208), o algoritmo padrão do pandas (quicksort) NÃO garante manter a ordem original
    # entre eles. Isso fazia a checagem dar False em algumas máquinas, mesmo com o ranking correto.
    # A ordenação estável preserva a ordem do arquivo nos empates e torna o resultado determinístico.
    df_ordenado = df.sort_values(by=coluna_pontuacao, ascending=False, kind="stable").reset_index(drop=True)
    ranking_ordenado_correto = (df_ordenado[coluna_ranking].values == np.arange(1, len(df) + 1)).all()
    # Países que compartilham exatamente a mesma pontuação (explica por que a ordem entre eles é arbitrária)
    paises_empatados = int(df[coluna_pontuacao].duplicated(keep=False).sum())
    print(f" - Rankings duplicados: {ranking_duplicado}")
    print(f" - Países com pontuação empatada (mesmo score): {paises_empatados}")
    print(f" - Ranking estritamente coerente com a pontuação decrescente: {ranking_ordenado_correto}")

    # 8. Colunas numéricas lidas como texto (object)
    colunas_nao_numericas = df.select_dtypes(include=["object"]).columns.tolist()
    # Apenas 'Country or region' é esperada como string
    colunas_numericas_como_texto = [c for c in colunas_nao_numericas if c != "Country or region"]
    print(f" - Colunas não numéricas além do país: {colunas_numericas_como_texto}")

    print("[FIM] Diagnóstico concluído com sucesso.\n")

    return {
        "total_linhas": total_linhas,
        "total_colunas": total_colunas,
        "total_ausentes": total_ausentes,
        "duplicados_linhas": int(duplicados_linhas),
        "duplicados_paises": int(duplicados_paises),
        "paises_com_espacos": int(paises_com_espacos),
        "pontuacao_invalida": int(pontuacao_invalida),
        "fatores_negativos": int(fatores_negativos),
        "ranking_duplicado": int(ranking_duplicado),
        "ranking_ordenado_correto": bool(ranking_ordenado_correto),
        "paises_empatados": paises_empatados,
        "colunas_numericas_como_texto": colunas_numericas_como_texto,
    }


def tratar_dados(caminho_csv: Path, resultado_diagnostico: dict) -> pd.DataFrame:
    """
    Executa o tratamento dos dados com base nos achados do diagnóstico:
    - Remove duplicados se existirem.
    - Aplica strip nos nomes dos países.
    - Renomeia colunas para snake_case em português conforme MAPA_COLUNAS.
    - Se nenhum problema crítico for encontrado, preserva a integridade sem invenções.
    Retorna o DataFrame limpo.
    """
    print("[INÍCIO] Etapa de Tratamento e Limpeza dos Dados")
    df = pd.read_csv(caminho_csv)

    linhas_antes = len(df)

    # 1. Tratamento de duplicatas
    if resultado_diagnostico["duplicados_linhas"] > 0:
        df = df.drop_duplicates()
        print(f" - Removidas {linhas_antes - len(df)} linhas totalmente duplicadas.")
    else:
        print(" - Nenhuma linha duplicada encontrada; nenhuma remoção necessária.")

    # 2. Tratamento de espaços nos nomes dos países
    if resultado_diagnostico["paises_com_espacos"] > 0:
        df["Country or region"] = df["Country or region"].str.strip()
        print(f" - Aplicado .str.strip() em {resultado_diagnostico['paises_com_espacos']} nomes de países.")
    else:
        print(" - Nomes de países já limpos de espaços extras nas extremidades.")

    # 3. Tratamento de valores ausentes
    if resultado_diagnostico["total_ausentes"] > 0:
        # Decisão defensiva: como é uma análise exploratória descritiva sem imputação preditiva complexa,
        # ausências em métricas socioeconômicas invalidam a comparabilidade daquele país no ranking.
        # Documentamos e removemos registros afetados se houver.
        df = df.dropna()
        print(f" - Removidos registros com valores ausentes. Linhas afetadas: {linhas_antes - len(df)}")
    else:
        print(" - Nenhum valor ausente encontrado; nenhuma imputação ou remoção por ausência necessária.")

    # 4. Renomeação de colunas para snake_case em português
    df = df.rename(columns=MAPA_COLUNAS)
    print(" - Colunas renomeadas para português (snake_case) com sucesso.")

    # Salvar versão limpa em data/processed/
    caminho_saida = DIR_PROCESSED / "happiness_2019_limpo.csv"
    df.to_csv(caminho_saida, index=False, encoding="utf-8")
    print(f"[SUCESSO] Dataset limpo salvo em: {caminho_saida}")

    print("[FIM] Tratamento concluído.\n")
    return df


def validar_dados(df: pd.DataFrame) -> None:
    """
    Executa asserções rigorosas para garantir a qualidade final do dataset limpo:
    - Sem valores ausentes.
    - Sem linhas duplicadas.
    - Tipos numéricos corretos nas variáveis analíticas.
    - Pontuação estritamente entre 0 e 10.
    """
    print("[INÍCIO] Etapa de Validação Final (Asserts)")

    # 1. Sem valores ausentes
    assert df.isnull().sum().sum() == 0, "Erro de validação: O dataset limpo contém valores ausentes."

    # 2. Sem duplicatas
    assert df.duplicated().sum() == 0, "Erro de validação: O dataset limpo contém linhas duplicadas."
    assert df["pais"].duplicated().sum() == 0, "Erro de validação: Há países duplicados no dataset limpo."

    # 3. Tipos numéricos corretos
    colunas_numericas = [
        "ranking",
        "pontuacao",
        "pib_per_capita",
        "apoio_social",
        "expectativa_vida_saudavel",
        "liberdade",
        "generosidade",
        "percepcao_corrupcao",
    ]
    for col in colunas_numericas:
        assert pd.api.types.is_numeric_dtype(df[col]), f"Erro de validação: A coluna '{col}' não é numérica."

    # 4. Pontuação entre 0 e 10
    assert df["pontuacao"].between(0, 10).all(), "Erro de validação: Há pontuações fora do intervalo [0, 10]."

    print("[SUCESSO] Todas as validações (asserts) passaram com êxito!")
    print("[FIM] Validação concluída.\n")


def gerar_documentacao_limpeza(resultado_diag: dict, linhas_depois: int) -> Path:
    """
    Gera automaticamente o arquivo docs/decisoes_de_limpeza.md em português,
    contendo dimensões antes e depois, tabela de checagens com resultados reais,
    ações tomadas, justificativas e o mapeamento de colunas.
    """
    print("[INÍCIO] Gerando documentação de decisões de limpeza em docs/decisoes_de_limpeza.md...")
    garantir_pastas()
    caminho_doc = DIR_DOCS / "decisoes_de_limpeza.md"

    linhas_antes = resultado_diag["total_linhas"]
    colunas_antes = resultado_diag["total_colunas"]

    conteudo_md = f"""# Relatório de Decisões de Limpeza e Qualidade de Dados

Este documento registra de forma transparente e reprodutível o diagnóstico, as verificações de qualidade e as decisões de tratamento aplicadas ao dataset do World Happiness Report 2019 (`2019.csv`), em conformidade com as diretrizes do projeto SYNAPTA 2026.

---

## 1. Dimensões do Dataset

- **Antes da Limpeza**: {linhas_antes} linhas (países) e {colunas_antes} colunas (variáveis).
- **Depois da Limpeza**: {linhas_depois} linhas (países) e {colunas_antes} colunas (variáveis).
- **Registros Removidos**: {linhas_antes - linhas_depois} registros.

---

## 2. Tabela de Checagens de Diagnóstico e Ações Tomadas

| Verificação | Resultado Real do Diagnóstico | Ação Tomada | Justificativa Analítica |
| :--- | :--- | :--- | :--- |
| **Valores Ausentes** | {resultado_diag['total_ausentes']} valores ausentes encontrados | {'Nenhuma (ou remoção se aplicável)' if resultado_diag['total_ausentes'] == 0 else 'Remoção de registros afetados'} | { 'Nenhum valor ausente detectado; preservou-se 100% da amostra.' if resultado_diag['total_ausentes'] == 0 else 'Imputação arbitrária distorceria métricas de felicidade global.' } |
| **Linhas Duplicadas** | {resultado_diag['duplicados_linhas']} linhas duplicadas | {'Nenhuma' if resultado_diag['duplicados_linhas'] == 0 else 'Remoção de duplicatas'} | { 'Nenhuma linha duplicada na base original.' if resultado_diag['duplicados_linhas'] == 0 else 'Eliminação de redundâncias para evitar viés estatístico.' } |
| **Países Duplicados** | {resultado_diag['duplicados_paises']} ocorrências | {'Nenhuma' if resultado_diag['duplicados_paises'] == 0 else 'Investigação e remoção'} | { 'Cada país possui registro único.' if resultado_diag['duplicados_paises'] == 0 else 'Garantia de chave primária única por país.' } |
| **Espaços nos Nomes** | {resultado_diag['paises_com_espacos']} países com espaços extras | {'Aplicado .str.strip()' if resultado_diag['paises_com_espacos'] > 0 else 'Nenhuma'} | { 'Nomes de países já estavam limpos.' if resultado_diag['paises_com_espacos'] == 0 else 'Padronização de strings para junções e agrupamentos.' } |
| **Pontuação Inválida** | {resultado_diag['pontuacao_invalida']} fora de [0, 10] | Nenhuma | Todos os valores de pontuação respeitam a escala oficial de 0 a 10. |
| **Fatores Negativos** | {resultado_diag['fatores_negativos']} valores negativos | Nenhuma | Nenhum fator socioeconômico apresentou valor menor que zero. |
| **Empates de Pontuação** | {resultado_diag['paises_empatados']} países compartilham pontuação idêntica | Nenhuma | Empates são legítimos; a checagem de ranking usa ordenação estável para não depender da ordem arbitrária entre eles. |
| **Coerência de Ranking** | Coerente: {resultado_diag['ranking_ordenado_correto']} | Nenhuma | { 'O ranking oficial é consistente com a ordenação decrescente do score (empates mantêm a ordem do arquivo).' if resultado_diag['ranking_ordenado_correto'] else 'ATENÇÃO: o ranking do arquivo não coincide com a ordenação por score; revisar a base antes de prosseguir.' } |

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

"""

    caminho_doc.write_text(conteudo_md, encoding="utf-8")
    print(f"[SUCESSO] Documentação gerada em: {caminho_doc}")
    print("[FIM] Documentação concluída.\n")
    return caminho_doc


def executar_pipeline_ingestao() -> None:
    """
    Função principal que orquestra o pipeline completo:
    1. Download / verificação do arquivo bruto.
    2. Diagnóstico da qualidade dos dados.
    3. Tratamento e limpeza com base nos achados.
    4. Validação final via asserts.
    5. Geração automática da documentação em Markdown.
    """
    print("=== INÍCIO DO PIPELINE DE INGESTÃO E LIMPEZA (SYNAPTA 2026) ===")
    
    # Passo 1: Download
    caminho_bruto = baixar_dataset()
    
    # Passo 2: Diagnóstico
    resultado_diagnostico = diagnosticar_dados(caminho_bruto)
    
    # Passo 3: Tratamento
    df_limpo = tratar_dados(caminho_bruto, resultado_diagnostico)
    
    # Passo 4: Validação
    validar_dados(df_limpo)
    
    # Passo 5: Registro / Documentação
    gerar_documentacao_limpeza(resultado_diagnostico, len(df_limpo))
    
    print("=== PIPELINE EXECUTADO COM SUCESSO! ===")


if __name__ == "__main__":
    executar_pipeline_ingestao()
