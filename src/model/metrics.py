import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from scipy.stats import sem

class Metrics:
  def __init__(self, y_true: list, y_pred: list):
    mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
    self.y_true = np.array(y_true)[mask]
    self.y_pred = np.array(y_pred)[mask]

  def smape(self) -> float:
    """Calcula o erro percentual absoluto médio simétrico (sMAPE).

    Returns:
      float: Erro percentual absoluto médio simétrico.
    """
    y_true = np.array(self.y_true)
    y_pred = np.array(self.y_pred)

    numerator = np.abs(y_true - y_pred)
    denominator = (np.abs(y_true) + np.abs(y_pred))/2
    epsilon = 1e-10

    smape = np.mean(numerator / (denominator+epsilon))*100
    return round(smape, 2)

  def sem(self, erros: list[float]) -> float:
    """Calcula o erro médio absoluto percentual (sEM).

    Parameters:
      erros (list[float]): Lista de erros absolutos percentuais.

    Returns:
      float: Erro médio absoluto percentual.
    """
    return round(sem(erros),4)

  def mae(self) -> float:
    """Calcula o erro médio absoluto (MAE).
    Returns:
      float: Erro médio absoluto.
    """
    y_true = np.array(self.y_true)
    y_pred = np.array(self.y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    return round(mae, 2)

  def rmse(self) -> float:
    """Calcula a raiz do erro quadrático médio (RMSE).
    Returns:
      float: Raiz do erro quadrático médio.
    """
    y_true = np.array(self.y_true)
    y_pred = np.array(self.y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    return round(rmse, 2)
