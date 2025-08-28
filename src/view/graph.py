import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Graph:
  @staticmethod
  def period_series(title:str, values:list):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(values))), y=values, mode='lines', name='Série Temporal'))
    fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4'],
      showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)

  @staticmethod
  def time_series(title:str, df:pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["value"], mode="lines", name="Série Temporal"))
    fig.update_layout(
      title=title,
      xaxis_title="Tempo",
      yaxis_title="Valores",
      colorway=["#1f77b4"],
      showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

  @staticmethod
  def forecast(title:str, y_true:list, y_pred:list, key:int=1):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(y_true))), y=y_true, mode='lines', name='Valores Reais'))
    fig.add_trace(go.Scatter(x=list(range(len(y_pred))), y=y_pred, mode='lines', name='Valores Previsto'))
    fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4', '#ff7f0e'],
      showlegend=True,
      height=600
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

  @staticmethod
  def forecast_statistics(title:str, y_true:list, y_pred:list):
    metrics = ['Média', 'Mediana', 'Desvio Padrão', 'Máximo', 'Mínimo']
    y_true_values = [np.nanmean(y_true), np.nanmedian(y_true), np.nanstd(y_true), np.nanmax(y_true), np.nanmin(y_true)]
    y_pred_values = [np.nanmean(y_pred), np.nanmedian(y_pred), np.nanstd(y_pred), np.nanmax(y_pred), np.nanmin(y_pred)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=metrics, y=y_true_values, name='Valores Reais', marker_color='#1f77b4'))
    fig.add_trace(go.Bar(x=metrics, y=y_pred_values, name='Valores Previsto', marker_color='#ff7f0e'))
    fig.update_layout(
      title=title,
      yaxis_title='Valores',
      barmode='group',
      height=500
    )
    st.plotly_chart(fig, use_container_width=True)
