import json


def from_json(data: str) -> list:
  """
  Converte uma string JSON contendo uma lista de objetos com chaves "Date" e "Value"
  em uma lista de tuplas (date, value).

  Args:
      data (str): String JSON representando uma lista de objetos.
                  Exemplo: '[{"Date": "2025-01-01", "Value": 10}, {"Date": "2025-01-02", "Value": 20}]'

  Returns:
      list[tuple]: Lista de tuplas (date, value).

  Examples:
      >>> s = '[{"Date": "2025-01-01", "Value": 10}, {"Date": "2025-01-02", "Value": 20}]'
      >>> from_json(s)
      [('2025-01-01', 10), ('2025-01-02', 20)]
  """
  return [(v["Date"], v["Value"]) for v in json.loads(data)]
