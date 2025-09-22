"""
Módulo para criação de gráficos.

Este módulo fornece funções especializadas para visualização de dados
de séries temporais, incluindo plotagem de dados históricos, previsões,
estatísticas comparativas e decomposição de séries temporais.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def plot_time_series(title: str, ts: pd.DataFrame, **kwargs):
  """
  Cria um gráfico de linha para uma série temporal com datas.

  Args:
      title (str): Título do gráfico.
      ts (pd.DataFrame): DataFrame contendo colunas 'date' e 'value'
                        com os dados da série temporal.
      **kwargs: Argumentos adicionais passados para fig.update_layout().

  Returns:
      go.Figure: Objeto Figure do Plotly com o gráfico da série temporal.

  Examples:
      >>> ts = pd.DataFrame({
      ...     'date': pd.date_range('2020-01-01', periods=100),
      ...     'value': np.random.randn(100).cumsum()
      ... })
      >>> fig = plot_time_series("Vendas Mensais", ts)
      >>> fig.show()
  """
  fig = go.Figure()
  fig.add_trace(go.Scatter(
      x=ts["date"], y=ts["value"], mode="lines", name="Série Temporal"))
  fig.update_layout(
      title=title,
      xaxis_title="Tempo",
      yaxis_title="Valores",
      colorway=["#1f77b4"],
      showlegend=True,
      **kwargs
  )
  return fig


def plot_period_series(title: str, values: list, **kwargs):
  """
  Cria um gráfico de linha para uma série temporal indexada por períodos.

  Args:
      title (str): Título do gráfico.
      values (list): Lista de valores numéricos da série temporal.
      **kwargs: Argumentos adicionais passados para fig.update_layout().

  Returns:
      go.Figure: Objeto Figure do Plotly com o gráfico da série temporal.

  Examples:
      >>> values = [10, 15, 12, 18, 20, 16, 14]
      >>> fig = plot_period_series("Série por Períodos", values)
      >>> fig.show()
  """
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=list(range(len(values))),
                y=values, mode='lines', name='Série Temporal'))
  fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4'],
      showlegend=True,
      **kwargs
  )
  return fig


def plot_forecast(title: str, y_val: list, y_pred: list, **kwargs):
  """
  Cria um gráfico comparativo entre valores reais e previstos.

  Plota duas linhas sobrepostas para comparar visualmente os valores
  reais com as previsões do modelo.

  Args:
      title (str): Título do gráfico.
      y_val (list): Lista com valores reais da série temporal.
      y_pred (list): Lista com valores previstos pelo modelo.
      **kwargs: Argumentos adicionais passados para fig.update_layout().

  Returns:
      go.Figure: Objeto Figure do Plotly com gráfico de comparação.

  Examples:
      >>> y_real = [10, 12, 15, 18, 20]
      >>> y_previsto = [9, 13, 14, 19, 21]
      >>> fig = plot_forecast("Previsão vs Reality", y_real, y_previsto)
      >>> fig.show()
  """
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=list(range(len(y_val))),
                y=y_val, mode='lines', name='Valores Reais'))
  fig.add_trace(go.Scatter(x=list(range(len(y_pred))),
                y=y_pred, mode='lines', name='Valores Previsto'))
  fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4', '#ff7f0e'],
      showlegend=True,
      height=600,
      **kwargs
  )
  return fig


def plot_forecast_statistics(title: str, y_val: list, y_pred: list, **kwargs):
  """
  Cria um gráfico de barras comparando estatísticas descritivas.

  Compara métricas estatísticas (média, mediana, desvio padrão, máximo, mínimo)
  entre valores reais e previstos usando gráfico de barras agrupadas.

  Args:
      title (str): Título do gráfico.
      y_val (list): Lista com valores reais da série temporal.
      y_pred (list): Lista com valores previstos pelo modelo.
      **kwargs: Argumentos adicionais passados para fig.update_layout().

  Returns:
      go.Figure: Objeto Figure do Plotly com gráfico de barras comparativo.

  Examples:
      >>> y_real = [10, 12, 15, 18, 20, 8, 25]
      >>> y_previsto = [9, 13, 14, 19, 21, 7, 24]
      >>> fig = plot_forecast_statistics("Estatísticas Comparativas", y_real, y_previsto)
      >>> fig.show()
  """
  metrics = ['Média', 'Mediana', 'Desvio Padrão', 'Máximo', 'Mínimo']
  y_val_values = [np.nanmean(y_val), np.nanmedian(
      y_val), np.nanstd(y_val), np.nanmax(y_val), np.nanmin(y_val)]
  y_pred_values = [np.nanmean(y_pred), np.nanmedian(
      y_pred), np.nanstd(y_pred), np.nanmax(y_pred), np.nanmin(y_pred)]
  fig = go.Figure()
  fig.add_trace(go.Bar(x=metrics, y=y_val_values,
                name='Valores Reais', marker_color='#1f77b4'))
  fig.add_trace(go.Bar(x=metrics, y=y_pred_values,
                name='Valores Previsto', marker_color='#ff7f0e'))
  fig.update_layout(
      title=title,
      yaxis_title='Valores',
      barmode='group',
      height=500,
      **kwargs
  )
  return fig


def plot_decomposition(
    title: str,
    trend: pd.Series,
    seasonal: pd.Series,
    resid: pd.Series,
    **kwargs
):
  """
  Cria um gráfico de decomposição de série temporal em subplots.

  Exibe a decomposição da série temporal em três componentes:
  tendência, sazonalidade e resíduos, cada um em um subplot separado.

  Args:
      title (str): Título principal do gráfico.
      trend (pd.Series): Série com o componente de tendência.
      seasonal (pd.Series): Série com o componente sazonal.
      resid (pd.Series): Série com os resíduos.
      **kwargs: Argumentos adicionais passados para fig.update_layout().

  Returns:
      go.Figure: Objeto Figure do Plotly com subplots da decomposição.

  Examples:
      >>> # Assumindo decomposição já realizada
      >>> fig = plot_decomposition(
      ...     "Decomposição da Série",
      ...     trend_series,
      ...     seasonal_series,
      ...     residual_series
      ... )
      >>> fig.show()
  """
  fig = make_subplots(
      rows=3, cols=1, shared_xaxes=True,
      subplot_titles=("Tendência", "Sazonalidade", "Resíduos")
  )
  fig.add_trace(
      go.Scatter(x=trend.index, y=trend, mode="lines",
                 name="Tendência", line=dict(color="orange")),
      row=1, col=1
  )
  fig.add_trace(
      go.Scatter(x=seasonal.index, y=seasonal, mode="lines",
                 name="Sazonalidade", line=dict(color="green")),
      row=2, col=1
  )
  fig.add_trace(
      go.Scatter(x=resid.index, y=resid, mode="lines",
                 name="Resíduos", line=dict(color="red")),
      row=3, col=1
  )
  fig.update_layout(
      height=800,
      width=1000,
      title=title,
      showlegend=True,
      **kwargs
  )
  return fig
