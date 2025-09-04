def to_array(data: list[float | tuple]) -> str:
  """
  Converte uma lista de números ou uma lista de tuplas em uma string formatada como array.

  Args:
      data (list[float | tuple]): Lista de valores numéricos ou tuplas/listas (ex.: [(x, y), ...]).

  Returns:
      str: String no formato "[v1, v2, v3, ...]".

  Examples:
      >>> to_array([1, 2, 3])
      '[1, 2, 3]'
      >>> to_array([(0, 10), (1, 20), (2, 30)])
      '[10, 20, 30]'
  """
  if data and isinstance(data[0], (tuple, list)):
    data = [v for _, v in data]
  return "[" + ", ".join(map(str, data)) + "]"
