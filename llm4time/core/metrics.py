from .evaluate.metrics import Metrics
from .evaluate.statistics import Statistics


def evaluate(y_val: list[float], y_pred: list[float]) -> tuple[Metrics, Statistics, Statistics]:
  """
  Avalia previsões de séries temporais e calcula estatísticas descritivas.

  Esta função cria instâncias das classes ``Metrics`` e ``Statistics``
  para fornecer uma análise completa das previsões de séries temporais,
  incluindo métricas de erro e estatísticas descritivas tanto dos valores
  observados quanto dos valores preditos.

  Args:
      y_val (list[float]): Lista de valores observados (reais).
      y_pred (list[float]): Lista de valores preditos pelo modelo.

  Returns:
      tuple[Metrics, Statistics, Statistics]:
          - metrics (Metrics): Instância contendo métricas de erro.
          - stats_val (Statistics): Instância com estatísticas da série observada.
          - stats_pred (Statistics): Instância com estatísticas da série predita.

  Examples:
      >>> y_val = [10, 20, 30, 40]
      >>> y_pred = [12, 18, 29, 41]
      >>> metrics, val_stats, pred_stats = evaluate(y_val, y_pred)
      >>> print(metrics.mae, metrics.rmse, metrics.smape)
      1.5 1.58 5.0
      >>> print(val_stats.mean, pred_stats.mean)
      25.0 25.0
      >>> print(val_stats.missing_count, pred_stats.missing_count)
      0 0
  """
  metrics = Metrics(y_val, y_pred)
  stats_val = Statistics(y_val)
  stats_pred = Statistics(y_pred)
  return metrics, stats_val, stats_pred
