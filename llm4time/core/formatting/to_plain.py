def to_plain(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string de texto simples.

  Cada tupla é transformada em uma linha no formato "Date: <data>, Value: <valor>".

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String de múltiplas linhas representando os pares data-valor.

  Examples:
      >>> to_plain([("2025-01-01", 10), ("2025-01-02", 20)])
      'Date: 2025-01-01, Value: 10\\nDate: 2025-01-02, Value: 20'
  """
  return "\n".join(f"Date: {d}, Value: {v}" for d, v in data)
