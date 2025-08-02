import streamlit as st
from datetime import date
import os
import pandas as pd

#componentes
from src.view.header import Header
from src.view.dataset import Dataset
from src.view.prompt import Prompt
from src.view.resultados import Resultados

#Banco de dados e API
from database.crud_database import Crud
from api.api import API

from src.model.format_model import TSFormat, TSType, string_to_list


with st.sidebar:
	st.write(" ### 🔍 Parâmetros da Busca")

	lista_datasets = os.listdir('data')

	dataset = st.selectbox('Base de Dados', lista_datasets)
	with open('./database/modelos.txt', 'r') as f:
		modelos = f.read().splitlines()
	modelo = st.selectbox('Modelo', modelos, index=0, help='Escolha o modelo a ser utilizado. O modelo deepseek-r1-distill-qwen-32b é o mais avançado e pode fornecer melhores resultados, mas também é mais pesado e pode levar mais tempo para gerar respostas.')
	temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help='A temperatura controla a aleatoriedade da resposta do modelo. Valores mais altos resultam em respostas mais criativas e variados.')
	st.write('---')
	st.write(f"#### ⚙️ Configurações do Prompt - {dataset}")

	df = pd.read_csv(f'data/{dataset}')
	data_min = pd.to_datetime(df['date']).min().date()
	data_max = pd.to_datetime(df['date']).max().date()

	valor_default_inicio = data_min
	valor_default_fim = min(data_min + pd.Timedelta(days=1), data_max)

	data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=valor_default_inicio)
	data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=valor_default_fim)

	periodos = st.slider(label='Períodos', min_value=1, max_value=96, value=24, step=1, help='Número de períodos a serem previstos. Cada período representa 1 hora de previsão.')
	tipo_prompt = st.radio(label='Prompt', options=['ZERO_SHOT', 'FEW_SHOT', 'COT', 'COT_FEW'], index=0, help='Escolha o tipo de prompt a ser utilizado')

	tipo_serie = st.radio(label='Tipo de Série', options=list(TSType), index=0, format_func=lambda f: f.name, help='Escolha o tipo de série temporal. A série numérica os valores são passados como números, enquanto a série textual os valores são passados como texto. A série textual pode ser mais lenta para gerar respostas, mas pode fornecer resultados mais precisos em alguns casos.')
	formato_dados = st.selectbox(label='Formato dos Dados', options=list(TSFormat), index=0, format_func=lambda f: f.name, help='Formato de apresentação dos dados para o modelo. Diferentes formatos podem influenciar a performance do modelo.')

	confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary', use_container_width=True)

if confirma:
	Header(dataset=dataset, data_fim=str(data_fim), data_inicio=str(data_inicio), modelo=modelo, periodos=periodos, tipo_prompt=tipo_prompt, tipo_serie=tipo_serie.name).header()
	Dataset(dataset=dataset, data_inicio=str(data_inicio), data_fim=str(data_fim), qtd_periodos=periodos).exibir_dados()
	prompt, lista_exato = Prompt(dataset=dataset, data_inicio=str(data_inicio), data_fim=str(data_fim), qtd_periodos=periodos, tipo_prompt=tipo_prompt, formato_dados=formato_dados, tipo_serie=tipo_serie).prompt()
	resposta, qtd_tokens_prompt, qtd_tokens_predito, tempo = API(model=modelo, prompt=prompt, temperature=temperatura).resposta_openai()

	resposta = string_to_list(resposta, formato_dados, tipo_serie)
	smape, mae, rmse = Resultados(val_exatos=lista_exato, val_previstos=resposta, qtd_tokens_prompt=qtd_tokens_prompt, qtd_tokens_resposta=qtd_tokens_predito, tempo=tempo).exibir_resultados()

	confirme_insert = Crud().insert(
		data_inicio=data_inicio,
		data_fim=data_fim,
		periodos=periodos,
		modelo=modelo,
		temperatura_modelo=temperatura,
		prompt=prompt,
		tipo_prompt=tipo_prompt,
		valores_exatos=str(lista_exato),
		valores_previstos=str(resposta),
		smape=smape,
		mae=mae,
		rmse=rmse,
		total_tokens_resposta=qtd_tokens_predito,
		total_tokens_prompt=qtd_tokens_prompt,
		total_tokens=qtd_tokens_predito+qtd_tokens_prompt,
		base_dados= dataset
	)
	if confirme_insert:
		st.toast("Análise gerada com sucesso!", icon="✅")
	else:
		st.toast("Erro ao gerar a análise.", icon="🚨")


else:
	st.write('## Confirme a escolha dos parâmetros para gerar a análise.')
	st.image("icons/undraw_search_re_x5gq.svg", width=500)
