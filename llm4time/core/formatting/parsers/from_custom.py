import pandas as pd
from io import StringIO


def from_custom(data: str) -> list:
  """
  Converte uma string no formato customizado com separador "|" em uma lista de tuplas (date, value).

  Args:
      data (str): String contendo os dados, com cabeçalho "Date|Value" e valores separados por "|".

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:
      >>> s = "Date|Value\\n2025-01-01|10\\n2025-01-02|20"
      >>> from_custom(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  df = pd.read_csv(StringIO(data), sep="|")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
