from datetime import date
import pandas as pd
from pathlib import Path

class DadosModel:
	def __init__(self, dataset: str, data_inicio: date, data_fim: date, qtd_periodos: int):
		"""Classe para manipulação de dados.

		Args:
			dataset (str): Nome do arquivo CSV do dataset.
			data_inicio (date): Data de início do recorte dos dados.
			data_fim (date): Data de fim do recorte dos dados.
			qtd_periodos (int): Quantidade de períodos futuros a prever.
		"""
		self.dataset = dataset
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.qtd_periodos = qtd_periodos
		diretorio_do_script = Path(__file__).resolve().parent
		self.caminho =  diretorio_do_script.parent.parent / 'data' / self.dataset

	def exibir_dados(self) -> pd.DataFrame:
		"""Carrega o dataset do arquivo CSV."""
		try:
			print(f"[INFO] Lendo dados do caminho: {self.caminho}")
			dataset = pd.read_csv(self.caminho)
			print(f"[INFO] Dados carregados com sucesso do arquivo: {self.caminho}")
			return dataset
		except FileNotFoundError as e:
			print(f"[ERROR] Arquivo não encontrado: {e}")
			return None
		except pd.errors.EmptyDataError as e:
			print(f"[ERROR] Arquivo vazio: {e}")
			return None

	def selecao_periodo(self) -> tuple[pd.DataFrame, pd.DataFrame]:
		"""Seleciona os dados entre as datas de início e fim e os dados futuros a prever."""
		try:
			dataset = self.exibir_dados()
			if dataset is None or dataset.empty:
				raise ValueError("O dataset está vazio ou não foi carregado corretamente.")
			if self.data_inicio > self.data_fim:
				raise ValueError("A data de início não pode ser maior que a data de fim.")

			df = dataset.query("date >= @self.data_inicio and date <= @self.data_fim")
			df_exatos = dataset.query("date > @self.data_fim")
			return df, df_exatos[:self.qtd_periodos]
		except ValueError as e:
			print(f"[ERROR] {e}")
			return None, None
		except Exception as e:
			print(f"[ERROR] Ocorreu um erro inesperado: {e}")
			return None, None

	def dados_prompt(self) -> tuple[list[float], list[float]]:
		"""Retorna os dados do período selecionado e os valores exatos a prever como listas."""
		try:
			dataset, df_exatos = self.selecao_periodo()
			if dataset is None or df_exatos is None:
				raise ValueError("Os dados não foram carregados corretamente.")
			if dataset.empty or df_exatos.empty:
				raise ValueError("Os dados estão vazios.")

			print(f"[INFO] Dados entre {self.data_inicio} e {self.data_fim} carregados com sucesso.")
			dados_prompt = list(zip(dataset['date'].astype(str), dataset['value'].round(3)))
			dados_exatos = df_exatos['value'].round(3)
			return dados_prompt, dados_exatos
		except ValueError as e:
			print(f"[ERROR] {e}")
			return None, None
		except Exception as e:
			print(f"[ERROR] Ocorreu um erro inesperado: {e}")
			return None, None
