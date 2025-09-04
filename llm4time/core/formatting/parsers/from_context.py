import pandas as pd
from io import StringIO


def from_context(data: str) -> list:
  """
  Converte uma string CSV-like no formato "Date,Value" em uma lista de tuplas (date, value),
  removendo colchetes dos valores.

  Args:
      data (str): String contendo os dados CSV-like, com cabeçalho "Date,Value".
                  Exemplo de linha: 2025-01-01,[10]

  Returns:
      list[tuple]: Lista de tuplas (date, value) com valores como strings sem colchetes.

  Examples:
      >>> s = "Date,Value\\n2025-01-01,[10]\\n2025-01-02,[20]"
      >>> from_context(s)
      [('2025-01-01', '10'), ('2025-01-02', '20')]
  """
  df = pd.read_csv(StringIO(data))
  df["Value"] = df["Value"].astype(str).str.strip("[]")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
