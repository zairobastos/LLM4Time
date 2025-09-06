"""
Módulo para análise estatística de séries temporais.

Este módulo fornece uma classe para calcular estatísticas descritivas
e análises avançadas de séries temporais, incluindo decomposição
de tendência e sazonalidade usando STL.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL


class Statistics:
  """
  Classe para calcular estatísticas descritivas de séries temporais.

  Esta classe fornece propriedades para calcular medidas estatísticas robustas
  de séries temporais, tratando automaticamente valores ausentes e fornecendo
  análises de tendência e sazonalidade.

  Args:
      data (list[float]): Lista de valores numéricos da série temporal.

  Attributes:
      data (np.array): Array numpy com todos os dados originais.
      valid_data (np.array): Array numpy apenas com dados válidos (sem NaN).

  Examples:
      >>> data = [10.5, 12.0, np.nan, 15.2, 13.8, 11.1]
      >>> stats = Statistics(data)
      >>> stats.mean
      12.52
      >>> stats.missing_count
      1
  """

  def __init__(self, data: list[float]) -> None:
    """
    Inicializa a classe Statistics com dados da série temporal.

    Args:
        data (list[float]): Lista de valores numéricos.
    """
    self.data = np.array(data)
    self.valid_data = np.array(data)[~np.isnan(data)]

  @property
  def mean(self) -> float:
    """
    Calcula a média dos valores válidos.

    Returns:
        float: Média arredondada para 4 casas decimais.
    """
    return round(float(np.mean(self.valid_data)), 4)

  @property
  def median(self) -> float:
    """
    Calcula a mediana dos valores válidos.

    Returns:
        float: Mediana arredondada para 4 casas decimais.
    """
    return round(float(np.median(self.valid_data)), 4)

  @property
  def first_quartile(self) -> float:
    """
    Calcula o primeiro quartil (percentil 25) dos valores válidos.

    Returns:
        float: Primeiro quartil arredondado para 4 casas decimais.
    """
    return round(float(np.percentile(self.valid_data, 25)), 4)

  @property
  def third_quartile(self) -> float:
    """
    Calcula o terceiro quartil (percentil 75) dos valores válidos.

    Returns:
        float: Terceiro quartil arredondado para 4 casas decimais.
    """
    return round(float(np.percentile(self.valid_data, 75)), 4)

  @property
  def std(self) -> float:
    """
    Calcula o desvio padrão amostral dos valores válidos.

    Usa ddof=1 para calcular o desvio padrão amostral (divisão por n-1).

    Returns:
        float: Desvio padrão arredondado para 4 casas decimais.
    """
    return round(float(np.std(self.valid_data, ddof=1)), 4)

  @property
  def min(self) -> float:
    """
    Encontra o valor mínimo dos valores válidos.

    Returns:
        float: Valor mínimo arredondado para 4 casas decimais.
    """
    return round(float(np.min(self.valid_data)), 4)

  @property
  def max(self) -> float:
    """
    Encontra o valor máximo dos valores válidos.

    Returns:
        float: Valor máximo arredondado para 4 casas decimais.
    """
    return round(float(np.max(self.valid_data)), 4)

  @property
  def missing_count(self) -> int:
    """
    Conta o número de valores ausentes (NaN) nos dados.

    Returns:
        int: Quantidade de valores NaN.
    """
    return int(np.isnan(self.data).sum())

  @property
  def missing_percentage(self) -> float:
    """
    Calcula a porcentagem de valores ausentes nos dados.

    Returns:
        float: Percentual de valores NaN arredondado para 4 casas decimais.
    """
    total = len(self.data)
    missing = self.missing_count
    return round(float((missing / total) * 100) if total > 0 else 0.0, 4)

  @staticmethod
  def trend_seasonality(
      df: pd.DataFrame,
      period: int = None,
      freq: str = None
  ) -> tuple[pd.Series, pd.Series, pd.Series, float, float]:
    """
    Decompõe uma série temporal em tendência, sazonalidade e resíduo usando STL.

    Aplica decomposição STL (Seasonal and Trend decomposition using Loess)
    e calcula a força da tendência e da sazonalidade baseada na variância
    dos componentes.

    Args:
        df (pd.DataFrame): DataFrame contendo colunas "date" e "value".
        period (int, optional): Período sazonal para STL. Se None, STL infere automaticamente.
                                Defaults to None.
        freq (str, optional): Frequência da série temporal (ex.: "D", "M", "Q").
                              Se fornecida, será aplicada via asfreq. Defaults to None.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, float, float]: Tupla contendo:
            - trend: Componente de tendência estimada
            - seasonal: Componente sazonal estimado
            - resid: Resíduo após remoção de tendência e sazonalidade
            - trend_strength: Força da tendência (0 = fraca, 1 = forte)
            - seasonality_strength: Força da sazonalidade (0 = fraca, 1 = forte)

    Examples:
        >>> data = pd.DataFrame({
        ...     "date": pd.date_range("2020-01-01", periods=24, freq="M"),
        ...     "value": [i + (i % 12) * 2 for i in range(24)]
        ... })
        >>> trend, seasonal, resid, t_str, s_str = Statistics.trend_seasonality(data, period=12)
        >>> # Retorna componentes decompostos e forças calculadas
    """
    df = df.copy()

    # Garantir que a coluna "date" exista e seja datetime
    if "date" not in df.columns:
      print("[ERROR] O DataFrame deve conter a coluna 'date'.")
      return None, None, None, np.nan, np.nan
    try:
      df["date"] = pd.to_datetime(df["date"])
      df = df.sort_values('date')
    except Exception as e:
      print(f"[ERROR] Erro ao converter 'date' para datetime: {e}")
      return None, None, None, np.nan, np.nan

    df = df.set_index("date")

    # Garantir que exista a coluna "value"
    if "value" not in df.columns:
      print("[ERROR] O DataFrame deve conter a coluna 'value'.")
      return None, None, None, np.nan, np.nan

    # Forçar frequência se for informada
    if freq is not None:
      try:
        df = df.asfreq(freq)
      except Exception as e:
        print(f"[ERROR] Erro ao definir frequência '{freq}': {e}")
        return None, None, None, np.nan, np.nan

    # Aplicar STL
    try:
      stl = STL(df["value"], period=period) if period else STL(df["value"])
      res = stl.fit()
    except Exception as e:
      print(f"[ERROR] Erro ao aplicar STL: {e}")
      return None, None, None, np.nan, np.nan

    trend, seasonal, resid = (
        res.trend.round(4), res.seasonal.round(4), res.resid.round(4))

    # Cálculo das forças
    try:
      var_r = np.var(resid)
      trend_strength = round(
          1 - var_r / np.var(trend + resid), 4
      ) if np.var(trend + resid) > 0 else np.nan
      seasonality_strength = round(
          1 - var_r / np.var(seasonal + resid), 4
      ) if np.var(seasonal + resid) > 0 else np.nan
    except Exception as e:
      print(f"[ERROR] Erro ao calcular forças: {e}")
      return None, None, None, np.nan, np.nan

    return trend, seasonal, resid, trend_strength, seasonality_strength
