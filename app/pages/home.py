import streamlit as st
from components.home import Home
from lib.api import API
from lib.crud import crud_models
from lib.crud import crud_history
from utils.paths import abspath
import pandas as pd
import os

# LLM4Time
from llm4time.core.models import Provider
from llm4time.core.prompts import PromptType
from llm4time.core.formatting import TSFormat, TSType
from llm4time.core.data import preprocessor
from llm4time.core import prompt as pmpt
from llm4time.core.formatter import parse
from llm4time.core.evaluate.metrics import Metrics
from llm4time.core.evaluate.statistics import Statistics


with st.sidebar:
  st.write(f"#### ⚙️ Configurações do Modelo")

  provider = st.selectbox("API", options=list(Provider))
  models = crud_models().select(provider=str(provider))
  models = [model[1] for model in models]

  model = st.selectbox(
      'Modelo', models, index=0,
      help='Escolha o modelo a ser utilizado. O modelo deepseek-r1-distill-qwen-32b é o mais avançado e pode fornecer melhores resultados, mas também é mais pesado e pode levar mais response_time para gerar respostas.')

  temperature = st.slider(
      label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.1,
      help='A temperatura controla a aleatoriedade da resposta do modelo. Valores mais altos resultam em respostas mais criativas e variados.')

  st.write('---')
  datasets = os.listdir(abspath('uploads'))
  dataset = st.selectbox('Base de Dados', datasets)

  if dataset:
    st.write(f"#### ⚙️ Configurações do Prompt")
    df = pd.read_csv(abspath(f'uploads/{dataset}'))
    min_date = pd.to_datetime(df['date']).min().date()
    max_date = pd.to_datetime(df['date']).max().date()

    default_start_date = min_date
    default_end_date = min(min_date + pd.Timedelta(days=1), max_date)

    start_date = st.date_input(
        label='Data de início', max_value=max_date,
        min_value=min_date, value=default_start_date)

    end_date = st.date_input(
        label='Data de término', max_value=max_date,
        min_value=min_date, value=default_end_date)

    periods = st.slider(
        label='Períodos', min_value=1, max_value=96, value=24, step=1,
        help='Número de períodos a serem previstos. Cada período representa 1 hora de previsão.')

    prompt_type = st.selectbox(
        label='Prompt', options=list(PromptType), index=0, format_func=lambda f: f.name,
        help='Escolha o tipo de prompt a ser utilizado.')

    ts_format = st.selectbox(
        label='Formato dos Dados', options=list(TSFormat), index=0, format_func=lambda f: f.name,
        help='Formato de apresentação dos dados para o modelo. Diferentes formatos podem influenciar a performance do modelo.')

    ts_type = st.radio(
        label='Série', options=list(TSType), index=0, format_func=lambda f: f.name,
        help='Na série numérica os valores são passados como [3.662, 3.124, 3.465, 3.609], enquanto na série textual os valores são passados como [3 . 6 6 2, 3 . 1 2 4, 3 . 4 6 5, 3 . 6 0 9].')

  confirm = st.button(
      label='Gerar Análise', type='primary', use_container_width=True,
      help='Clique para gerar a análise de dados')


# ---------------- Validações ----------------

if not confirm:
  st.write('## LLM4Time Pipeline')
  st.write('Siga as etapas de pré-processamento dos dados e configuração do modelo no pipeline abaixo para gerar previsões.\n')
  st.image(abspath("assets/llm4time.svg"), width=750)

elif not model:
  st.toast("Modelo não selecionado. Selecione um antes de continuar.",
           icon="⚠️")

elif not dataset:
  st.toast("Base de dados não selecionada. Selecione uma antes de continuar.",
           icon="⚠️")


# ---------------- Resultado ----------------

else:
  Home.header(
      model=model,
      dataset=dataset,
      start_date=str(start_date),
      end_date=str(end_date),
      periods=periods,
      prompt_type=prompt_type.name,
      ts_format=ts_format.name,
      ts_type=ts_type.name)

  train, y_val = preprocessor.split(
      df,
      start_date=str(start_date),
      end_date=str(end_date),
      periods=periods)

  Home.train_section(train)

  try:
    prompt = pmpt.generate(
        train=train,
        periods=periods,
        prompt_type=prompt_type,
        ts_format=ts_format,
        ts_type=ts_type)

    Home.prompt_section(
        train,
        prompt=prompt,
        prompt_type=prompt_type)

    api = API(model, provider, temperature)

    # y_pred, total_tokens_prompt, total_tokens_response, response_time = (
    #     api.response(prompt))

    y_pred, total_tokens_prompt, total_tokens_response, response_time = (
        API.mock(periods, ts_format, ts_type))

    y_pred = parse(y_pred, ts_format=ts_format, ts_type=ts_type)

    metrics = Metrics(y_val, y_pred)
    stats_val = Statistics(y_val)
    stats_pred = Statistics(y_pred)

    Home.results_section(
        y_val=y_val,
        y_pred=y_pred,
        metrics=metrics,
        total_tokens_prompt=total_tokens_prompt,
        total_tokens_response=total_tokens_response,
        response_time=response_time)

    inserted = crud_history().insert(
        model=model,
        temperature=temperature,
        dataset=dataset,
        start_date=start_date,
        end_date=end_date,
        periods=periods,
        prompt=prompt,
        prompt_type=prompt_type,
        ts_format=ts_format,
        ts_type=ts_type,
        y_val=str(y_val),
        y_pred=str(y_pred),
        smape=metrics.smape(),
        mae=metrics.mae(),
        rmse=metrics.rmse(),
        total_tokens_prompt=total_tokens_prompt,
        total_tokens_response=total_tokens_response,
        total_tokens=total_tokens_prompt+total_tokens_response,
        response_time=response_time,
        mean_val=stats_val.mean(),
        mean_pred=stats_pred.mean(),
        median_val=stats_val.median(),
        median_pred=stats_pred.median(),
        std_val=stats_val.std(),
        std_pred=stats_pred.std(),
        min_val=stats_val.min(),
        min_pred=stats_pred.min(),
        max_val=stats_val.max(),
        max_pred=stats_pred.max()
    )

    if inserted:
      st.toast("Análise gerada com sucesso!", icon="✅")
    else:
      st.error("Erro ao gerar a análise.", icon="🚨")
  except ValueError as e:
    st.toast(e, icon="🚨")
  except:
    st.toast("Houve um erro inesperado durante a previsão.", icon="🚨")
