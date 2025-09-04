import streamlit as st
import pandas as pd


class Statistics:
  """
  Classe especializada em componentes da página 'statistics'.
  """

  @staticmethod
  def header(
      df: pd.DataFrame,
      df_name: str,
      t_strength: float,
      s_strength: float
  ):
    """
    Cria o cabeçalho da página 'statistics'.

    Args:
      df (pd.DataFrame): DataFrame contendo as colunas 'date' e 'value'.
      df_name (str): Base de dados a ser utilizada. Ex: 'ETTH1', 'ETTH2'.
      t_strength (float): Força da tendência.
      s_strength (float): Força da sazonalidade.
    """
    describe = df['value'].describe()
    missing = df['value'].isna().sum()
    missing_percent = (missing / len(df)) * 100

    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 1])
    with col1:
      st.metric(label="Base de Dados", value=df_name)
    with col2:
      st.metric("Total de Dados", len(df))
    with col3:
      st.metric("Mínimo", f"{describe['min']:.2f}")
    with col4:
      st.metric("Máximo", f"{describe['max']:.2f}")
    with col5:
      st.metric("Média", f"{describe['mean']:.2f}")
    with col6:
      st.metric("Dados Ausentes", missing)
    with col7:
      st.metric("Dados Ausentes (%)", f"{missing_percent:.2f}")

    col8, col9, col10, col11, col12, col13 = st.columns(6)
    with col8:
      st.metric("1º Quartil (Q1)", f"{describe['25%']:.2f}")
    with col9:
      st.metric("Mediana", f"{describe['50%']:.2f}")
    with col10:
      st.metric("3º Quartil (Q3)", f"{describe['75%']:.2f}")
    with col11:
      st.metric("Desvio Padrão", f"{describe['std']:.2f}")
    with col12:
      st.metric(label="Força da tendência", value=t_strength)
    with col13:
      st.metric(label="Força da sazonalidade", value=s_strength)
