import numpy as np
from typing import Union


def denormalize_missing(value: Union[float, str]) -> float:
  """
  Converte valores normalizados de ausentes de volta para NaN.

  Se o valor for a string 'nan' (case-insensitive), retorna np.nan.
  Caso contrário, retorna o valor original como float.

  Args:
      value (float | str): Valor numérico ou string representando NaN.

  Returns:
      float: Valor original ou np.nan se o valor for 'nan'.

  Examples:
      >>> denormalize_missing(10.5)
      10.5
      >>> denormalize_missing('nan')
      nan
      >>> denormalize_missing('NaN')
      nan
  """
  if str(value).lower() == 'nan':
    return np.nan
  return value
