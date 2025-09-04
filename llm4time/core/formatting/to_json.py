import json


def to_json(data: list[tuple]) -> str:
  """
  Converte uma lista de tuplas (date, value) em uma string JSON.

  Cada tupla é transformada em um dicionário com chaves "Date" e "Value".

  Args:
      data (list[tuple]): Lista de tuplas no formato (date, value).

  Returns:
      str: String JSON representando a lista de objetos com campos "Date" e "Value".

  Examples:
      >>> to_json([("2025-01-01", 10), ("2025-01-02", 20)])
      '[{"Date": "2025-01-01", "Value": 10}, {"Date": "2025-01-02", "Value": 20}]'
  """
  return json.dumps([{"Date": d, "Value": v} for d, v in data])
