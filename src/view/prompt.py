import streamlit as st
from src.model.prompt import PromptModel, PromptType
from src.model.data import Data
from src.model.format import TSFormat, TSType
from src.view.graph import Graph

class Prompt:
  def __init__(
    self, dataset:str, start_date:str, end_date:str,
    periods: int, prompt_type:PromptType,
    ts_format:TSFormat=TSFormat.CSV,
    ts_type:TSType=TSType.NUMERIC
  ):
    """
    Classe responsável por manipular o dataset.

    Args:
      dataset (str): Dataset a ser manipulado.
      start_date (str): Data de início do dataset.
      end_date (str): Data de fim do dataset.
      periods (int): Quantidade de períodos a serem previstos.
      prompt_type (PromptType): Tipo do prompt (ZERO_SHOT, FEW_SHOT, etc.)
      ts_format (TSFormat): Formato dos dados temporais (ARRAY, CSV, etc.).
      ts_type (TSType): Tipo de série (NUMERIC, TEXTUAL).
    """
    self.dataset = dataset
    self.start_date = start_date
    self.end_date = end_date
    self.periods = periods
    self.prompt_type = prompt_type
    self.ts_format = ts_format
    self.ts_type = ts_type

  def view(self):
    window, y_true = Data(dataset=self.dataset, start_date=self.start_date, end_date=self.end_date, periods=self.periods).prompt()
    prompt = PromptModel(window=window, periods=self.periods, prompt_type=self.prompt_type, ts_format=self.ts_format, ts_type=self.ts_type).generate()

    st.write('---')
    st.write(f'#### Prompt - {self.prompt_type.name}')
    st.code(prompt, language='python', line_numbers=True)

    Graph.period_series(
      title="Série Temporal - Prompt",
      values=[v for _, v in window]
    )

    return window, y_true, prompt
