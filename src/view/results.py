import streamlit as st
from src.model.metrics import Metrics
from src.view.graph import Graph

class Results:
  def __init__(
    self, y_true:list, y_pred:str, total_tokens_prompt:int,
    total_tokens_response:int, response_time:float
  ):
    """
    Classe responsável por exibir os resultados.

    Args:
      y_true (list): Valores exatos.
      y_pred (list): Valores previstos.
      total_tokens_prompt (int): Quantidade de tokens do prompt.
      total_tokens_response (int): Quantidade de tokens da resposta.
      response_time (float): Tempo de resposta.
    """
    self.y_true = y_true
    self.y_pred = y_pred
    self.total_tokens_prompt = total_tokens_prompt
    self.total_tokens_response = total_tokens_response
    self.response_time = response_time

  def show(self):
    st.write('---')
    st.write('### Resultados')
    m = Metrics(y_pred=self.y_pred, y_true=self.y_true)

    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric(label='Tokens Prompt', value=self.total_tokens_prompt)
    with col2:
      st.metric(label='Tokens Resposta', value=self.total_tokens_response)
    with col3:
      st.metric(label='Tempo de Execução', value=f"{self.response_time:.2f} segundos")

    col4, col5, col6 = st.columns(3)
    with col4:
      smape = m.smape()
      st.metric(label='sMAPE', value=smape, help="Erro percentual absoluto médio simétrico (sMAPE).")
    with col5:
      mae = m.mae()
      st.metric(label='MAE', value=mae, help="Erro médio absoluto (MAE).")
    with col6:
      rmse = m.rmse()
      st.metric(label='RMSE', value=rmse, help="Erro quadrático médio (RMSE).")

    st.write("Valores Exatos")
    st.code(self.y_true, language='python', line_numbers=True)

    st.write("Valores Previstos")
    st.code(self.y_pred, language='python', line_numbers=True)

    Graph.forecast_statistics(
      title="Comparação Estatística",
      y_true=self.y_true,
      y_pred=self.y_pred
    )

    Graph.forecast(
      title=f'Série Temporal - Previsão / SMAPE = {smape}',
      y_true=self.y_true,
      y_pred=self.y_pred
    )

    return smape, mae, rmse
