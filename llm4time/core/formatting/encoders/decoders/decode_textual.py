import numpy as np
import pandas as pd
from ...normalizers import denormalize_missing


def decode_textual(data: list[float | tuple]) -> list[float | tuple]:
  """
  Converte uma lista de valores textuais normalizados de volta para floats,
  substituindo valores ausentes ou 'nan' por np.nan.

  Se os elementos da lista forem tuplas ou listas, apenas o segundo elemento (valor) é considerado.
  Remove espaços em strings antes de converter para float.

  Args:
      data (list[float | tuple]): Lista de valores textuais ou tuplas (date, value) possivelmente normalizados.

  Returns:
      list[float]: Lista de floats, com valores ausentes representados por np.nan.

  Examples:
      >>> decode_textual(['10', 'nan', ' 5.0 ', 'nan'])
      [10.0, nan, 5.0, nan]
      >>> decode_textual([("2025-01-01", '10'), ("2025-01-02", 'nan')])
      [10.0, nan]
  """
  if data and isinstance(data[0], (tuple, list)):
    data = [denormalize_missing(v) for _, v in data]
  else:
    data = [denormalize_missing(v) for v in data]
  return [float(str(v).replace(' ', '')) if not pd.isna(v) else np.nan for v in data]
