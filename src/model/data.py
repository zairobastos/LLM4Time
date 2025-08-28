import pandas as pd
from pathlib import Path
from datetime import date

class Data:
  def __init__(self, dataset:str, start_date:date, end_date:date, periods:int):
    """
    Classe para manipulação de dados.

    Args:
      dataset (str): Nome do arquivo CSV do dataset.
      start_date (date): Data de início do recorte dos dados.
      end_date (date): Data de fim do recorte dos dados.
      periods (int): Quantidade de períodos futuros a prever.
    """
    self.dataset = dataset
    self.start_date = start_date
    self.end_date = end_date
    self.periods = periods

  @staticmethod
  def read_csv(dataset: str) -> pd.DataFrame:
    """Lê um arquivo CSV do caminho especificado e retorna um DataFrame."""
    dir = Path(__file__).resolve().parent
    path =  dir.parent.parent / 'uploads' / dataset

    try:
      print(f"[INFO] Lendo dados do caminho: {path}")
      df = pd.read_csv(path)
      print(f"[INFO] Dados carregados com sucesso do arquivo: {path}")
      return df
    except FileNotFoundError as e:
      print(f"[ERROR] Arquivo não encontrado: {e}")
      return None
    except pd.errors.EmptyDataError as e:
      print(f"[ERROR] Arquivo vazio: {e}")
      return None

  def period_selection(self) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Seleciona os dados entre as datas de início e fim e os dados futuros a prever."""
    try:
      dataset = Data.read_csv(self.dataset)
      if dataset is None or dataset.empty:
        raise ValueError("O dataset está vazio ou não foi carregado corretamente.")
      if self.start_date > self.end_date:
        raise ValueError("A data de início não pode ser maior que a data de fim.")

      df_window = dataset.query("date >= @self.start_date and date <= @self.end_date")
      df_true = dataset.query("date > @self.end_date")
      return df_window, df_true[:self.periods]
    except ValueError as e:
      print(f"[ERROR] {e}")
      return None, None
    except Exception as e:
      print(f"[ERROR] Ocorreu um erro inesperado: {e}")
      return None, None

  def prompt(self) -> tuple[list[float], list[float]]:
    """Retorna os dados do período selecionado e os valores exatos a prever como listas."""
    try:
      df_window, df_true = self.period_selection()
      if df_window is None or df_true is None:
        raise ValueError("Os dados não foram carregados corretamente.")
      if df_window.empty or df_true.empty:
        raise ValueError("Os dados estão vazios.")

      print(f"[INFO] Dados entre {self.start_date} e {self.end_date} carregados com sucesso.")
      window = list(zip(df_window['date'].astype(str), df_window['value'].round(3)))
      y_true = df_true['value'].round(3).tolist()
      return window, y_true
    except ValueError as e:
      print(f"[ERROR] {e}")
      return None, None
    except Exception as e:
      print(f"[ERROR] Ocorreu um erro inesperado: {e}")
      return None, None
