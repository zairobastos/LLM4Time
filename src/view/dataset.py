import streamlit as st
from src.model.data import Data

class Dataset:
  def __init__(self, dataset:str, start_date:str, end_date:str, periods:int):
    """
    Classe responsável por visualizar o dataset.

    Args:
      dataset (str): Dataset a ser manipulado.
      start_date (str): Data de início do dataset.
      end_date (str): Data de fim do dataset.
      periods (int): Quantidade de períodos a serem previstos.
    """
    self.dataset = dataset
    self.start_date = start_date
    self.end_date = end_date
    self.periods = periods

  def show(self):
    window, _ = Data(dataset=self.dataset, start_date=self.start_date, end_date=self.end_date, periods=self.periods).period_selection()

    st.write('---')
    st.write("#### Dados Selecionados")
    st.dataframe(window, use_container_width=True)

    st.write("#### Estatísticas")
    df = window['value']
    describe = df.describe()
    missing = df.isna().sum()
    missing_percent = (missing / len(df)) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric("Total de Dados", len(window))
    with col2:
      st.metric("Mínimo", f"{describe['min']:.2f}")
    with col3:
      st.metric("Máximo", f"{describe['max']:.2f}")
    with col4:
      st.metric("Média", f"{describe['mean']:.2f}")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
      st.metric("Mediana", f"{describe['50%']:.2f}")
    with col6:
      st.metric("Desvio Padrão", f"{describe['std']:.2f}")
    with col7:
      st.metric("Dados Ausentes", missing)
    with col8:
      st.metric("Dados Ausentes (%)", f"{missing_percent:.2f}")
