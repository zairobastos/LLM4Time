import pandas as pd
from io import StringIO


def from_symbol(data: str) -> list:
  """
  Converte uma string CSV contendo colunas "Date", "Value" e possivelmente "DirectionIndicator"
  em uma lista de tuplas (date, value).

  O indicador de direção é ignorado e apenas "Date" e "Value" são retornados.

  Args:
      data (str): String CSV com pelo menos as colunas "Date" e "Value".

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:
      >>> s = "Date,Value,DirectionIndicator\\n2025-01-01,10,→\\n2025-01-02,20,↑"
      >>> from_symbol(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  df = pd.read_csv(StringIO(data))
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
