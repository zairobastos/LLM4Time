import numpy as np
from typing import Union


def normalize_missing(value: Union[float, None]) -> Union[float, str]:
  """
  Normaliza valores ausentes ou NaN em uma representação padronizada.

  Se o valor for None ou NaN, retorna a string 'nan'.
  Caso contrário, retorna o valor original.

  Args:
      value (float | None): Valor numérico ou None.

  Returns:
      float | str: Retorna o valor original se válido, ou 'nan' se ausente.

  Examples:
      >>> normalize_missing(10.5)
      10.5
      >>> normalize_missing(None)
      'nan'
      >>> normalize_missing(np.nan)
      'nan'
  """
  if value is None or (isinstance(value, float) and np.isnan(value)):
    return 'nan'
  return value
