"""
Módulo para carregamento de dados de séries temporais.

Este módulo fornece funcionalidades para carregar e processar dados de séries
temporais.
"""

import os
import pandas as pd
from llm4time.core.logging import logger


def load_data(path: str) -> pd.DataFrame | None:
  """
  Carrega dados de séries temporais a partir de um arquivo.

  Esta função identifica a extensão do arquivo e utiliza a função de leitura
  apropriada do pandas. Formatos suportados: CSV, XLSX, JSON, Parquet.

  Args:
      path (str): Caminho para o arquivo a ser carregado.

  Returns:
      pd.DataFrame | None: DataFrame contendo os dados carregados ou None em caso de erro.

  Examples:
      >>> df = load_data("etth2.csv")
  """
  try:
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext in [".csv", ".txt"]:
      df = pd.read_csv(path)
    elif ext in [".xlsx", ".xls"]:
      df = pd.read_excel(path)
    elif ext == ".json":
      df = pd.read_json(path)
    elif ext == ".parquet":
      df = pd.read_parquet(path)
    else:
      logger.error(f"Extensão de arquivo não suportada: {ext}")
      return None

    return df

  except FileNotFoundError as e:
    logger.error(f"Arquivo não encontrado: {e}")
    return None
  except pd.errors.EmptyDataError as e:
    logger.error(f"Arquivo vazio: {e}")
    return None
  except Exception as e:
    logger.error(f"Ocorreu um erro inesperado: {e}")
    return None
