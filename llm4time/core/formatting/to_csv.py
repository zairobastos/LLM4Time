def to_csv(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string CSV com cabeçalho "Date,Value".

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String no formato CSV, com cada linha representando "data,valor".

  Examples:
      >>> to_csv([("2025-01-01", 10), ("2025-01-02", 20)])
      'Date,Value\\n2025-01-01,10\\n2025-01-02,20'
  """
  return "Date,Value\n" + "\n".join(f"{d},{v}" for d, v in data)
