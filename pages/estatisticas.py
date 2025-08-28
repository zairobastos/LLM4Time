import streamlit as st
from src.view.header import Header
from src.view.graph import Graph
import pandas as pd
import os


with st.sidebar:
  datasets = os.listdir('uploads')
  dataset = st.selectbox('Database', datasets)

  confirm = st.button(
    label='Gerar Estatísticas',
    key='generate_statistics',
    type='primary',
    use_container_width=True
  )

if confirm:
  df = pd.read_csv(f"uploads/{dataset}")

  st.write("### Descrição")
  Header.statistics(dataset=dataset, df=df)

  st.write("### Base de Dados")
  st.dataframe(df, use_container_width=True)

  Graph.time_series(title="Valores ao Longo do Tempo", df=df)
