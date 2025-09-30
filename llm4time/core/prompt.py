"""
Módulo para geração e carregamento de prompts de previsão em séries temporais.
"""

from .prompts import PromptType
from .prompts import ZERO_SHOT, FEW_SHOT, COT, COT_FEW
from .formatting import TSFormat, TSType
from .formatter import format
from .data import Sampling
from .data.sampling import frontend, backend, random, uniform
from .evaluate.statistics import Statistics
import pandas as pd


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
    ts_type: TSType,
    sampling: Sampling = None,
    num_examples: int = 0,
    template: str = None,
    **kwargs
) -> str:
  """
  Gera um prompt de previsão de séries temporais de acordo com o tipo especificado.

  A função prepara os dados de treino no formato e tipo desejados, constrói exemplos
  de acordo com a estratégia de amostragem especificada e insere essas informações
  em diferentes templates.

  Args:
      train (list[tuple]): Série temporal de treino no formato [(date, value), ...].
      periods (int): Número de períodos a serem previstos.
      prompt_type (PromptType): Tipo de prompt a ser gerado:
          - ZERO_SHOT: Sem exemplos.
          - FEW_SHOT: Com exemplos de previsões passadas.
          - COT: Com raciocínio passo a passo (Chain of Thought).
          - COT_FEW: Combinação de exemplos e raciocínio passo a passo.
          - CUSTOM: Se desejar utilizar um prompt customizado.
      ts_format (TSFormat): Formato de serialização da série temporal (ex.: CSV, JSON, Markdown).
      ts_type (TSType): Tipo de codificação dos valores (ex.: NUMERIC, TEXTUAL).
      sampling (Sampling, opcional): Estratégia de amostragem dos dados de exemplo.
                                     Padrão: Sampling.FRONTEND.
      num_examples (int, opcional): Quantidade de exemplos a serem gerados.
                                    Padrão: 0.
      template (str, opcional): Prompt customizado se `prompt_type` for CUSTOM.
                                    Padrão: None.
      **kwargs: Se desejar inserir chaves adicionais ao prompt ou substituir
                as chaves padrão.

  Returns:
      str: Prompt formatado pronto para ser usado em um modelo de linguagem.

  Raises:
      ValueError:
          - Se `prompt_type` for inválido.
          - Se `prompt_type` for CUSTOM e `template` for None.
          - Se `num_examples` for maior que 0 e não houver períodos
            suficientes para os exemplos solicitados.

  Examples:
      >>> generate(
      ...     train=[("2025-01-01", 100), ("2025-01-02", 200)],
      ...     periods=7,
      ...     prompt_type=PromptType.ZERO_SHOT,
      ...     ts_format=TSFormat.CSV,
      ...     ts_type=TSType.NUMERIC
      ... )
  """
  if prompt_type == PromptType.CUSTOM and template is None:
    raise ValueError(f"Para o tipo CUSTOM é obrigatório um template.")

  n_periods_input = len(train)
  n_periods_forecast = periods
  n_periods_example = periods

  df = pd.DataFrame(train, columns=['date', 'value'])
  stats = Statistics(df['value'])
  stl = stats.trend_seasonality(df)

  base_kwargs = {
      "input": format(train, ts_format, ts_type),
      "input_example": format(train[:4], ts_format, ts_type),
      "output_example": format(train[:n_periods_example], ts_format, ts_type),
      "n_periods_input": n_periods_input,
      "n_periods_forecast": n_periods_forecast,
      "n_periods_example": n_periods_example,
      "mean": stats.mean,
      "median": stats.median,
      "std": stats.std,
      "min": stats.min,
      "max": stats.max,
      "first_quartile": stats.first_quartile,
      "third_quartile": stats.third_quartile,
      "trend_strength": stl[3],
      "seasonality_strength":  stl[4],
  }
  base_kwargs.update(kwargs)

  min_required = n_periods_forecast * 2 * num_examples
  if n_periods_input < min_required:
    raise ValueError(
        f"Para o número de exemplos solicitado é necessário pelo menos {min_required} períodos.")

  if sampling is not None:
    sampling_map = {
        Sampling.FRONTEND: frontend,
        Sampling.BACKEND: backend,
        Sampling.RANDOM: random,
        Sampling.UNIFORM: uniform,
    }
    if sampling not in sampling_map:
      raise ValueError(f"Estratégia de amostragem inválida: {sampling}")
    samples = sampling_map[sampling](
        train, window_size=n_periods_example, num_samples=num_examples)
    examples = [
        f"Exemplo {i}:\n"
        f"Entrada (histórico):\n{format(history, ts_format, ts_type)}\n"
        f"Saída (previsto):\n<out>\n{format(forecast, ts_format, ts_type)}\n</out>\n"
        for i, (history, forecast) in enumerate(samples, 1)]
    base_kwargs.update({"examples": "\n".join(examples)})

  prompt_map = {
      PromptType.ZERO_SHOT: ZERO_SHOT,
      PromptType.FEW_SHOT: FEW_SHOT,
      PromptType.COT_FEW: COT_FEW,
      PromptType.COT: COT,
      PromptType.CUSTOM: template,
  }
  if prompt_type not in prompt_map:
    raise ValueError(f"Tipo de prompt inválido: {prompt_type}")
  try:
    return prompt_map[prompt_type].format(**base_kwargs)
  except KeyError as e:
    raise ValueError(f"Chave {e} não definida.")
