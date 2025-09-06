"""
Módulo para carregamento de dados de séries temporais.

Este módulo fornece funcionalidades para carregar e processar dados de séries
temporais.
"""

import pandas as pd
from llm4time.core.logging import logger
from .preprocessor import select_columns


def load_data(
    path: str,
    date_col: str,
    value_col: str,
    duplicates: str | None = "first"
) -> pd.DataFrame | None:
  """
  Carrega dados de séries temporais a partir de um arquivo CSV.

  Esta função lê um arquivo CSV e seleciona as colunas especificadas para análise
  de séries temporais, aplicando tratamento de duplicatas conforme necessário.

  Args:
      path (str): Caminho para o arquivo CSV a ser carregado.
      date_col (str): Nome da coluna que contém as datas/timestamps.
      value_col (str): Nome da coluna que contém os valores da série temporal.
      duplicates (str | None): Como tratar dados duplicados:
        "first" → mantém a primeira ocorrência.
        "last" → mantém a última ocorrência.
        "sum" → soma os valores duplicados.
        None → não remove duplicatas.

  Returns:
      pd.DataFrame | None: DataFrame contendo os dados processados com as colunas selecionadas, ou None em caso de erro no carregamento.

  Examples:
      >>> df = load_data(
      ...     path="etth2.csv",
      ...     date_col="date",
      ...     value_col="OT",
      ...     duplicates="first"
      ... )
  """
  try:
    df = pd.read_csv(path)
    df = select_columns(df, date_col, value_col, duplicates)
    return df
  except FileNotFoundError as e:
    logger.error(f"Arquivo não encontrado: {e}")
    return None
  except pd.errors.EmptyDataError as e:
    logger.error(f"Arquivo vazio: {e}")
    return None
  except Exception as e:
    logger.error(f"Ocorreu um erro inesperado: {e}")
