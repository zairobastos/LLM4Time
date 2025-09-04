from ..normalizers import normalize_missing


def encode_numeric(data: list[float | tuple]) -> list[float | tuple]:
  """
  Normaliza valores ausentes ou NaN em uma lista de valores numéricos ou tuplas (date, value).

  Se os elementos da lista forem tuplas ou listas, apenas o segundo elemento (valor)
  é normalizado usando `normalize_missing`. Caso contrário, cada valor é normalizado diretamente.

  Args:
      data (list[float | tuple]): Lista de valores numéricos ou tuplas (date, value).

  Returns:
      list[float | tuple]: Lista com valores normalizados, onde valores ausentes são substituídos por 'nan'.

  Examples:
      >>> encode_numeric([10, None, 5.0, float('nan')])
      [10, 'nan', 5.0, 'nan']
      >>> encode_numeric([("2025-01-01", 10), ("2025-01-02", None)])
      [('2025-01-01', 10), ('2025-01-02', 'nan')]
  """
  if data and isinstance(data[0], (tuple, list)):
    return [(d, normalize_missing(v)) for d, v in data]
  return [normalize_missing(v) for v in data]
