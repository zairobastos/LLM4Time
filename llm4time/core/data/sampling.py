"""
Módulo para amostragem de janelas em séries temporais.

Este módulo fornece diferentes estratégias para criação de pares de janelas
(entrada, saída) a partir de sequências temporais, incluindo seleção sequencial
do início (FRONTEND), do final (BACKEND), posições aleatórias (RANDOM) e
distribuição uniforme (UNIFORM).
"""

import numpy as np


def frontend(data: list[tuple], window_size: int, num_samples: int) -> list:
  """
  Cria janelas sequenciais a partir do início da série temporal.

  Gera pares de janelas (entrada, saída) começando do início dos dados,
  onde cada janela de entrada é seguida imediatamente pela janela de saída.

  Args:
      data (List[Tuple]): Lista de tuplas representando a série temporal.
      window_size (int): Tamanho de cada janela.
      num_samples (int): Número de amostras a serem geradas.

  Returns:
      List[Tuple]: Lista de pares de janelas.

  Examples:
      >>> data = [('2024-01-01', 1.0), ('2024-01-02', 2.0), ('2024-01-03', 3.0),
      ...         ('2024-01-04', 4.0), ('2024-01-05', 5.0), ('2024-01-06', 6.0),
      ...         ('2024-01-07', 7.0), ('2024-01-08', 8.0), ('2024-01-09', 9.0),
      ...         ('2024-01-10', 10.0), ('2024-01-11', 11.0), ('2024-01-12', 12.0)]
      >>> frontend(data, window_size=2, num_samples=2)
      [([('2024-01-01', 1.0), ('2024-01-02', 2.0)], [('2024-01-03', 3.0), ('2024-01-04', 4.0)]),
       ([('2024-01-05', 5.0), ('2024-01-06', 6.0)], [('2024-01-07', 7.0), ('2024-01-08', 8.0)])]
  """
  windows = []
  for i in range(num_samples):
    start_in = i * 2 * window_size
    end_in = start_in + window_size
    start_out = end_in
    end_out = start_out + window_size

    if end_out > len(data):
      break

    input_seq = data[start_in:end_in]
    target_seq = data[start_out:end_out]
    windows.append((input_seq, target_seq))
  return windows


def backend(data: list[tuple], window_size: int, num_samples: int) -> list:
  """
  Cria janelas sequenciais a partir do final da série temporal.

  Gera pares de janelas começando do final dos dados em direção ao início.
  Útil para focar nos dados mais recentes da série temporal.

  Args:
      data (List[Tuple]): Lista de tuplas representando a série temporal.
      window_size (int): Tamanho de cada janela.
      num_samples (int): Número de amostras a serem geradas.

  Returns:
      List[Tuple]: Lista de pares de janelas.

  Examples:
      >>> data = [('2024-01-01', 1.0), ('2024-01-02', 2.0), ('2024-01-03', 3.0),
      ...         ('2024-01-04', 4.0), ('2024-01-05', 5.0), ('2024-01-06', 6.0),
      ...         ('2024-01-07', 7.0), ('2024-01-08', 8.0), ('2024-01-09', 9.0),
      ...         ('2024-01-10', 10.0), ('2024-01-11', 11.0), ('2024-01-12', 12.0)]
      >>> backend(data, window_size=2, num_samples=2)
      [([('2024-01-05', 5.0), ('2024-01-06', 6.0)], [('2024-01-07', 7.0), ('2024-01-08', 8.0)]),
       ([('2024-01-09', 9.0), ('2024-01-10', 10.0)], [('2024-01-11', 11.0), ('2024-01-12', 12.0)])]
  """
  windows = []
  total = len(data) // window_size - 1
  num_samples = min(num_samples, total)

  for i in range(num_samples):
    offset = (num_samples - i) * window_size * 2
    start_in = len(data) - offset
    end_in = start_in + window_size
    start_out = end_in
    end_out = start_out + window_size

    input_seq = data[start_in:end_in]
    target_seq = data[start_out:end_out]
    windows.append((input_seq, target_seq))
  return windows


def random(data: list[tuple], window_size: int, num_samples: int) -> list:
  """
  Cria janelas em posições aleatórias da série temporal.

  Seleciona aleatoriamente posições iniciais para criar pares de janelas.

  Args:
      data (List[Tuple]): Lista de tuplas representando a série temporal.
      window_size (int): Tamanho de cada janela.
      num_samples (int): Número de amostras a serem geradas.

  Returns:
      List[Tuple]: Lista de pares de janelas.

  Examples:
      >>> data = [('2024-01-01', 1.0), ('2024-01-02', 2.0), ('2024-01-03', 3.0),
      ...         ('2024-01-04', 4.0), ('2024-01-05', 5.0), ('2024-01-06', 6.0),
      ...         ('2024-01-07', 7.0), ('2024-01-08', 8.0), ('2024-01-09', 9.0),
      ...         ('2024-01-10', 10.0), ('2024-01-11', 11.0), ('2024-01-12', 12.0)]
      >>> random(data, window_size=2, num_samples=2)
      [([('2024-01-03', 3.0), ('2024-01-04', 4.0)], [('2024-01-05', 5.0), ('2024-01-06', 6.0)]),
       ([('2024-01-04', 4.0), ('2024-01-05', 5.0)], [('2024-01-06', 6.0), ('2024-01-07', 7.0)])]
  """
  windows = []
  max_start = len(data) - 2 * window_size
  if max_start < 0:
    return windows

  starts = sorted(np.random.choice(range(max_start + 1),
                  size=min(num_samples, max_start + 1), replace=False))

  for start in starts:
    end_in = start + window_size
    start_out = end_in
    end_out = start_out + window_size

    input_seq = data[start:end_in]
    target_seq = data[start_out:end_out]
    windows.append((input_seq, target_seq))
  return windows


def uniform(data: list[tuple], window_size: int, num_samples: int, step: int = None) -> list:
  """
  Cria janelas uniformemente distribuídas ao longo da série temporal.

  Distribui as janelas de forma uniforme ao longo de toda a série temporal,
  garantindo cobertura representativa dos dados. Pode usar espaçamento
  linear ou por passo fixo.

  Args:
      data (List[Tuple]): Lista de tuplas representando a série temporal.
      window_size (int): Tamanho de cada janela.
      num_samples (int): Número de amostras a serem geradas.
      step (int, opcional): Tamanho do passo entre janelas. Se None, usa
                            espaçamento linear uniforme. Padrão: None.

  Returns:
      List[Tuple]: Lista de pares de janelas.

  Examples:
      >>> data = [('2024-01-01', 1.0), ('2024-01-02', 2.0), ('2024-01-03', 3.0),
      ...         ('2024-01-04', 4.0), ('2024-01-05', 5.0), ('2024-01-06', 6.0),
      ...         ('2024-01-07', 7.0), ('2024-01-08', 8.0), ('2024-01-09', 9.0),
      ...         ('2024-01-10', 10.0), ('2024-01-11', 11.0), ('2024-01-12', 12.0)]
      >>> uniform(data, window_size=2, num_samples=2)
      [([('2024-01-01', 1.0), ('2024-01-02', 2.0)], [('2024-01-03', 3.0), ('2024-01-04', 4.0)]),
        ([('2024-01-09', 9.0), ('2024-01-10', 10.0)], [('2024-01-11', 11.0), ('2024-01-12', 12.0)])]

      >>> uniform(data, window_size=2, num_samples=3, step=2)
      [([('2024-01-01', 1.0), ('2024-01-02', 2.0)], [('2024-01-03', 3.0), ('2024-01-04', 4.0)]),
        ([('2024-01-03', 3.0), ('2024-01-04', 4.0)], [('2024-01-05', 5.0), ('2024-01-06', 6.0)]),
        ([('2024-01-05', 5.0), ('2024-01-06', 6.0)], [('2024-01-07', 7.0), ('2024-01-08', 8.0)])]
  """
  windows = []
  length = len(data)
  max_start = length - 2 * window_size

  if max_start < 0 or num_samples <= 0:
    return windows

  if step is None:
    starts = [int(x) for x in np.linspace(0, max_start, num_samples)]
  else:
    starts = list(range(0, max_start + 1, step))[:num_samples]

  for start in starts:
    end_in = start + window_size
    start_out = end_in
    end_out = start_out + window_size

    input_seq = data[start:end_in]
    target_seq = data[start_out:end_out]
    windows.append((input_seq, target_seq))
  return windows
