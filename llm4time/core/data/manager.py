"""
Módulo para gerenciamento de dados de séries temporais.

Este módulo fornece funcionalidades para salvar DataFrames processados
em diferentes formatos, facilitando a persistência de dados após o
processamento e análise de séries temporais.
"""

import os
import pandas as pd
from llm4time.core.logging import logger


def save(df: pd.DataFrame, path: str) -> None:
  """
  Salva um DataFrame em arquivo, identificando automaticamente o formato.

  Suporta os seguintes formatos: CSV, XLSX, JSON, Parquet.

  Args:
      df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
      path (str): Caminho completo incluindo nome e extensão do arquivo.

  Examples:
      >>> df = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'],
      ...                    'value': [10.5, 12.3]})
      >>> save(df, "etth2.csv")
      # Arquivo salvo em etth2.csv
  """
  try:
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".csv":
      df.to_csv(path, index=False)
    elif ext in ".xlsx":
      df.to_excel(path, index=False)
    elif ext == ".json":
      df.to_json(path, orient="records", date_format="iso")
    elif ext == ".parquet":
      df.to_parquet(path, index=False)
    else:
      logger.error(f"Extensão de arquivo não suportada: {ext}")
      return

    logger.info(f"Arquivo salvo em {path}")

  except Exception as e:
    logger.error(f"Falha ao salvar arquivo: {e}")
