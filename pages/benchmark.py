import streamlit as st
import pandas as pd

df = pd.DataFrame({
  'Posição': [1, 2, 3],
  'Modelo': ['GPT-4', 'Claude 3', 'Gemini Pro'],
  'Pontuação': [100, 95, 90],
  'Organização': ['OpenAI', 'Anthropic', 'Google DeepMind'],
  'Licença': ['Comercial', 'Comercial', 'Comercial'],
})
st.write('### Comparação de desempenho de modelos de linguagem na previsão de séries temporais.')


st.dataframe(
  data=df,
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

st.divider()
st.write('### Observações')

st.divider()
st.write("### Métricas de Avaliação")
