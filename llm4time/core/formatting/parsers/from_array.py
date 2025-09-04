def from_array(data: str) -> list:
  """
  Converte uma string no formato de array (ex.: "[1, 2, 3]") em uma lista de strings.

  Remove os colchetes e separa os elementos pelo delimitador ", ".

  Args:
      data (str): String representando um array, com elementos separados por vírgula e espaço.

  Returns:
      list[str]: Lista de elementos como strings.

  Examples:
      >>> from_array("[10, 20, 30]")
      ['10', '20', '30']
  """
  return data.strip("[]").split(", ")
