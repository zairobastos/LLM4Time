import streamlit as st
from components.statistics import Statistics
from utils.paths import abspath
import pandas as pd
import os

# LLM4Time
from llm4time.core.evaluate.statistics import Statistics as Stats
from llm4time.visualization import plots


with st.sidebar:
  datasets = os.listdir(abspath('uploads'))
  dataset = st.selectbox('Base de Dados', datasets)

  confirm = st.button(
      label='Gerar Estatísticas',
      key='generate_statistics',
      type='primary',
      use_container_width=True
  )

if not confirm:
  pass

elif not dataset:
  st.toast("Dataset não selecionado. Selecione um antes de continuar.",
           icon="⚠️")

elif dataset:
  df = pd.read_csv(abspath(f"uploads/{dataset}"))

  trend, seasonal, resid, t_strength, s_strength = (
      Stats.trend_seasonality(df))

  st.write("### Descrição")
  Statistics.header(
      df,
      df_name=dataset,
      t_strength=t_strength,
      s_strength=s_strength)

  st.write("### Base de Dados")
  st.dataframe(df, use_container_width=True)

  st.plotly_chart(
      plots.plot_time_series(title="Valores ao Longo do Tempo", df=df),
      use_container_width=True
  )

  st.plotly_chart(
      plots.plot_decomposition(
          title="Decomposição da Série Temporal (STL)",
          trend=trend,
          seasonal=seasonal,
          resid=resid
      ),
      use_container_width=True
  )
