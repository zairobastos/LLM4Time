"""
Módulo para operações CRUD na tabela models do banco de dados.
"""

import sqlite3
from ..core.logging import logger


class ModelNotFoundError(Exception):
  """
  Exceção levantada quando um modelo não é encontrado na tabela models.

  Esta exceção é utilizada quando operações tentam acessar modelos
  que não existem no banco de dados.
  """
  pass


class ModelAlreadyExistsError(Exception):
  """
  Exceção levantada quando se tenta inserir um modelo que já existe.

  Esta exceção é utilizada quando há tentativa de criar duplicatas
  na combinação única de name e provider.
  """
  pass


class CrudModels:
  """
  Classe para operações CRUD na tabela models.

  Esta classe gerencia todas as operações de banco de dados relacionadas
  aos modelos de IA disponíveis no sistema, incluindo inserção, consulta,
  remoção e renomeação.

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
    Insere um novo modelo na tabela models.

    Args:
        **kwargs: Argumentos nomeados contendo os dados do modelo.
                  Campos aceitos:
                  - name (str): Nome do modelo
                  - provider (str): Provedor do modelo (ex: 'openai', 'anthropic')

    Returns:
        bool: True se a inserção foi bem-sucedida, False caso contrário.

    Raises:
        ModelAlreadyExistsError: Se já existir um modelo com o mesmo
                                name e provider.

    Examples:
        >>> crud = CrudModels()
        >>> success = crud.insert(name='gpt-4', provider='openai')
    """
    name = kwargs.get('name')
    provider = kwargs.get('provider')

    try:
      self.cursor.execute(
          "INSERT INTO models (name, provider) VALUES (?, ?)",
          (name, provider))

      self.connection.commit()
      logger.info("Dados inseridos com sucesso na tabela models.")
      return True
    except sqlite3.IntegrityError as e:
      raise ModelAlreadyExistsError(
          f"O modelo '{name}' já existe para o provedor '{provider}'.")

    except sqlite3.Error as e:
      logger.error(f"Erro ao inserir dados na tabela models: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, provider: str) -> list[tuple]:
    """
    Seleciona todos os modelos de um provedor específico.

    Args:
        provider (str): Nome do provedor para filtrar os modelos.

    Returns:
        list[tuple]: Lista de tuplas contendo os registros dos modelos
                    do provedor especificado. Lista vazia em caso de erro
                    ou nenhum registro encontrado.

    Examples:
        >>> crud = CrudModels()
        >>> models = crud.select('openai')
        >>> for model_id, name, provider in models:
        ...     print(f"{name} by {provider}")
    """
    try:
      self.cursor.execute(
          "SELECT * FROM models WHERE provider = ?", (provider,))
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      logger.error(f"Erro ao selecionar dados da tabela models: {e}")
      return []
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def select_all(self) -> list[tuple]:
    """
    Seleciona todos os modelos da tabela.

    Returns:
        list[tuple]: Lista de tuplas contendo todos os registros da tabela.
                    Lista vazia em caso de erro ou tabela vazia.

    Examples:
        >>> crud = CrudModels()
        >>> all_models = crud.select_all()
        >>> print(f"Total de modelos: {len(all_models)}")
    """
    try:
      self.cursor.execute("SELECT * FROM models")
      return self.cursor.fetchall()
    except sqlite3.Error as e:
      logger.error(f"Erro ao selecionar todos os dados da tabela models: {e}")
      return []
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def remove_many(self, models: list[tuple[str, str]]) -> dict[tuple[str, str], bool]:
    """
    Remove múltiplos registros da tabela models.

    Para cada modelo na lista, verifica sua existência e o remove
    se encontrado. Retorna o status de cada operação.

    Args:
        models (list[tuple[str, str]]): Lista de tuplas contendo
                                      (name, provider) dos modelos
                                      a serem removidos.

    Returns:
        dict[tuple[str, str], bool]: Dicionário onde as chaves são
                                    as tuplas (name, provider) e os
                                    valores são True para sucesso ou
                                    False para falha.

    Examples:
        >>> crud = CrudModels()
        >>> models_to_remove = [('gpt-3.5', 'openai'), ('claude-1', 'anthropic')]
        >>> results = crud.remove_many(models_to_remove)
        >>> for (name, provider), success in results.items():
        ...     status = "removido" if success else "falhou"
        ...     print(f"{name} ({provider}): {status}")
    """
    try:
      results = {}
      for name, provider in models:
        # Verifica existência do registro
        self.cursor.execute(
            "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
            (name, provider))

        if self.cursor.fetchone()[0] == 0:
          logger.warning(
              f"Registro com modelo '{name}' e provedor '{provider}' não encontrado.")
          results[(name, provider)] = False
          continue

        # Remove o registro
        self.cursor.execute(
            "DELETE FROM models WHERE name = ? AND provider = ?",
            (name, provider))

        logger.info(
            f"Registro com modelo '{name}' e provedor '{provider}' removido com sucesso.")
        results[(name, provider)] = True

      self.connection.commit()
      return results
    except sqlite3.Error as e:
      logger.error(f"Erro ao remover registros da tabela models: {e}")
      return {entry: False for entry in models}
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()

  def rename(self, old_name: str, new_name: str, provider: str) -> bool:
    """
    Renomeia um modelo na tabela models alterando o campo name.

    Verifica a existência do modelo original e se o novo nome
    não causa conflito antes de realizar a operação.

    Args:
        old_name (str): Nome atual do modelo a ser renomeado.
        new_name (str): Novo nome para o modelo.
        provider (str): Provedor do modelo.

    Returns:
        bool: True se a renomeação foi bem-sucedida, False caso contrário.

    Raises:
        ModelNotFoundError: Se o modelo com old_name não existir.
        ModelAlreadyExistsError: Se já existir um modelo com new_name
                                para o mesmo provider.

    Examples:
        >>> crud = CrudModels()
        >>> success = crud.rename('gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'openai')
    """
    try:
      # Verifica existência do registro
      self.cursor.execute(
          "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
          (old_name, provider))

      if self.cursor.fetchone()[0] == 0:
        raise ModelNotFoundError(
            f"Registro com modelo '{old_name}' e provedor '{provider}' não encontrado.")

      # Verifica se já existe conflito com o novo nome
      self.cursor.execute(
          "SELECT COUNT(*) FROM models WHERE name = ? AND provider = ?",
          (new_name, provider))

      if self.cursor.fetchone()[0] > 0:
        raise ModelAlreadyExistsError(
            f"Já existe registro com modelo '{new_name}' e provedor '{provider}'.")

      # Atualiza o nome
      self.cursor.execute(
          "UPDATE models SET name = ? WHERE name = ? AND provider = ?",
          (new_name, old_name, provider))

      self.connection.commit()
      logger.info(
          f"Modelo '{old_name}' renomeado para '{new_name}' com sucesso (provider='{provider}').")
      return True
    except sqlite3.Error as e:
      logger.error(f"Erro ao renomear modelo: {e}")
      return False
    finally:
      logger.info("Fechando conexão com o banco de dados.")
      self.connection.close()
