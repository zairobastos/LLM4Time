import streamlit as st
from lib.crud import crud_history

# Componentes
from components.benchmark import Benchmark

st.write("## Melhores modelos na previsão de séries temporais")
st.write("Comparação de desempenho de modelos de linguagem na previsão de séries temporais.")

tab1, tab2 = st.tabs(["🏆 Ranking de Modelos", "📈 Melhores Resultados"])

# ---------------- Tab 1 ----------------
with tab1:
  Benchmark.best_models_section()

# ---------------- Tab 2 ----------------
with tab2:
  columns_to_group = ["model", "temperature", "dataset",
                      "start_date", "end_date", "periods",
                      "prompt", "prompt_type", "ts_format",
                      "ts_type", "y_val"]
  results, col_names = crud_history().group_by(columns=columns_to_group)

  if results:
    Benchmark.best_results_section(results, col_names)
  else:
    st.info("Nenhum resultado encontrado.")
