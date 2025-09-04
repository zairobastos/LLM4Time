import streamlit as st
import pandas as pd

# LLM4Time
from llm4time.core.prompts import PromptType
from llm4time.core.evaluate.statistics import Statistics
from llm4time.core.evaluate.metrics import Metrics
from llm4time.visualization import plots


class Home:
  """
  Classe especializada em componentes da página 'home'.
  """

  @staticmethod
  def header(
      model: str,
      dataset: str,
      start_date: str,
      end_date: str,
      periods: int,
      prompt_type: str,
      ts_format: str,
      ts_type: str
  ):
    """
    Cria o cabeçalho da página 'home'.

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
    st.write("### ANÁLISE DOS DADOS")

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
  def train_section(train: list[tuple[str, float]]):
    """
    Renderiza os dados selecionados e suas estatísticas.

    Args:
      train (list[tuple[str, float]]): Lista de tuplas ou números.
      start_date (str): Data de início dos dados a serem analisados.
      end_date (str): Data de fim dos dados a serem analisados.
      periods (int): Quantidade de períodos a serem previstos.
    """
    df_train = pd.DataFrame({
        "date": [d for d, _ in train],
        "value": [v for _, v in train]
    })

    _, _, _, t_strength, s_strength = (
        Statistics.trend_seasonality(df=df_train))

    st.write('---')
    st.write("#### DADOS SELECIONADOS")
    st.dataframe(df_train, use_container_width=True)

    st.write("#### ESTATÍSTICAS")
    df = df_train['value']
    describe = df.describe()
    missing = df.isna().sum()
    missing_percent = (missing / len(df)) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
      st.metric("Total de Dados", len(train))
    with col2:
      st.metric("Mínimo", f"{describe['min']:.2f}")
    with col3:
      st.metric("Máximo", f"{describe['max']:.2f}")
    with col4:
      st.metric("Dados Ausentes", missing)
    with col5:
      st.metric("Dados Ausentes (%)", f"{missing_percent:.2f}")

    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
      st.metric("Média", f"{describe['mean']:.2f}")
    with col7:
      st.metric("Mediana", f"{describe['50%']:.2f}")
    with col8:
      st.metric("Desvio Padrão", f"{describe['std']:.2f}")
    with col9:
      st.metric(label="Força da tendência", value=t_strength)
    with col10:
      st.metric(label="Força da sazonalidade", value=s_strength)

  @staticmethod
  def prompt_section(
      train: list[tuple[str, float]],
      prompt: str,
      prompt_type: PromptType,
  ):
    """
    Exibe o prompt e apresenta uma visualização gráfica dos dados que serão enviados
    ao modelo para análise e previsão.

    Args:
      train (list[tuple[str, float]]): Lista de tuplas ou números.
      prompt (str): O prompt gerado que será enviado ao modelo.
      prompt_type (PromptType): Estratégia de prompting a ser utilizada.
    """
    st.write('---')
    st.write(f'#### PROMPT - {prompt_type.name}')
    st.code(prompt, language='python', line_numbers=True)

    st.plotly_chart(
        plots.plot_period_series(
            title="Série Temporal - Prompt",
            values=[v for _, v in train]
        ),
        use_container_width=True
    )

  @staticmethod
  def results_section(
      y_val: list,
      y_pred: str,
      metrics: Metrics,
      total_tokens_prompt: int,
      total_tokens_response: int,
      response_time: float
  ):
    """
    Processa e exibe os resultados da previsão com métricas de erro
    e visualizações gráficas comparativas.

    Args:
      y_val (list): Valores exatos.
      y_pred (list): Valores previstos.
      metrics (Metrics): Métricas de erro usadas para avaliação.
      total_tokens_prompt (int): Quantidade de tokens do prompt.
      total_tokens_response (int): Quantidade de tokens da resposta.
      response_time (float): Tempo de resposta.
    """
    st.write('---')
    st.write('### RESULTADOS')

    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric(label='Tokens Prompt', value=total_tokens_prompt)
    with col2:
      st.metric(label='Tokens Resposta', value=total_tokens_response)
    with col3:
      st.metric(label='Tempo de Execução',
                value=f"{response_time:.2f} segundos")

    col4, col5, col6 = st.columns(3)
    with col4:
      smape = metrics.smape()
      st.metric(label='sMAPE', value=smape,
                help="Erro percentual absoluto médio simétrico (sMAPE).")
    with col5:
      mae = metrics.mae()
      st.metric(label='MAE', value=mae, help="Erro médio absoluto (MAE).")
    with col6:
      rmse = metrics.rmse()
      st.metric(label='RMSE', value=rmse, help="Erro quadrático médio (RMSE).")

    st.write("Valores Exatos")
    st.code(y_val, language='python', line_numbers=True)

    st.write("Valores Previstos")
    st.code(y_pred, language='python', line_numbers=True)

    st.plotly_chart(
        plots.plot_forecast(
            title=f'Série Temporal - Previsão / SMAPE = {smape}',
            y_val=y_val,
            y_pred=y_pred
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.plot_forecast_statistics(
            title="Comparação Estatística",
            y_val=y_val,
            y_pred=y_pred
        ),
        use_container_width=True,
    )
