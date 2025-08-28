import sqlite3

# ---------------- Exceções ----------------

class HistoryNotFoundError(Exception):
  pass

# ---------------- CRUD ----------------

class CrudHistory:
  def __init__(self):
    self.connection = sqlite3.connect('./database/database.db')
    self.cursor = self.connection.cursor()

  def insert(self, **kwargs) -> bool:
    """Insere um registro na tabela history."""
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
        kwargs.get('ts_format'),
        kwargs.get('ts_type'),
        kwargs.get('y_true'),
        kwargs.get('y_pred'),
        kwargs.get('smape'),
        kwargs.get('mae'),
        kwargs.get('rmse'),
        kwargs.get('total_tokens_prompt'),
        kwargs.get('total_tokens_response'),
        kwargs.get('total_tokens'),
        kwargs.get('response_time')
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
          ts_format,
          ts_type,
          y_true,
          y_pred,
          smape,
          mae,
          rmse,
          total_tokens_prompt,
          total_tokens_response,
          total_tokens,
          response_time
        ) VALUES ({', '.join(['?'] * len(values))})""",
        values
      )
      self.connection.commit()
      print("[INFO] Dados inseridos com sucesso na tabela history.")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao inserir dados na tabela history: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, dataset: str, prompt_types: list[str]) -> list:
    """Seleciona dados da tabela com base em 'dataset' e 'prompt_type'."""
    try:
      placeholders = ','.join(['?'] * len(prompt_types))
      query = f"SELECT * FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      params = [dataset] + prompt_types
      self.cursor.execute(query, params)
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao selecionar dados da tabela history: {e}")
      return []
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove(self, id: int) -> bool:
    """Remove um registro específico da tabela com base no ID."""
    try:
      self.cursor.execute("SELECT COUNT(*) FROM history WHERE id = ?", (id,))
      if self.cursor.fetchone()[0] == 0:
        raise HistoryNotFoundError(
          f"[WARNING] Registro com ID {id} não encontrado na tabela history."
        )

      self.cursor.execute("DELETE FROM history WHERE id = ?", (id,))
      self.connection.commit()
      print(f"[INFO] Registro com ID {id} removido com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao remover registro da tabela history: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_many(self, dataset: str, prompt_types: list[str]) -> bool:
    """Remove registros da tabela com base em 'dataset' e lista de 'prompt_type'."""
    try:
      if not prompt_types:
        print("[WARNING] A lista de prompt_types está vazia. Nenhum registro será removido.")
        return False

      placeholders = ','.join(['?'] * len(prompt_types))
      query_count = f"SELECT COUNT(*) FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      self.cursor.execute(query_count, [dataset] + prompt_types)
      count = self.cursor.fetchone()[0]

      if count == 0:
        print("[INFO] Nenhum registro encontrado para remover.")
        return True

      query_delete = f"DELETE FROM history WHERE dataset = ? AND prompt_type IN ({placeholders})"
      self.cursor.execute(query_delete, [dataset] + prompt_types)
      self.connection.commit()
      print(f"[INFO] {count} registros removidos com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao remover registros da tabela history: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_all(self) -> bool:
    """Remove todos os registros da tabela history."""
    try:
      self.cursor.execute("SELECT COUNT(*) FROM history")
      count = self.cursor.fetchone()[0]
      if count == 0: return True

      self.cursor.execute("DELETE FROM history")
      self.cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'history'")
      self.connection.commit()
      print(f"[INFO] {count} registros removidos com sucesso da tabela history.")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao remover todos os registros da tabela history: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()
