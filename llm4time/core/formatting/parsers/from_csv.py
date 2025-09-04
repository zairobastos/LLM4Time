import pandas as pd
from io import StringIO


def from_csv(data: str) -> list:
  """
  Converte uma string CSV no formato "Date,Value" em uma lista de tuplas (date, value).

  Args:
      data (str): String contendo os dados CSV, com cabeçalho "Date,Value".

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:
      >>> s = "Date,Value\\n2025-01-01,10\\n2025-01-02,20"
      >>> from_csv(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  df = pd.read_csv(StringIO(data))
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
