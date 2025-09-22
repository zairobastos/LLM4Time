"""
Módulo para formatação e parsing de séries temporais.
"""

from .formatting import TSFormat, TSType
from .formatting import FORMATTERS, PARSERS
from .formatting import ENCODERS, DECODERS


def format(data: list, ts_format: TSFormat, ts_type: TSType) -> str:
  """
  Formata uma série temporal de acordo com o tipo e o formato especificados.

  Args:
      data (list): Série temporal, como lista de valores ou tuplas (data, valor).
      ts_format (TSFormat): Tipo de formatação desejada (ex.: CSV, JSON, Markdown, etc.).
      ts_type (TSType): Tipo de codificação dos valores (ex.: numeric, textual).

  Returns:
      str: Série temporal formatada como string de acordo com `ts_format` e `ts_type`.

  Raises:
      ValueError: Se `ts_format` ou `ts_type` forem desconhecidos.

  Examples:

      >>> format([("2025-01-01", 100), ("2025-01-02", 200)],
      ...        ts_format=TSFormat.CSV, ts_type=TSType.NUMERIC)
      'Date,Value\\n2025-01-01,100\\n2025-01-02,200'

      >>> format([("2025-01-01", 100), ("2025-01-02", 200)],
      ...        ts_format=TSFormat.CSV, ts_type=TSType.TEXTUAL)
      'Date,Value\\n2025-01-01,1 0 0\\n2025-01-02,2 0 0'
  """
  if ts_format not in FORMATTERS:
    raise ValueError(f"Formato desconhecido: {ts_format}")
  if ts_type not in ENCODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  return FORMATTERS[ts_format](ENCODERS[ts_type](data))


def parse(data: str, ts_format: TSFormat, ts_type: TSType) -> list:
  """
  Converte uma string representando uma série temporal em uma lista de valores
  ou tuplas (date, value), de acordo com o formato e o tipo especificados.

  Caso ocorra falha durante o parsing, a função tenta uma alternativa de fallback,
  assumindo formato `ARRAY` e tipo `NUMERIC`.

  Args:
      ts (str): String contendo a série temporal (ex.: CSV, JSON, Markdown, etc.).
      ts_format (TSFormat): Formato de entrada (ex.: 'csv', 'json', 'markdown').
      ts_type (TSType): Tipo de codificação esperado ('numeric' ou 'textual').

  Returns:
      list: Série temporal como lista de valores ou tuplas (date, value).

  Raises:
      ValueError: Se `ts_format` ou `ts_type` forem desconhecidos.

  Examples:

      >>> parse("Date,Value\\n2025-01-01,100\\n2025-01-02,200",
      ...       ts_format=TSFormat.CSV, ts_type=TSType.NUMERIC)
      [('2025-01-01', 100), ('2025-01-02', 200)]

      >>> parse("Date,Value\\n2025-01-01,1 0 0\\n2025-01-02,2 0 0",
      ...       ts_format=TSFormat.CSV, ts_type=TSType.TEXTUAL)
      [('2025-01-01', 100), ('2025-01-02', 200)]
  """
  if ts_format not in PARSERS:
    raise ValueError(f"Formato desconhecido: {ts_format}")
  if ts_type not in DECODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  try:
    return DECODERS[ts_type](PARSERS[ts_format](data))
  except:
    return DECODERS[TSType.NUMERIC](PARSERS[TSFormat.ARRAY](data))
