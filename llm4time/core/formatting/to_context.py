def to_context(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string,
  onde cada linha contém a data e o valor entre colchetes.

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String formatada com cabeçalho "Date,Value" e cada linha no formato "data,[valor]".

  Examples:
      >>> to_context([("2025-01-01", 10), ("2025-01-02", 20)])
      'Date,Value\\n2025-01-01,[10]\\n2025-01-02,[20]'
  """
  return "Date,Value\n" + "\n".join(f"{d},[{v}]" for d, v in data)
