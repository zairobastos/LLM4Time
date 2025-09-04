"""
Módulo para geração e carregamento de prompts de previsão em séries temporais.
"""

from .prompts import PromptType
from .prompts import ZERO_SHOT, FEW_SHOT, COT, COT_FEW
from .formatting import TSFormat, TSType
from .formatter import format


def load_prompt(path: str, **kwargs) -> str:
  """
  Carrega um template de prompt de um arquivo e realiza substituições de variáveis.

  Lê o conteúdo do arquivo especificado por `path` e formata a string com os argumentos
  fornecidos em `kwargs`. É útil para reutilizar prompts de previsão de séries temporais
  com placeholders dinâmicos.

  Args:
      path (str): Caminho para o arquivo de texto contendo o template do prompt.
      **kwargs: Argumentos para substituição de placeholders no template.

  Returns:
      str: Conteúdo do arquivo formatado com os argumentos fornecidos.

  Raises:
      FileNotFoundError: Se o arquivo não for encontrado.
      IOError: Se houver erro ao ler o arquivo.
      KeyError: Se algum placeholder no template não tiver correspondência em `kwargs`.

  Examples:
      >>> load_prompt("templates/zero_shot.txt", train_data="...", periods=7)
  """
  try:
    with open(path, 'r', encoding='utf-8') as file:
      prompt = file.read()
    return prompt.format(**kwargs)
  except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo não encontrado: {path}")
  except IOError as e:
    raise IOError(f"Erro ao ler o arquivo {path}: {e}")
  except KeyError as e:
    raise KeyError(f"Chave de formatação não encontrada: {e}")


def generate(
    train: list[tuple],
    periods: int,
    prompt_type: PromptType,
    ts_format: TSFormat,
    ts_type: TSType
) -> str:
  """
  Gera um prompt de previsão de séries temporais de acordo com o tipo especificado.

  A função prepara os dados de treino no formato e tipo desejados, constrói exemplos
  (quando necessário) e insere essas informações em diferentes templates de prompt
  (ZERO-SHOT, FEW-SHOT, COT, COT-FEW).

  Args:
      train (list[tuple]): Série temporal de treino no formato [(date, value), ...].
      periods (int): Número de períodos a serem previstos.
      prompt_type (PromptType): Tipo de prompt a ser gerado:
          - ZERO_SHOT: sem exemplos.
          - FEW_SHOT: com exemplos de previsões passadas.
          - COT: com raciocínio passo a passo (Chain of Thought).
          - COT_FEW: combinação de exemplos e raciocínio passo a passo.
      ts_format (TSFormat): Formato de serialização da série temporal (ex.: CSV, JSON, Markdown).
      ts_type (TSType): Tipo de codificação dos valores (ex.: NUMERIC, TEXTUAL).

  Returns:
      str: Prompt formatado pronto para ser usado em um modelo de linguagem.

  Raises:
      ValueError:
          - Se `prompt_type` for inválido.
          - Se `prompt_type` for FEW_SHOT ou COT_FEW e houver menos de 96 observações em `train`.

  Examples:
      >>> generate(
      ...     train=[("2025-01-01", 100), ("2025-01-02", 200)],
      ...     periods=7,
      ...     prompt_type=PromptType.ZERO_SHOT,
      ...     ts_format=TSFormat.CSV,
      ...     ts_type=TSType.NUMERIC
      ... )
  """
  num_periods_train = len(train)
  num_periods_forecast = periods
  num_periods_example = periods
  start_forecast_example = format(train[:4], ts_format, ts_type)
  output_example = format(train[:24], ts_format, ts_type)
  train_data = format(train, ts_format, ts_type)

  base_kwargs = {
      "num_periods_train": num_periods_train,
      "num_periods_forecast": num_periods_forecast,
      "num_periods_example": num_periods_example,
      "start_forecast_example": start_forecast_example,
      "output_example": output_example,
      "train_data": train_data,
      "timestamp": "hora"
  }

  if prompt_type == PromptType.ZERO_SHOT:
    return ZERO_SHOT.format(**base_kwargs)

  elif prompt_type == PromptType.FEW_SHOT or prompt_type == PromptType.COT_FEW:
    # Verificação se há dados suficientes
    if num_periods_train < 96:
      raise ValueError(
          "Para FEW-SHOT ou COT-FEW deve conter pelo menos 96 elementos.")

    window1 = format(train[:24], ts_format, ts_type)
    window2 = format(train[24:48], ts_format, ts_type)
    window3 = format(train[48:72], ts_format, ts_type)
    window4 = format(train[72:96], ts_format, ts_type)

    windows = {
        "window1": window1,
        "window2": window2,
        "window3": window3,
        "window4": window4,
    }
    base_kwargs.update(windows)

    if prompt_type == PromptType.FEW_SHOT:
      return FEW_SHOT.format(**base_kwargs)
    else:
      return COT_FEW.format(**base_kwargs)

  elif prompt_type == PromptType.COT:
    return COT.format(**base_kwargs)

  else:
    raise ValueError(f"Tipo de prompt inválido: {prompt_type}")
