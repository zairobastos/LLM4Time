"""
Módulo para salvamento de dados de séries temporais.

Este módulo fornece funcionalidades para salvar DataFrames processados
em arquivos CSV, facilitando a persistência de dados após processamento
e análise de séries temporais.
"""

import pandas as pd


def save(df: pd.DataFrame, path: str) -> None:
  """
  Salva um DataFrame em arquivo CSV.

  Exporta o DataFrame fornecido para um arquivo CSV no caminho especificado,
  sem incluir o índice do DataFrame no arquivo de saída.

  Args:
      df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
      path (str): Caminho onde o arquivo CSV será salvo, incluindo nome
                  e extensão do arquivo.

  Examples:
      >>> df = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'],
      ...                    'value': [10.5, 12.3]})
      >>> save(df, "dados_processados.csv")
      # Arquivo salvo em dados_processados.csv

      >>> # Salvando em diretório específico
      >>> save(df, "output/serie_temporal_limpa.csv")
      # Arquivo salvo em output/serie_temporal_limpa.csv
  """
  df.to_csv(path, index=False)
