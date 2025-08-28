import streamlit as st
import pandas as pd

class Header:
  @staticmethod
  def home(
    model:str, dataset:str, start_date:str, end_date:str,
    periods:int, prompt_type:str, ts_format:str, ts_type:str
  ):
    """
    Cria o cabeçalho da página Home.

    Args:
			model (str): model a ser utilizado. Ex: 'deepseek-r1-distill-qwen-32b'.
			dataset (str): Base de dados a ser utilizada. Ex: 'ETTH1', 'ETTH2'.
			start_date (str): Data de início da previsão. Ex: '2016-07-01'.
			end_date (str): Data de fim da previsão. Ex: '2016-07-02'.
			periods  (int): Número de períodos a serem previstos. Ex: 1.
      prompt_type (PromptType): Tipo do prompt (ZERO_SHOT, FEW_SHOT, etc.)
      ts_format (TSFormat): Formato dos dados temporais (ARRAY, CSV, etc.).
      ts_type (TSType): Tipo de série (NUMERIC, TEXTUAL).
    """
    st.write("### Análise dos dados")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(label="Base de Dados", value=dataset)
    with col2:
      st.metric(label="Data de Início", value=start_date)
    with col3:
      st.metric(label="Data de Fim", value=end_date)
    with col4:
      st.metric(label="Períodos", value=periods)

    col4, col5, col6, col7 = st.columns(4)
    with col4:
      st.metric(label="Modelo", value=model)
    with col5:
      st.metric(label="Prompt", value=prompt_type)
    with col6:
      st.metric(label="Formato", value=ts_format)
    with col7:
      st.metric(label="Série Temporal", value=ts_type)

  @staticmethod
  def statistics(dataset:str, df:pd.DataFrame):
    """
    Cria o cabeçalho da página Estatísticas.

    Args:
			dataset (str): Base de dados a ser utilizada. Ex: 'ETTH1', 'ETTH2'.
      df: DataFrame contendo os dados carregados da base.
    """
    describe = df['value'].describe()
    missing = df['value'].isna().sum()
    missing_percent = (missing / len(df)) * 100

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
      st.metric(label="Base de Dados", value=dataset)
    with col2:
      st.metric("Total de Dados", len(df))
    with col3:
      st.metric("Mínimo", f"{describe['min']:.2f}")
    with col4:
      st.metric("Máximo", f"{describe['max']:.2f}")
    with col5:
      st.metric("Média", f"{describe['mean']:.2f}")

    col6, col7, col8, col9, col10, col11 = st.columns(6)
    with col6:
      st.metric("1º Quartil (Q1)", f"{describe['25%']:.2f}")
    with col7:
      st.metric("Mediana", f"{describe['50%']:.2f}")
    with col8:
      st.metric("3º Quartil (Q3)", f"{describe['75%']:.2f}")
    with col9:
      st.metric("Desvio Padrão", f"{describe['std']:.2f}")
    with col10:
      st.metric("Dados Ausentes", missing)
    with col11:
      st.metric("Dados Ausentes (%)", f"{missing_percent:.2f}")
