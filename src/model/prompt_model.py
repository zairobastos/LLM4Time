from enum import Enum

from src.prompts.zero_shot import ZERO_SHOT
from src.prompts.cot import COT
from src.prompts.few_shot import FEW_SHOT
from src.prompts.cot_few import COT_FEW

from src.model.format_model import TSFormat, TSType, list_to_string

class PromptType(str, Enum):
	ZERO_SHOT = 'ZERO_SHOT'
	FEW_SHOT = 'FEW_SHOT'
	COT = 'COT'
	COT_FEW = 'COT_FEW'

class PromptModel:
	def __init__(self, lista_prompt:list, tipo_prompt:PromptType, tam_previsao:int, formato_dados:TSFormat = TSFormat.CSV, tipo_serie:TSType = TSType.NUMERIC):
		"""
		Classe responsável por gerar prompts com base em um tipo definido.

		Args:
			lista_prompt (list): Lista com dados de entrada.
			tipo_prompt (PromptType): Tipo de prompt a ser utilizado.
			tam_previsao (int): Número de dias a serem previstos.
			formato_dados (TSFormat): Formato dos dados de entrada.
			tipo_serie (TSType): Tipo de série: 'Numérica' ou 'Textual'.
		"""

		if not isinstance(tam_previsao, int) or tam_previsao <= 0:
			raise ValueError("tam_previsao deve ser um inteiro positivo.")

		self.lista_prompt = lista_prompt
		self.tipo_prompt = tipo_prompt
		self.tam_periodos = len(lista_prompt)
		self.tam_previsao = tam_previsao
		self.formato_dados = formato_dados
		self.tipo_serie = tipo_serie

	def prompt(self) -> str:
		"""
		Gera o prompt formatado com base no tipo escolhido.

		Returns:
			str: Prompt formatado para entrada no modelo.
		"""
		print(f"[INFO] Formato dos dados: {self.formato_dados.value}")
		print(f"[INFO] Tipo de série: {self.tipo_serie.value}")
		inicio_previsao = list_to_string(self.lista_prompt[:4], self.formato_dados, self.tipo_serie)
		exemplo_saida = list_to_string(self.lista_prompt[:24], self.formato_dados, self.tipo_serie)
		dados_prompt = list_to_string(self.lista_prompt, self.formato_dados, self.tipo_serie)

		base_kwargs = {
			"periodos": self.tam_periodos,
			"inicio_previsao": inicio_previsao,
			"saida": self.tam_previsao,
			"exemplo_saida": exemplo_saida,
			"dados_prompt": dados_prompt,
			"n": self.tam_previsao,
		}

		if self.tipo_prompt == PromptType.ZERO_SHOT:
			print(f"[INFO] Prompt ZERO-SHOT gerado com {self.tam_periodos} períodos.")
			return ZERO_SHOT.format(**base_kwargs)

		elif self.tipo_prompt == PromptType.FEW_SHOT or self.tipo_prompt == PromptType.COT_FEW:
			print(f"[INFO] Prompt FEW-SHOT ou COT-FEW gerado com {self.tam_periodos} períodos.")
			# Verificação se há dados suficientes
			if len(self.lista_prompt) < 96:
				raise ValueError("Para FEW-SHOT ou COT-FEW, lista_prompt deve conter pelo menos 96 elementos.")

			periodo1 = list_to_string(self.lista_prompt[:24], self.formato_dados, self.tipo_serie)
			periodo2 = list_to_string(self.lista_prompt[24:48], self.formato_dados, self.tipo_serie)
			periodo3 = list_to_string(self.lista_prompt[48:72], self.formato_dados, self.tipo_serie)
			periodo4 = list_to_string(self.lista_prompt[72:96], self.formato_dados, self.tipo_serie)

			exemplos = {
				"periodo1": periodo1,
				"periodo2": periodo2,
				"periodo3": periodo3,
				"periodo4": periodo4,
			}
			base_kwargs.update(exemplos)

			if self.tipo_prompt == PromptType.FEW_SHOT:
				return FEW_SHOT.format(**base_kwargs)
			else:
				return COT_FEW.format(**base_kwargs)

		elif self.tipo_prompt == PromptType.COT:
			print(f"[INFO] Prompt COT gerado com {self.tam_periodos} períodos.")
			return COT.format(**base_kwargs)

		else:
			raise ValueError(f"Tipo de prompt inválido: {self.tipo_prompt}")
