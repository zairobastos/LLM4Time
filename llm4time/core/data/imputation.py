"""
Módulo para imputação de valores ausentes em séries temporais.

Este módulo fornece diversas estratégias para tratamento de valores NaN
em dados de séries temporais, incluindo métodos estatísticos, de preenchimento
e interpolação.
"""

import pandas as pd
from typing import Union


def mean(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando a média da coluna 'value'.

  Substitui todos os valores NaN na coluna 'value' pela média
  dos valores não-nulos, arredondada para 3 casas decimais.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      pela média.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> df_filled = mean(df)
      >>> print(df_filled['value'].tolist())
      [1.0, 3.0, 3.0, 3.0, 5.0]
  """
  data["value"] = data["value"].fillna(round(data["value"].mean(), 3))
  return data


def median(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando a mediana da coluna 'value'.

  Substitui todos os valores NaN na coluna 'value' pela mediana
  dos valores não-nulos. Útil quando há outliers nos dados.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      pela mediana.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, 100.0, np.nan, 5.0]})
      >>> df_filled = median(df)
      >>> print(df_filled['value'].median())
      5.0
  """
  data["value"] = data["value"].fillna(data["value"].median())
  return data


def forward_fill(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando forward fill seguido de backward fill.

  Preenche valores NaN propagando o último valor válido para frente,
  e depois preenche valores restantes propagando para trás. Preserva
  a continuidade temporal dos dados.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por propagação temporal.

  Examples:
      >>> df = pd.DataFrame({'value': [np.nan, 2.0, np.nan, 4.0, np.nan]})
      >>> df_filled = forward_fill(df)
      >>> print(df_filled['value'].tolist())
      [2.0, 2.0, 2.0, 4.0, 4.0]
  """
  data["value"] = data["value"].ffill().bfill()
  return data


def backward_fill(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando backward fill seguido de forward fill.

  Preenche valores NaN propagando o próximo valor válido para trás,
  e depois preenche valores restantes propagando para frente.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por propagação temporal reversa.

  Examples:
      >>> df = pd.DataFrame({'value': [np.nan, 2.0, np.nan, 4.0, np.nan]})
      >>> df_filled = backward_fill(df)
      >>> print(df_filled['value'].tolist())
      [2.0, 2.0, 4.0, 4.0, 4.0]
  """
  data["value"] = data["value"].bfill().ffill()
  return data


def simple_moving_average(
    data: Union[pd.Series, pd.DataFrame], window: int, min_periods: int = 1
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando média móvel simples.

  Calcula a média móvel dos valores não-nulos e usa para imputar
  valores ausentes, seguido de forward/backward fill para garantir
  cobertura completa.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.
      window (int): Tamanho da janela para cálculo da média móvel.
      min_periods (int, optional): Número mínimo de observações na janela.
                                  Defaults to 1.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por média móvel.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> df_filled = simple_moving_average(df, window=3)
  """
  data["value"] = data["value"].fillna(data["value"].rolling(
      window=window, min_periods=min_periods).mean()).ffill().bfill()
  return data


def exponential_moving_average(
    data: Union[pd.Series, pd.DataFrame], span: int, adjust: bool = False
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando média móvel exponencial.

  Aplica média móvel exponencial que dá maior peso aos valores recentes
  para imputar valores ausentes, seguido de forward/backward fill.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.
      span (int): Span para o cálculo da média móvel exponencial.
      adjust (bool, optional): Se True, divide por fator de decaimento
                              em expansão. Defaults to False.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por média móvel exponencial.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> df_filled = exponential_moving_average(df, span=3)
  """
  data["value"] = data["value"].fillna(data["value"].ewm(
      span=span, adjust=adjust).mean()).ffill().bfill()
  return data


def linear_interpolation(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando interpolação linear.

  Usa interpolação linear entre pontos conhecidos para estimar
  valores ausentes, seguido de forward/backward fill para extremos.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por interpolação linear.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, np.nan, 4.0]})
      >>> df_filled = linear_interpolation(df)
      >>> print(df_filled['value'].tolist())
      [1.0, 2.0, 3.0, 4.0]
  """
  data["value"] = data["value"].interpolate(method='linear').ffill().bfill()
  return data


def spline_interpolation(
    data: Union[pd.Series, pd.DataFrame], order: int = 2
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando interpolação spline.

  Aplica interpolação spline de ordem especificada para suavizar
  a estimação de valores ausentes. Em caso de falha, recorre à
  interpolação linear.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.
      order (int, optional): Ordem do polinômio spline. Defaults to 2.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      por interpolação spline ou linear
                                      (fallback).

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, np.nan, 4.0, np.nan, 6.0]})
      >>> df_filled = spline_interpolation(df, order=3)
      >>> # Curva suave conectando pontos conhecidos
  """
  try:
    data["value"] = data["value"].interpolate(
        method='spline', order=order).ffill().bfill()
    return data
  except:
    return linear_interpolation(data)


def zero(
    data: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes com zero.

  Substitui todos os valores NaN na coluna 'value' por 0.
  Útil quando valores ausentes representam ausência de eventos
  ou medições.

  Args:
      data (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                            com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados
                                      com zero.

  Examples:
      >>> df = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> df_filled = zero(df)
      >>> print(df_filled['value'].tolist())
      [1.0, 0.0, 3.0, 0.0, 5.0]
  """
  data["value"] = data["value"].fillna(0)
  return data
