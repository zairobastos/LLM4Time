def to_markdown(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma tabela Markdown.

  Cada tupla é transformada em uma linha da tabela com colunas "Date" e "Value".

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String formatada como tabela Markdown.

  Examples:
      >>> to_markdown([("2025-01-01", 10), ("2025-01-02", 20)])
      '|Date|Value|\\n|---|---|\\n|2025-01-01|10|\\n|2025-01-02|20|'
  """
  return "|Date|Value|\n|---|---|\n" + "\n".join(f"|{d}|{v}|" for d, v in data)
