import pandas as pd
from io import StringIO


def from_markdown(data: str) -> list:
  """
  Converte uma string representando uma tabela Markdown em uma lista de tuplas (date, value).

  Remove as linhas de separação Markdown (`|---|---|`) e converte as colunas
  em `Date` e `Value`.

  Args:
      data (str): String contendo a tabela Markdown. Exemplo::

          |Date|Value|
          |---|---|
          |2025-01-01|10|
          |2025-01-02|20|

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:

      >>> s = "|Date|Value|\\n|---|---|\\n|2025-01-01|10|\\n|2025-01-02|20|"
      >>> from_markdown(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  data = data.strip().splitlines()
  data = [line.strip().strip("|") for line in [data[0]] + data[2:]]
  df = pd.read_csv(StringIO("\n".join(data)), sep="|",
                   engine="python", skipinitialspace=True)
  df.columns = [c.strip() for c in df.columns]
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))
