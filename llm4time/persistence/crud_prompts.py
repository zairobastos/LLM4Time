"""
Módulo para operações CRUD na tabela prompts do banco de dados.
"""

import json
import sqlite3
from ..core.logging import logger


class PromptNotFoundError(Exception):
  """Exceção levantada quando um prompt não é encontrado na tabela prompts."""
  pass


class PromptAlreadyExistsError(Exception):
  """Exceção levantada quando se tenta inserir um prompt que já existe."""
  pass


class CrudPrompts:
  """
  Classe para operações CRUD na tabela prompts.

  Esta classe gerencia todas as operações de banco de dados relacionadas
  aos prompts do sistema.
  """

  def __init__(self, db_path: str = "database/database.db") -> None:
    """
    Inicializa a conexão com o banco de dados SQLite.

    Args:
        db_path (str, optional): Caminho para o arquivo do banco de dados.
                                 Padrão: 'database/database.db'.
    """
    self.connection = sqlite3.connect(db_path)
    self.cursor = self.connection.cursor()

  def insert(self, **kwargs) -> bool:
    """
    Insere um novo prompt na tabela prompts.

    Args:
        **kwargs: Argumentos nomeados contendo os dados do prompt.
                  - name (str): Nome do prompt
                  - content (str): Conteúdo do prompt
                  - variables (dict[str, str]): Dicionário de variáveis com valores padrão

    Returns:
        bool: True se a inserção foi bem-sucedida, False caso contrário.

    Raises:
        PromptAlreadyExistsError: Se já existir um prompt com o mesmo nome.
    """
    name = kwargs.get("name")
    content = kwargs.get("content")
    variables = kwargs.get("variables", {})

    try:
      self.cursor.execute(
          "INSERT INTO prompts (name, content, variables) VALUES (?, ?, ?)",
          (name, content, json.dumps(variables)))

      self.connection.commit()
      logger.info("Prompt inserido com sucesso na tabela prompts.")
      return True
    except sqlite3.IntegrityError:
      raise PromptAlreadyExistsError(f"O prompt '{name}' já existe na tabela.")

    except sqlite3.Error as e:
      logger.error(f"Erro ao inserir prompt: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, name: str) -> dict | None:
    """
    Seleciona um prompt pelo nome.

    Args:
        name (str): Nome do prompt.

    Returns:
        dict | None: Registro do prompt ou None se não encontrado.
                     Estrutura: {"name": str, "content": str, "variables": dict}

    Raises:
        PromptNotFoundError: Se o prompt não existir.
    """
    try:
      self.cursor.execute(
          "SELECT name, content, variables FROM prompts WHERE name = ?", (name,))
      row = self.cursor.fetchone()
      if row is None:
        raise PromptNotFoundError(f"Prompt '{name}' não encontrado.")
      return {
          "name": row[0],
          "content": row[1],
          "variables": json.loads(row[2]) if row[2] else {}
      }
    except sqlite3.Error as e:
      logger.error(f"Erro ao selecionar prompt: {e}")
      return None
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def select_all(self) -> list[dict]:
    """
    Seleciona todos os prompts da tabela.

    Returns:
        list[dict]: Lista com todos os registros de prompts.
    """
    try:
      self.cursor.execute("SELECT name, content, variables FROM prompts")
      rows = self.cursor.fetchall()
      return [
          {"name": r[0], "content": r[1], "variables": json.loads(r[2]) if r[2] else {}}
          for r in rows]
    except sqlite3.Error as e:
      logger.error(f"Erro ao selecionar prompts: {e}")
      return []
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove(self, name: str) -> bool:
    """
    Remove um prompt pelo nome.

    Args:
        name (str): Nome do prompt a ser removido.

    Returns:
        bool: True se removido, False caso contrário.

    Raises:
        PromptNotFoundError: Se o prompt não existir.
    """
    try:
      self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE name = ?", (name,))
      if self.cursor.fetchone()[0] == 0:
        raise PromptNotFoundError(f"Prompt '{name}' não encontrado.")

      self.cursor.execute("DELETE FROM prompts WHERE name = ?", (name,))
      self.connection.commit()
      logger.info(f"Prompt '{name}' removido com sucesso.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao remover prompt: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_many(self, names: list[str]) -> dict[str, bool]:
    """
    Remove múltiplos prompts da tabela prompts.

    Para cada prompt na lista, verifica sua existência e o remove
    se encontrado. Retorna o status de cada operação.

    Args:
        names (list[str]): Lista de nomes de prompts a serem removidos.

    Returns:
        dict[str, bool]: Dicionário onde as chaves são os nomes dos prompts
                         e os valores são True para sucesso ou False para falha.

    Examples:
        >>> crud = CrudPrompts()
        >>> results = crud.remove_many(['prompt1', 'prompt2'])
        >>> for name, success in results.items():
        ...     status = "removido" if success else "falhou"
        ...     print(f"{name}: {status}")
    """
    try:
      results = {}
      for name in names:
        # Verifica existência do registro
        self.cursor.execute(
            "SELECT COUNT(*) FROM prompts WHERE name = ?",
            (name,))

        if self.cursor.fetchone()[0] == 0:
          logger.warning(f"Prompt '{name}' não encontrado.")
          results[name] = False
          continue

        # Remove o registro
        self.cursor.execute(
            "DELETE FROM prompts WHERE name = ?",
            (name,))

        logger.info(f"Prompt '{name}' removido com sucesso.")
        results[name] = True

      self.connection.commit()
      return results

    except sqlite3.Error as e:
      logger.error(f"Erro ao remover registros da tabela prompts: {e}")
      return {name: False for name in names}

    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def update(self, name: str, new_content: str, new_variables: dict[str, str]) -> bool:
    """
    Atualiza o conteúdo e as variáveis de um prompt existente.

    Args:
        name (str): Nome do prompt a ser atualizado.
        new_content (str): Novo conteúdo do prompt.
        new_variables (dict[str, str]): Dicionário de variáveis com valores padrão.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.

    Raises:
        PromptNotFoundError: Se o prompt não existir.
    """
    try:
      # Verifica existência do prompt
      self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE name = ?", (name,))
      if self.cursor.fetchone()[0] == 0:
        raise PromptNotFoundError(f"Prompt '{name}' não encontrado.")

      # Atualiza conteúdo e chaves
      self.cursor.execute(
          "UPDATE prompts SET content = ?, variables = ? WHERE name = ?",
          (new_content, json.dumps(new_variables), name),)

      self.connection.commit()
      logger.info(f"Prompt '{name}' atualizado com sucesso.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao atualizar prompt '{name}': {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def rename(self, old_name: str, new_name: str) -> bool:
    """
    Renomeia um prompt.

    Args:
        old_name (str): Nome atual do prompt.
        new_name (str): Novo nome para o prompt.

    Returns:
        bool: True se renomeado com sucesso, False caso contrário.

    Raises:
        PromptNotFoundError: Se o prompt original não existir.
        PromptAlreadyExistsError: Se o novo nome já existir.
    """
    try:
      # Verifica se existe o prompt original
      self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE name = ?", (old_name,))
      if self.cursor.fetchone()[0] == 0:
        raise PromptNotFoundError(f"Prompt '{old_name}' não encontrado.")

      # Verifica se já existe o novo nome
      self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE name = ?", (new_name,))
      if self.cursor.fetchone()[0] > 0:
        raise PromptAlreadyExistsError(f"Já existe prompt com nome '{new_name}'.")

      # Atualiza o nome
      self.cursor.execute(
          "UPDATE prompts SET name = ? WHERE name = ?",
          (new_name, old_name))

      self.connection.commit()
      logger.info(f"Prompt '{old_name}' renomeado para '{new_name}'.")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao renomear prompt: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()
