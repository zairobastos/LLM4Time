from enum import Enum

from src.prompts.zero_shot import ZERO_SHOT
from src.prompts.cot import COT
from src.prompts.few_shot import FEW_SHOT
from src.prompts.cot_few import COT_FEW

from src.model.format import TSFormat, TSType, format_timeseries

class PromptType(str, Enum):
  ZERO_SHOT = 'ZERO_SHOT'
  FEW_SHOT = 'FEW_SHOT'
  COT = 'COT'
  COT_FEW = 'COT_FEW'

class PromptModel:
  def __init__(
      self, window:list, periods:int, prompt_type:PromptType,
      ts_format:TSFormat = TSFormat.CSV, ts_type:TSType = TSType.NUMERIC
  ):
    """
    Classe responsável por gerar prompts com base em um tipo definido.

    Args:
      window (list): Lista com dados de entrada.
      periods (int): Número de dias a serem previstos.
      prompt_type (PromptType): Tipo do prompt (ZERO_SHOT, FEW_SHOT, etc.)
      ts_format (TSFormat): Formato dos dados temporais (ARRAY, CSV, etc.).
      ts_type (TSType): Tipo de série (NUMERIC, TEXTUAL).
    """

    if not isinstance(periods, int) or periods <= 0:
      raise ValueError("periods deve ser um inteiro positivo.")

    self.window = window
    self.num_periods_window = len(self.window)
    self.num_periods_forecast = periods
    self.prompt_type = prompt_type
    self.ts_format = ts_format
    self.ts_type = ts_type

  def generate(self) -> str:
    """
    Gera o prompt formatado com base no tipo escolhido.

    Returns:
      str: Prompt formatado para entrada no modelo.
    """
    print(f"[INFO] Formato dos dados: {self.ts_format.value}")
    print(f"[INFO] Tipo de série: {self.ts_type.value}")

    start_forecast = format_timeseries(self.window[:4], self.ts_format, self.ts_type)
    output_example = format_timeseries(self.window[:24], self.ts_format, self.ts_type)
    window = format_timeseries(self.window, self.ts_format, self.ts_type)

    base_kwargs = {
      "start_forecast": start_forecast,
      "num_periods_window": self.num_periods_window,
      "num_periods_forecast": self.num_periods_forecast,
      "num_periods_example": self.num_periods_forecast,
      "output_example": output_example,
      "input": window,
      "timestamp": "hora",
    }

    if self.prompt_type == PromptType.ZERO_SHOT:
      print(f"[INFO] Prompt ZERO-SHOT gerado com {self.num_periods_window} períodos.")
      return ZERO_SHOT.format(**base_kwargs)

    elif self.prompt_type == PromptType.FEW_SHOT or self.prompt_type == PromptType.COT_FEW:
      print(f"[INFO] Prompt FEW-SHOT ou COT-FEW gerado com {self.num_periods_window} períodos.")
      # Verificação se há dados suficientes
      if self.num_periods_window < 96:
        raise ValueError("Para FEW-SHOT ou COT-FEW, window deve conter pelo menos 96 elementos.")

      period1 = format_timeseries(self.window[:24], self.ts_format, self.ts_type)
      period2 = format_timeseries(self.window[24:48], self.ts_format, self.ts_type)
      period3 = format_timeseries(self.window[48:72], self.ts_format, self.ts_type)
      period4 = format_timeseries(self.window[72:96], self.ts_format, self.ts_type)

      exemplos = {
        "period1": period1,
        "period2": period2,
        "period3": period3,
        "period4": period4,
      }
      base_kwargs.update(exemplos)

      if self.prompt_type == PromptType.FEW_SHOT:
        return FEW_SHOT.format(**base_kwargs)
      else:
        return COT_FEW.format(**base_kwargs)

    elif self.prompt_type == PromptType.COT:
      print(f"[INFO] Prompt COT gerado com {self.num_periods_window} períodos.")
      return COT.format(**base_kwargs)

    else:
      raise ValueError(f"Tipo de prompt inválido: {self.prompt_type}")
