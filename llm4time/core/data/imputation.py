"""
Módulo para imputação de valores ausentes em séries temporais.

Este módulo fornece diversas estratégias para tratamento de valores NaN
em dados de séries temporais, incluindo métodos estatísticos, de preenchimento
e interpolação.
"""

import pandas as pd
from typing import Union


def mean(
    ts: Union[pd.Series, pd.DataFrame],
    decimals: int = 4
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando a média da coluna 'value'.

  Substitui todos os valores NaN na coluna 'value' pela média
  dos valores não nulos, arredondada para o número de casas
  decimais definido.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.
      decimals (int, opcional): Número de casas decimais para arredondamento.
                                Padrão: 4.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados pela média.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> mean(ts, decimals=2)
      [1.0, 3.0, 3.0, 3.0, 5.0]
  """
  ts["value"] = ts["value"].fillna(round(ts["value"].mean(), decimals))
  return ts


def median(
    ts: Union[pd.Series, pd.DataFrame],
    decimals: int = 4
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando a mediana da coluna 'value'.

  Substitui todos os valores NaN na coluna 'value' pela mediana
  dos valores não nulos, arredondada para o número de casas
  decimais definido.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna
                                'value' com possíveis valores ausentes.
      decimals (int, opcional): Número de casas decimais para arredondamento.
                                Padrão: 4.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados pela mediana.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, 100.0, np.nan, 5.0]})
      >>> median(ts, decimals=2)
      [1.0, 5.0, 100.0, 5.0, 5.0]
  """
  ts["value"] = ts["value"].fillna(round(ts["value"].median(), decimals))
  return ts


def ffill(
    ts: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando forward fill seguido de backward fill.

  Preenche valores NaN propagando o último valor válido para frente,
  e depois preenche valores restantes propagando para trás. Preserva
  a continuidade temporal dos dados.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por propagação temporal.

  Examples:
      >>> ts = pd.DataFrame({'value': [np.nan, 2.0, np.nan, 4.0, np.nan]})
      >>> ffill(ts)
      [2.0, 2.0, 2.0, 4.0, 4.0]
  """
  ts["value"] = ts["value"].ffill().bfill()
  return ts


def bfill(
    ts: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando backward fill seguido de forward fill.

  Preenche valores NaN propagando o próximo valor válido para trás,
  e depois preenche valores restantes propagando para frente.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por propagação temporal reversa.

  Examples:
      >>> ts = pd.DataFrame({'value': [np.nan, 2.0, np.nan, 4.0, np.nan]})
      >>> bfill(ts)
      [2.0, 2.0, 4.0, 4.0, 4.0]
  """
  ts["value"] = ts["value"].bfill().ffill()
  return ts


def sma(
    ts: Union[pd.Series, pd.DataFrame],
    window: int,
    min_periods: int = 1
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando média móvel simples.

  Calcula a média móvel dos valores não nulos e usa para imputar
  valores ausentes, seguido de forward/backward fill para garantir
  cobertura completa.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.
      window (int): Tamanho da janela para cálculo da média móvel.
      min_periods (int, optional): Número mínimo de observações na janela.
                                   Padrão: 1.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por média móvel.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> sma(ts, window=3)
  """
  ts["value"] = ts["value"].fillna(ts["value"].rolling(
      window=window, min_periods=min_periods).mean()).ffill().bfill()
  return ts


def ema(
    ts: Union[pd.Series, pd.DataFrame], span: int, adjust: bool = False
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando média móvel exponencial.

  Aplica média móvel exponencial que dá maior peso aos valores recentes
  para imputar valores ausentes, seguido de forward/backward fill.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.
      span (int): Span para o cálculo da média móvel exponencial.
      adjust (bool, optional): Se True, divide por fator de decaimento em expansão.
                              Padrão: False.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por média móvel exponencial.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> ema(ts, span=3)
  """
  ts["value"] = ts["value"].fillna(ts["value"].ewm(
      span=span, adjust=adjust).mean()).ffill().bfill()
  return ts


def linear_interpolation(
    ts: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando interpolação linear.

  Usa interpolação linear entre pontos conhecidos para estimar
  valores ausentes, seguido de forward/backward fill para extremos.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por interpolação linear.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, np.nan, 4.0]})
      >>> linear_interpolation(ts)
      [1.0, 2.0, 3.0, 4.0]
  """
  ts["value"] = ts["value"].interpolate(method='linear').ffill().bfill()
  return ts


def spline_interpolation(
    ts: Union[pd.Series, pd.DataFrame],
    order: int = 2
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes usando interpolação spline.

  Aplica interpolação spline de ordem especificada para suavizar
  a estimação de valores ausentes. Em caso de falha, recorre à
  interpolação linear.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.
      order (int, optional): Ordem do polinômio spline.
                             Padrão: 2.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados por interpolação spline ou linear (fallback).

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, np.nan, 4.0, np.nan, 6.0]})
      >>> spline_interpolation(ts, order=3)
  """
  try:
    ts["value"] = ts["value"].interpolate(
        method='spline', order=order).ffill().bfill()
    return ts
  except:
    return linear_interpolation(ts)


def zero(
    ts: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
  """
  Imputa valores ausentes com zero.

  Substitui todos os valores NaN na coluna 'value' por 0.
  Útil quando valores ausentes representam ausência de eventos
  ou medições.

  Args:
      ts (Union[pd.Series, pd.DataFrame]): Dados contendo uma coluna 'value'
                                             com possíveis valores ausentes.

  Returns:
      Union[pd.Series, pd.DataFrame]: Dados com valores ausentes imputados com zero.

  Examples:
      >>> ts = pd.DataFrame({'value': [1.0, np.nan, 3.0, np.nan, 5.0]})
      >>> zero(ts)
      [1.0, 0.0, 3.0, 0.0, 5.0]
  """
  ts["value"] = ts["value"].fillna(0)
  return ts
