# Instruções do Dataset

Este diretório armazena os dados utilizados na análise do World Happiness Report.

## Origem dos Dados
- **Dataset no Kaggle**: [World Happiness Report](https://www.kaggle.com/datasets/unsdsn/world-happiness)
- **Arquivo Utilizado**: `2019.csv`

## Instruções de Posicionamento
Por motivos de licença e boas práticas de versionamento (conforme as regras do repositório), os dados brutos (`data/raw/`) e processados (`data/processed/`) **não** são versionados no Git.

Para executar os scripts de análise com sucesso:
1. Acesse o link do Kaggle acima e baixe o dataset World Happiness Report.
2. Extraia o arquivo `2019.csv` e coloque-o dentro da pasta `data/raw/` (`data/raw/2019.csv`).
3. Alternativamente, os scripts de ingestão/análise podem utilizar o pacote `kagglehub` para o download automatizado, caso configurado.
