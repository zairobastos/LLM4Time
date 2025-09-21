"""
Módulo para operações CRUD na tabela history do banco de dados.
"""

import sqlite3
from ..core.logging import logger


class HistoryNotFoundError(Exception):
  """
  Exceção levantada quando um registro não é encontrado na tabela history.

  Esta exceção é utilizada quando operações tentam acessar registros
  que não existem no banco de dados.
  """
  pass


class CrudHistory:
  """
  Classe para operações CRUD na tabela history.

  Esta classe gerencia todas as operações de banco de dados relacionadas
  ao histórico de experimentos, incluindo inserção, consulta, remoção
  e análise de resultados.

  Attributes:
      connection: Conexão com o banco de dados SQLite.
      cursor: Cursor para execução de comandos SQL.
  """

  def __init__(self, db_path: str = 'database/database.db') -> None:
    """
    Inicializa a conexão com o banco de dados.

    Estabelece conexão com o banco SQLite localizado em './database/database.db'
    e cria um cursor para execução de comandos.

    Args:
        db_path (str, optional): Caminho para o arquivo do banco de dados.
                                 Padrão: 'database/database.db'.
    """
    self.connection = sqlite3.connect(db_path)
    self.cursor = self.connection.cursor()

  def insert(self, **kwargs) -> bool:
    """
    Insere um novo registro na tabela history.

    Args:
        **kwargs: Argumentos nomeados contendo os dados do experimento.
                  Campos aceitos: model, temperature, dataset, start_date,
                  end_date, periods, prompt, prompt_type, ts_format, ts_type,
                  y_val, y_pred, smape, mae, rmse, total_tokens_prompt,
                  total_tokens_response, total_tokens, response_time,
                  mean_val, mean_pred, median_val, median_pred, std_val,
                  std_pred, min_val, min_pred, max_val, max_pred.

    Returns:
        bool: True se a inserção foi bem-sucedida, False caso contrário.
    """
    try:
      values = (
          kwargs.get('model'),
          kwargs.get('temperature'),
          kwargs.get('dataset'),
          kwargs.get('start_date'),
          kwargs.get('end_date'),
          kwargs.get('periods'),
          kwargs.get('prompt'),
          kwargs.get('prompt_type'),
          kwargs.get('examples'),
          kwargs.get('sampling'),
          kwargs.get('ts_format'),
          kwargs.get('ts_type'),
          kwargs.get('y_val'),
          kwargs.get('y_pred'),
          kwargs.get('smape'),
          kwargs.get('mae'),
          kwargs.get('rmse'),
          kwargs.get('total_tokens_prompt'),
          kwargs.get('total_tokens_response'),
          kwargs.get('total_tokens'),
          kwargs.get('response_time'),
          kwargs.get('mean_val'),
          kwargs.get('mean_pred'),
          kwargs.get('median_val'),
          kwargs.get('median_pred'),
          kwargs.get('std_val'),
          kwargs.get('std_pred'),
          kwargs.get('min_val'),
          kwargs.get('min_pred'),
          kwargs.get('max_val'),
          kwargs.get('max_pred')
      )
      self.cursor.execute(
          f"""
        INSERT INTO history (
          model,
          temperature,
          dataset,
          start_date,
          end_date,
          periods,
          prompt,
          prompt_type,
          examples,
          sampling,
          ts_format,
          ts_type,
          y_val,
          y_pred,
          smape,
          mae,
          rmse,
          total_tokens_prompt,
          total_tokens_response,
          total_tokens,
          response_time,
          mean_val,
          mean_pred,
          median_val,
          median_pred,
          std_val,
          std_pred,
          min_val,
          min_pred,
          max_val,
          max_pred
        ) VALUES ({', '.join(['?'] * len(values))})""",
          values
      )
      self.connection.commit()
      logger.info("Dados inseridos com sucesso na tabela history.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao inserir dados na tabela history: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, dataset: str, prompt_types: list[str]) -> list:
    """
    Seleciona registros da tabela history com base em critérios específicos.

    Args:
        dataset (str): Nome do dataset para filtrar os registros.
        prompt_types (list[str]): Lista de tipos de prompt para filtrar.

    Returns:
        list: Lista de tuplas contendo os registros encontrados.
              Lista vazia em caso de erro ou nenhum registro encontrado.

    Examples:
        >>> crud = CrudHistory()
        >>> results = crud.select('sales_data', ['basic', 'advanced'])
    """
    try:
      placeholders = ','.join(['?'] * len(prompt_types))
      query = f"SELECT * FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      params = [dataset] + prompt_types
      self.cursor.execute(query, params)
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      logger.error(f"Erro ao selecionar dados da tabela history: {e}")
      return []
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def group_by(self, columns: list[str]) -> tuple[list, list]:
    """
    Agrupa resultados experimentais pelas colunas especificadas.

    Args:
        columns (list[str]): Lista de nomes de colunas para agrupar e ordenar.

    Returns:
        tuple[list, list]: Tupla contendo:
            - Lista de registros agrupados
            - Lista com nomes das colunas

          Retorna listas vazias em caso de erro.

    Examples:
        >>> crud = CrudHistory()
        >>> grouped_results, col_names = crud.group_by(['model', 'dataset', 'temperature'])
        >>> if grouped_results:
        ...     print(f"Número de registros retornados: {len(grouped_results)}")
    """
    try:
      if not columns:
        raise ValueError("A lista de colunas não pode estar vazia.")

      cols_str = ", ".join(columns)
      query = f"""
            SELECT *
            FROM history
            WHERE smape IS NOT NULL
              AND mae IS NOT NULL
              AND rmse IS NOT NULL
            ORDER BY {cols_str}
        """

      self.cursor.execute(query)
      results = self.cursor.fetchall()
      col_names = [desc[0] for desc in self.cursor.description]

      if not results:
        return [], col_names

      return results, col_names

    except (sqlite3.Error, ValueError) as e:
      logger.error(f"Erro ao agrupar resultados: {e}")
      return [], []
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove(self, id: int) -> bool:
    """
    Remove um registro específico da tabela history pelo ID.

    Args:
        id (int): ID do registro a ser removido.

    Returns:
        bool: True se a remoção foi bem-sucedida, False caso contrário.

    Raises:
        HistoryNotFoundError: Se o registro com o ID especificado não existir.

    Examples:
        >>> crud = CrudHistory()
        >>> success = crud.remove(123)
    """
    try:
      self.cursor.execute("SELECT COUNT(*) FROM history WHERE id = ?", (id,))
      if self.cursor.fetchone()[0] == 0:
        raise HistoryNotFoundError(
            f"[WARNING] Registro com ID {id} não encontrado na tabela history."
        )

      self.cursor.execute("DELETE FROM history WHERE id = ?", (id,))
      self.connection.commit()
      logger.info(
          f"Registro com ID {id} removido com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao remover registro da tabela history: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_many(self, dataset: str, prompt_types: list[str]) -> bool:
    """
    Remove múltiplos registros da tabela history com base em critérios.

    Args:
        dataset (str): Nome do dataset para filtrar registros a serem removidos.
        prompt_types (list[str]): Lista de tipos de prompt para filtrar.

    Returns:
        bool: True se a remoção foi bem-sucedida, False caso contrário.

    Examples:
        >>> crud = CrudHistory()
        >>> success = crud.remove_many('old_dataset', ['type1', 'type2'])
    """
    try:
      if not prompt_types:
        logger.warning(
            "A lista de prompt_types está vazia. Nenhum registro será removido.")
        return False

      placeholders = ','.join(['?'] * len(prompt_types))
      query_count = f"SELECT COUNT(*) FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      self.cursor.execute(query_count, [dataset] + prompt_types)
      count = self.cursor.fetchone()[0]

      if count == 0:
        logger.info("Nenhum registro encontrado para remover.")
        return True

      query_delete = f"DELETE FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      self.cursor.execute(query_delete, [dataset] + prompt_types)
      self.connection.commit()
      logger.info(
          f"{count} registros removidos com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao remover registros da tabela history: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_all(self) -> bool:
    """
    Remove todos os registros da tabela history e reseta o autoincrement.

    Esta operação é irreversível e remove completamente o histórico
    de experimentos, além de resetar o contador de IDs.

    Returns:
        bool: True se a remoção foi bem-sucedida, False caso contrário.

    Examples:
        >>> crud = CrudHistory()
        >>> success = crud.remove_all()  # Remove todo o histórico
    """
    try:
      self.cursor.execute("SELECT COUNT(*) FROM history")
      count = self.cursor.fetchone()[0]
      if count == 0:
        return True

      self.cursor.execute("DELETE FROM history")
      self.cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'history'")
      self.connection.commit()
      logger.info(
          f"{count} registros removidos com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      logger.error(
          f"Erro ao remover todos os registros da tabela history: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()
