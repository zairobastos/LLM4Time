from .evaluate.metrics import Metrics


def evaluate(y_val: list[float], y_pred: list[float]) -> tuple[float, float, float]:
  """
  Avalia a performance de previsões de séries temporais usando métricas comuns.

  Calcula sMAPE, MAE e RMSE comparando os valores reais (`y_val`) com as previsões (`y_pred`).

  Args:
      y_val (list[float]): Valores reais da série temporal (conjunto de validação).
      y_pred (list[float]): Valores previstos correspondentes.

  Returns:
      tuple[float, float, float]: Métricas de avaliação:
          - sMAPE (Symmetric Mean Absolute Percentage Error)
          - MAE (Mean Absolute Error)
          - RMSE (Root Mean Squared Error)

  Examples:
      >>> y_val = [100, 200, 300]
      >>> y_pred = [110, 190, 310]
      >>> evaluate(y_val, y_pred)
      (0.0667, 10.0, 12.9099)
  """
  metrics = Metrics(y_val, y_pred)
  smape = metrics.smape()
  mae = metrics.mae()
  rmse = metrics.rmse()
  return smape, mae, rmse
