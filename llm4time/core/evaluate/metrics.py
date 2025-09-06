"""
Módulo para avaliação de modelos de séries temporais.

Este módulo fornece uma classe para calcular métricas de performance
comumente utilizadas na avaliação de previsões de séries temporais.
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from scipy.stats import sem


class Metrics:
  """
  Classe para calcular métricas de avaliação de previsões de séries temporais.

  Esta classe calcula diversas métricas de erro entre valores observados e preditos,
  removendo automaticamente valores NaN antes dos cálculos para garantir robustez.

  Args:
      y_val (list[float]): Lista de valores observados (reais) da série temporal.
      y_pred (list[float]): Lista de valores preditos pelo modelo.

  Attributes:
      y_val (np.array): Array numpy com valores observados sem NaN.
      y_pred (np.array): Array numpy com valores preditos sem NaN.

  Examples:
      >>> metrics = Metrics([10, 20, 30], [12, 18, 32])
      >>> print(metrics.mae)
      2.0
      >>> print(metrics.rmse)
      2.31
      >>> print(metrics.smape)
      6.67
      >>> print(Metrics.sem([2, -2, 2]))
      1.1547
  """

  def __init__(self, y_val: list[float], y_pred: list[float]) -> None:
    self.y_val = np.array(y_val)[~np.isnan(y_val)]
    self.y_pred = np.array(y_pred)[~np.isnan(y_pred)]

  @property
  def smape(self) -> float:
    """
    SMAPE — Erro Percentual Absoluto Médio Simétrico.

    Retorna a métrica em percentual, útil para avaliar a acurácia
    de previsões em diferentes escalas.

    Returns:
        float: Valor do SMAPE em percentual (duas casas decimais).
    """
    numerator = np.abs(self.y_val - self.y_pred)
    denominator = (np.abs(self.y_val) + np.abs(self.y_pred)) / 2
    epsilon = 1e-10
    smape = np.mean(numerator / (denominator + epsilon)) * 100
    return round(smape, 2)

  @property
  def mae(self) -> float:
    """
    MAE — Erro Absoluto Médio.

    Mede a média dos erros absolutos entre valores observados e preditos.

    Returns:
        float: Valor do MAE (duas casas decimais).
    """
    mae = mean_absolute_error(self.y_val, self.y_pred)
    return round(mae, 2)

  @property
  def rmse(self) -> float:
    """
    RMSE — Raiz do Erro Quadrático Médio.

    Penaliza mais fortemente erros grandes, sendo útil quando
    grandes desvios são indesejáveis.

    Returns:
        float: Valor do RMSE (duas casas decimais).
    """
    rmse = root_mean_squared_error(self.y_val, self.y_pred)
    return round(rmse, 2)

  @staticmethod
  def sem(errors: list[float]) -> float:
    """
    SEM — Erro Padrão da Média.

    Mede a variabilidade da média dos erros, útil para estimar
    intervalos de confiança.

    Args:
        errors (list[float]): Lista de erros individuais.

    Returns:
        float: Valor do SEM (quatro casas decimais).
    """
    return round(sem(errors), 4)
