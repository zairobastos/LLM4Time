import sqlite3

# ---------------- Exceções ----------------

class ModelNotFoundError(Exception):
  pass

class ModelAlreadyExistsError(Exception):
  pass

# ---------------- CRUD ----------------

class CrudModels:
  def __init__(self):
    self.connection = sqlite3.connect('./database/database.db')
    self.cursor = self.connection.cursor()

  def insert(self, **kwargs) -> bool:
    """Insere um registro na tabela models."""
    name = kwargs.get('name')
    provider = kwargs.get('provider')

    try:
      self.cursor.execute(
        "INSERT INTO models (name, provider) VALUES (?, ?)",
        (name, provider)
      )
      self.connection.commit()
      print("[INFO] Dados inseridos com sucesso na tabela models.")
      return True
    except sqlite3.IntegrityError as e:
      raise ModelAlreadyExistsError(
        f"O modelo '{name}' já existe para o provedor '{provider}'."
      )
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao inserir dados na tabela models: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, provider: str) -> list[tuple]:
    """Seleciona todos os modelos de um provider específico."""
    try:
      self.cursor.execute("SELECT * FROM models WHERE provider = ?", (provider,))
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao selecionar dados da tabela models: {e}")
      return []
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def select_all(self) -> list[tuple]:
    """Seleciona todos os modelos da tabela."""
    try:
      self.cursor.execute("SELECT * FROM models")
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao selecionar todos os dados da tabela models: {e}")
      return []
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_many(self, models: list[tuple[str, str]]) -> dict[tuple[str, str], bool]:
    """
    Remove múltiplos registros da tabela models.
    Recebe lista de tuplas (name, provider).
    Retorna dict com status por entrada.
    """
    try:
      results = {}
      for name, provider in models:
        # Verifica existência do registro
        self.cursor.execute(
          "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
          (name, provider)
        )
        if self.cursor.fetchone()[0] == 0:
          print(f"[WARNING] Registro com modelo '{name}' e provedor '{provider}' não encontrado.")
          results[(name, provider)] = False
          continue

        # Remove o registro
        self.cursor.execute(
          "DELETE FROM models WHERE name = ? AND provider = ?",
          (name, provider)
        )
        print(f"[INFO] Registro com modelo '{name}' e provedor '{provider}' removido com sucesso.")
        results[(name, provider)] = True

      self.connection.commit()
      return results
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao remover registros da tabela models: {e}")
      return {entry: False for entry in models}
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def rename(self, old_name: str, new_name: str, provider: str) -> bool:
    """
    Renomeia um registro na tabela models alterando o campo name.
    """
    try:
      # Verifica existência do registro
      self.cursor.execute(
        "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
        (old_name, provider)
      )
      if self.cursor.fetchone()[0] == 0:
        raise ModelNotFoundError(
          f"Registro com modelo '{old_name}' e provedor '{provider}' não encontrado."
        )

      # Verifica se já existe conflito com o novo nome
      self.cursor.execute(
        "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
        (new_name, provider)
      )
      if self.cursor.fetchone()[0] > 0:
        raise ModelAlreadyExistsError(
          f"Já existe registro com modelo '{new_name}' e provedor '{provider}'."
        )

      # Atualiza o nome
      self.cursor.execute(
        "UPDATE models SET name = ? WHERE name = ? AND provider = ?",
        (new_name, old_name, provider)
      )
      self.connection.commit()
      print(f"[INFO] Modelo '{old_name}' renomeado para '{new_name}' com sucesso (provider='{provider}').")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao renomear modelo: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()
