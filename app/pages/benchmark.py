import streamlit as st
from lib.crud import crud_history
import pandas as pd


st.write("## Melhores modelos na previsão de séries temporais")
st.write("Comparação de desempenho de modelos de linguagem na previsão de séries temporais.")

tab1, tab2 = st.tabs(["🏆 Ranking de Modelos", "📈 Métricas de Previsão"])

# ---------------- Tab 1 ----------------
with tab1:
  df2 = pd.DataFrame({
      'Posição': [1, 2, 3],
      'Modelo': ['GPT-4', 'Claude 3', 'Gemini Pro'],
      'Pontuação': [100, 95, 90],
      'Organização': ['OpenAI', 'Anthropic', 'Google DeepMind'],
      'Licença': ['Comercial', 'Comercial', 'Comercial'],
  })

  st.dataframe(
      data=df2,
      column_config={
          'Posição': st.column_config.NumberColumn(
              format="# %s",
              pinned='left',
              help="Posição do modelo no ranking"
          ),
          'Modelo': st.column_config.TextColumn(
              help="Nome do modelo de linguagem"
          ),
          'Pontuação': st.column_config.NumberColumn(
              format="%d",
              help="Pontuação do modelo em tarefas específicas"
          ),
          'Organização': st.column_config.TextColumn(
              help="Organização responsável pelo modelo"
          ),
          'Licença': st.column_config.TextColumn(
              help="Tipo de licença do modelo"
          )
      },
      hide_index=True,
      use_container_width=True
  )

# ---------------- Tab 2 ----------------
with tab2:
  results, col_names = crud_history().select_best_results()

  if results:
    df = pd.DataFrame(results, columns=col_names)

    cols_to_show = [
        "dataset", "model", "temperature", "ts_type", "prompt_type",
        "ts_format", "periods", "response_time", "smape", "mae", "rmse"]
    df = df[[c for c in cols_to_show if c in df.columns]]

    sort_cols = ["dataset", "model", "temperature", "ts_type",
                 "prompt_type", "ts_format", "periods"]
    df = df.sort_values(by=sort_cols, ascending=False)

    columns = {
        "dataset": "Dataset",
        "model": "Modelo",
        "temperature": "Temperatura",
        "ts_type": "Série",
        "prompt_type": "Prompt",
        "ts_format": "Formato",
        "periods": "Períodos",
        "response_time": "Tempo (s)",
        "smape": "sMAPE",
        "mae": "MAE",
        "rmse": "RMSE"
    }
    df = df.rename(columns=columns)

    st.dataframe(
        data=df,
        hide_index=True,
        use_container_width=True
    )
  else:
    st.info("Nenhum resultado experimental encontrado.")
