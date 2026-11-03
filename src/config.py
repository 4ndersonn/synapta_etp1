"""
Módulo de configuração centralizada do projeto.
Define caminhos utilizando pathlib e constantes globais.
"""

from pathlib import Path

# Raiz do projeto (diretório pai de src/)
RAIZ: Path = Path(__file__).resolve().parent.parent

# Diretórios de dados e artefatos
DIR_RAW: Path = RAIZ / "data" / "raw"
DIR_PROCESSED: Path = RAIZ / "data" / "processed"
DIR_IMAGES: Path = RAIZ / "images"
DIR_OUTPUTS: Path = RAIZ / "outputs"
DIR_TABLES: Path = DIR_OUTPUTS / "tables"
DIR_DOCS: Path = RAIZ / "docs"

# Identificadores e metadados do dataset
IDENTIFICADOR_DATASET: str = "unsdsn/world-happiness"
NOME_ARQUIVO_DADOS: str = "2019.csv"

# Dicionário de mapeamento de colunas (vazio, a ser preenchido na Etapa 2)
MAPA_COLUNAS: dict = {
    "Overall rank": "ranking",
    "Country or region": "pais",
    "Score": "pontuacao",
    "GDP per capita": "pib_per_capita",
    "Social support": "apoio_social",
    "Healthy life expectancy": "expectativa_vida_saudavel",
    "Freedom to make life choices": "liberdade",
    "Generosity": "generosidade",
    "Perceptions of corruption": "percepcao_corrupcao",
}


def garantir_pastas() -> None:
    """
    Garante que todos os diretórios de saída e dados essenciais existam no sistema de arquivos.
    Caso não existam, cria os diretórios recursivamente.
    """
    diretorios = [DIR_RAW, DIR_PROCESSED, DIR_IMAGES, DIR_OUTPUTS, DIR_TABLES, DIR_DOCS]
    for diretorio in diretorios:
        diretorio.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    garantir_pastas()
    print("Pastas verificadas e criadas com sucesso.")
