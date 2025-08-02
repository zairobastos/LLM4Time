import streamlit as st
from src.model.prompt_model import PromptModel, PromptType
from src.model.dados_model import DadosModel
from src.model.format_model import TSFormat, TSType
from src.view.grafico import Grafico

class Prompt:
	def __init__(
		self, dataset:str, data_inicio:str, data_fim:str, qtd_periodos:int, tipo_prompt:PromptType, formato_dados:TSFormat = TSFormat.CSV, tipo_serie:TSType = TSType.NUMERIC):
		"""
		Classe responsável por manipular o dataset.

		Args:
			dataset (str): Dataset a ser manipulado.
			data_inicio (str): Data de início do dataset.
			data_fim (str): Data de fim do dataset.
			qtd_periodos (int): Quantidade de períodos a serem previstos.
			formato_dados (TSFormat): Formato dos dados temporais.
			tipo_serie (TSType): Tipo de série: 'Numérica' ou 'Textual'.
		"""
		self.dataset = dataset
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.qtd_periodos = qtd_periodos
		self.tipo_prompt = tipo_prompt
		self.formato_dados = formato_dados
		self.tipo_serie = tipo_serie

	def prompt(self):
		st.write('---')
		st.write('### Prompt')
		lista_prompt, lista_exatos = DadosModel(dataset=self.dataset, data_inicio=self.data_inicio, data_fim=self.data_fim, qtd_periodos=self.qtd_periodos).dados_prompt()
		prompt = PromptModel(lista_prompt=lista_prompt, tipo_prompt=self.tipo_prompt, tam_previsao=self.qtd_periodos, formato_dados=self.formato_dados, tipo_serie=self.tipo_serie).prompt()
		st.code(
			prompt,
			language='python',
			line_numbers=True,
		)
		Grafico().amostragem([v for _, v in lista_prompt])
		return prompt, lista_exatos
