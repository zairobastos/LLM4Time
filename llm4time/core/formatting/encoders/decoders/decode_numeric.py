import numpy as np
import pandas as pd
from ...normalizers import denormalize_missing


def decode_numeric(data: list[float | tuple]) -> list[float | tuple]:
  """
  Converte valores normalizados (com 'nan') de volta para floats, substituindo ausentes por np.nan.

  Se os elementos da lista forem tuplas ou listas, apenas o segundo elemento (valor) é considerado.
  Todos os valores são convertidos em float; valores ausentes são convertidos para np.nan.

  Args:
      data (list[float | tuple]): Lista de valores ou tuplas (date, value) com valores possivelmente normalizados.

  Returns:
      list[float]: Lista de floats, com valores ausentes representados por np.nan.

  Examples:
      >>> decode_numeric([10, 'nan', 5.0, 'nan'])
      [10.0, nan, 5.0, nan]
      >>> decode_numeric([("2025-01-01", 10), ("2025-01-02", 'nan')])
      [10.0, nan]
  """
  if data and isinstance(data[0], (tuple, list)):
    data = [denormalize_missing(v) for _, v in data]
  else:
    data = [denormalize_missing(v) for v in data]
  return [float(v) if not pd.isna(v) else np.nan for v in data]
