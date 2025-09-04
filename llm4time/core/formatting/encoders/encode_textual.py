from ..normalizers import normalize_missing


def encode_textual(data: list[float | tuple]) -> list:
  """
  Converte uma lista de valores numéricos ou tuplas (date, value) em uma representação textual,
  normalizando valores ausentes ou NaN.

  Cada valor é convertido em string, e valores ausentes são substituídos por 'nan'.
  Se os elementos forem tuplas ou listas, apenas o segundo elemento (valor) é convertido em string.

  Args:
      data (list[float | tuple]): Lista de valores numéricos ou tuplas (date, value).

  Returns:
      list[str | tuple]: Lista com valores convertidos em strings. Para tuplas, retorna (data, valor_str).

  Examples:
      >>> encode_textual([10, None, 5.0, float('nan')])
      ['10', 'nan', '5.0', 'nan']
      >>> encode_textual([("2025-01-01", 10), ("2025-01-02", None)])
      [('2025-01-01', '10'), ('2025-01-02', 'nan')]
  """
  if data and isinstance(data[0], (tuple, list)):
    return [(d, ' '.join(str(normalize_missing(v)))) for d, v in data]
  return [' '.join(str(normalize_missing(v))) for v in data]
