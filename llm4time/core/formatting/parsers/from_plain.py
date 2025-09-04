import re


def from_plain(data: str) -> list:
  """
  Converte uma string em formato plain text em uma lista de tuplas (date, value).

  Cada linha deve estar no formato:
      "Date: <data>, Value: <valor>"

  Args:
      data (str): String de múltiplas linhas representando pares data-valor.

  Returns:
      list[tuple]: Lista de tuplas (date, value) como strings.

  Examples:
      >>> s = "Date: 2025-01-01, Value: 10\\nDate: 2025-01-02, Value: 20"
      >>> from_plain(s)
      [('2025-01-01', '10'), ('2025-01-02', '20')]
  """
  out = []
  for line in data.strip().splitlines():
    match = re.match(r'Date:\s*([^,]+),\s*Value:\s*(.*)', line.strip())
    if match:
      out.append((match[1], match[2]))
  return out
