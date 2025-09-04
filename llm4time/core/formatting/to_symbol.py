def to_symbol(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string CSV incluindo um indicador de direção.

  Para cada valor, a direção é representada por:
    - "→" se for o primeiro valor ou se igual ao anterior,
    - "↑" se o valor aumentar em relação ao anterior,
    - "↓" se o valor diminuir em relação ao anterior.

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String CSV com colunas "Date,Value,DirectionIndicator".

  Examples:
      >>> to_symbol([("2025-01-01", 10), ("2025-01-02", 20), ("2025-01-03", 15), ("2025-01-04", 15)])
      'Date,Value,DirectionIndicator\\n2025-01-01,10,→\\n2025-01-02,20,↑\\n2025-01-03,15,↓\\n2025-01-04,15,→'
  """
  def direction(i: int) -> str:
    if i == 0:
      return "→"
    return "↑" if data[i][1] > data[i-1][1] else "↓" if data[i][1] < data[i-1][1] else "→"
  return "Date,Value,DirectionIndicator\n" + "\n".join(f"{d},{v},{direction(i)}" for i, (d, v) in enumerate(data))
