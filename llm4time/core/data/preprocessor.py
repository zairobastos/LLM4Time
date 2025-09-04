"""
Módulo para preprocessamento de dados de séries temporais.

Este módulo fornece funcionalidades essenciais para preparação e estruturação
de dados de séries temporais, incluindo seleção e padronização de colunas,
normalização de frequência temporal, e divisão de dados para treino e validação.
"""

import pandas as pd


def select_columns(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    duplicates: str | None = "first"
) -> pd.DataFrame:
  """
  Seleciona e renomeia colunas de um DataFrame para uma série temporal padrão.

  Realiza os seguintes passos:
    1. Seleciona apenas as colunas `date_col` e `value_col`.
    2. Renomeia `date_col` para "date" e `value_col` para "value".
    3. Converte a coluna "date" para datetime.
    4. Ordena o DataFrame pela coluna "date" em ordem crescente.
    5. Reseta os índices do DataFrame resultante.

  Args:
      df (pd.DataFrame): DataFrame original contendo as colunas de interesse.
      date_col (str): Nome da coluna que contém as datas.
      value_col (str): Nome da coluna que contém os valores.
      duplicates : str | None
          Como tratar dados duplicados:
          - "first" → mantém a primeira ocorrência.
          - "last" → mantém a última ocorrência.
          - "sum" → soma os valores duplicados.
          - None → não remove duplicatas.

  Returns:
      pd.DataFrame: DataFrame padronizado com colunas `date` e `value`, ordenado por `date`.

  Examples:
      >>> df = pd.DataFrame({
      ...     "col1": ["2025-01-03", "2025-01-01", "2025-01-02"],
      ...     "col2": [30, 10, 20],
      ...     "col3": ["a", "b", "c"]
      ... })
      >>> select_columns(df, date_col="col1", value_col="col2")
              date  value
      0 2025-01-01     10
      1 2025-01-02     20
      2 2025-01-03     30
  """
  df = df[[date_col, value_col]].copy()
  # Renomeia as colunas para "date" e "value"
  df.rename(columns={date_col: "date", value_col: "value"}, inplace=True)
  # Ordena pela coluna "date" em ordem crescente
  df["date"] = pd.to_datetime(df["date"])
  df = df.sort_values('date', ascending=True).reset_index(drop=True)

  if duplicates == "first":
    df = df.drop_duplicates(subset=[date_col], keep="first")
  elif duplicates == "last":
    df = df.drop_duplicates(subset=[date_col], keep="last")
  elif duplicates == "sum":
    df = df.groupby(date_col, as_index=False)[value_col].sum()

  return df


def normalize(
    df: pd.DataFrame,
    freq: str,
    start: str = None,
    end: str = None
) -> pd.DataFrame:
  """
  Normaliza a série temporal garantindo que todas as datas dentro de um intervalo estejam presentes.

  Cria um intervalo contínuo de datas, baseado nos limites fornecidos ou,
  se não especificados, na menor e maior data da coluna 'date'.
  Datas ausentes são preenchidas com NaN.

  Args:
      df (pd.DataFrame): DataFrame contendo obrigatoriamente a coluna 'date'.
      freq (str): Frequência da série temporal (ex.: 'D' = diário, 'M' = mensal, 'H' = horário).
      start (str, optional): Data inicial do intervalo (ex.: "2020-01" ou "2020-01-01").
                            Se None, usa data mínima em `df["date"]`. Defaults to None.
      end (str, optional): Data final do intervalo (ex.: "2024-12" ou "2024-12-31").
                          Se None, usa data máxima em `df["date"]`. Defaults to None.

  Returns:
      pd.DataFrame: DataFrame expandido para conter todas as datas no intervalo definido,
                    com valores ausentes preenchidos como NaN.

  Examples:
      >>> df = pd.DataFrame({"date": pd.to_datetime(["2021-01-01", "2021-01-03"]), "value": [10, 30]})
      >>> normalize(df, freq="D", start="2021-01-01", end="2021-01-05")
              date  value
      0 2021-01-01   10.0
      1 2021-01-02    NaN
      2 2021-01-03   30.0
      3 2021-01-04    NaN
      4 2021-01-05    NaN
  """
  start_date = pd.to_datetime(start) if start else df["date"].min()
  end_date = pd.to_datetime(end) if end else df["date"].max()

  df_range = pd.date_range(start=start_date, end=end_date, freq=freq)
  df_range = pd.DataFrame({"date": df_range})
  df = pd.merge(df_range, df, on="date", how="left")
  return df


def split(df: pd.DataFrame, start_date: str, end_date: str, periods: int) -> tuple[list[tuple[str, float]], list[float]]:
  """
  Divide uma série temporal em conjunto de treino e validação com base em datas de corte.

  O conjunto de treino contém as observações no intervalo entre `start_date` e `end_date` (inclusive),
  enquanto o conjunto de validação contém as observações após `end_date`, limitado a `periods` valores.

  Args:
      df (pd.DataFrame): DataFrame com colunas obrigatórias 'date' e 'value'.
      start_date (str): Data inicial do período de treino (formato "YYYY-MM-DD").
      end_date (str): Data final do período de treino (formato "YYYY-MM-DD").
      periods (int): Quantidade de valores a considerar no conjunto de validação.

  Returns:
      tuple[list[tuple[str, float]], list[float]]: Tupla contendo:
          - train: Lista de tuplas (date, value) representando o conjunto de treino
          - y_val: Lista de valores (float) do conjunto de validação, limitado a `periods`

  Examples:
      >>> df = pd.DataFrame({
      ...     "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"],
      ...     "value": [10.123, 20.456, 30.789, 40.321]
      ... })
      >>> split(df, start_date="2025-01-01", end_date="2025-01-02", periods=2)
      ([('2025-01-01', 10.123), ('2025-01-02', 20.456)], [30.789, 40.321])

      >>> # Dividindo série com mais períodos de validação disponíveis que solicitados
      >>> split(df, start_date="2025-01-01", end_date="2025-01-01", periods=1)
      ([('2025-01-01', 10.123)], [20.456])
  """
  df_train = df.query("date >= @start_date and date <= @end_date")
  df_val = df.query("date > @end_date")

  train = list(zip(df_train['date'].astype(str), df_train['value'].round(3)))
  y_val = df_val['value'].round(3).tolist()

  return train, y_val[:periods]
