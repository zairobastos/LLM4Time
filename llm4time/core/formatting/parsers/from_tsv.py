import pandas as pd
from io import StringIO


def from_tsv(data: str) -> list:
  """
  Converte uma string no formato TSV (Tab-Separated Values) em uma lista de tuplas (date, value).

  Args:
      data (str): String contendo os dados TSV com cabeçalho "Date\tValue".

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:
      >>> s = "Date\tValue\\n2025-01-01\t10\\n2025-01-02\t20"
      >>> from_tsv(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  df = pd.read_csv(StringIO(data), sep="\t")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
