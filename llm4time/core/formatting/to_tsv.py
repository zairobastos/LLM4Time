def to_tsv(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string no formato TSV (Tab-Separated Values).

  Cada tupla é transformada em uma linha, com data e valor separados por tabulação.

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String formatada como TSV com cabeçalho "Date\tValue".

  Examples:
      >>> to_tsv([("2025-01-01", 10), ("2025-01-02", 20)])
      'Date\\tValue\\n2025-01-01\\t10\\n2025-01-02\\t20'
  """
  return "Date\tValue\n" + "\n".join(f"{d}\t{v}" for d, v in data)
