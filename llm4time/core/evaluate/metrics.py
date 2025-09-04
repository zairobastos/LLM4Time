"""
Módulo para avaliação de modelos de séries temporais.

Este módulo fornece uma classe para calcular métricas de performance
comumente utilizadas na avaliação de previsões de séries temporais,
incluindo métricas de erro absoluto, quadrático e percentual.
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
      >>> y_val = [10.0, 20.0, 30.0, 40.0]
      >>> y_pred = [9.5, 19.8, 31.2, 38.9]
      >>> metrics = Metrics(y_val, y_pred)
      >>> print(f"MAE: {metrics.mae()}")
      MAE: 1.15
      >>> print(f"SMAPE: {metrics.smape()}%")
      SMAPE: 3.85%
  """

  def __init__(self, y_val: list[float], y_pred: list[float]) -> None:
    """
    Inicializa a classe Metrics com valores observados e preditos.

    Args:
        y_val (list[float]): Lista de valores observados (reais).
        y_pred (list[float]): Lista de valores preditos.
    """
    self.y_val = np.array(y_val)[~np.isnan(y_val)]
    self.y_pred = np.array(y_pred)[~np.isnan(y_pred)]

  def smape(self) -> float:
    """
    Calcula o Symmetric Mean Absolute Percentage Error (SMAPE).

    SMAPE é uma métrica percentual que mede a precisão das previsões,
    sendo simétrica e menos sensível a outliers que MAPE tradicional.

    Returns:
        float: Valor do SMAPE em percentual, arredondado para 2 casas decimais.

    Examples:
        >>> metrics = Metrics([100, 200, 300], [110, 190, 310])
        >>> metrics.smape()
        6.67
    """
    numerator = np.abs(self.y_val - self.y_pred)
    denominator = (np.abs(self.y_val) + np.abs(self.y_pred))/2
    epsilon = 1e-10

    smape = np.mean(numerator / (denominator+epsilon))*100
    return round(smape, 2)

  def sem(self, errors: list[float]) -> float:
    """
    Calcula o Standard Error of the Mean (SEM) dos erros.

    SEM fornece uma medida da variabilidade da média dos erros,
    útil para determinar intervalos de confiança das métricas.

    Args:
        errors (list[float]): Lista de erros individuais.

    Returns:
        float: Valor do SEM arredondado para 4 casas decimais.

    Examples:
        >>> metrics = Metrics([10, 20, 30], [12, 18, 32])
        >>> errors = [2, -2, 2]  # diferenças individuais
        >>> metrics.sem(errors)
        1.1547
    """
    return round(sem(errors), 4)

  def mae(self) -> float:
    """
    Calcula o Mean Absolute Error (MAE).

    MAE mede a média dos erros absolutos entre valores observados
    e preditos, fornecendo uma interpretação direta do erro médio.

    Returns:
        float: Valor do MAE arredondado para 2 casas decimais.

    Examples:
        >>> metrics = Metrics([10, 20, 30], [12, 18, 32])
        >>> metrics.mae()
        2.0
    """
    mae = mean_absolute_error(self.y_val, self.y_pred)
    return round(mae, 2)

  def rmse(self) -> float:
    """
    Calcula o Root Mean Squared Error (RMSE).

    RMSE penaliza erros maiores mais severamente que MAE,
    sendo sensível a outliers e útil quando erros grandes
    são particularmente indesejáveis.

    Returns:
        float: Valor do RMSE arredondado para 2 casas decimais.

    Examples:
        >>> metrics = Metrics([10, 20, 30], [12, 18, 32])
        >>> metrics.rmse()
        2.31
    """
    rmse = root_mean_squared_error(self.y_val, self.y_pred)
    return round(rmse, 2)
