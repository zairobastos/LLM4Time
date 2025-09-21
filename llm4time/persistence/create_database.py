"""
Módulo para criação e inicialização do banco de dados SQLite.

Este módulo fornece funcionalidades para criar tabelas e inicializar
o banco de dados SQLite usado pelo sistema llm4time.
"""

import sqlite3
from sqlite3 import Cursor
from contextlib import closing
from llm4time.persistence import HISTORY_SCHEMA, MODELS_SCHEMA, PROMPTS_SCHEMA
from llm4time.core.logging import logger
import os


def create_table(cursor: Cursor, table_name: str, schema: str) -> None:
  """
  Cria uma tabela no banco de dados SQLite.

  Args:
      cursor (Cursor): Cursor do banco de dados SQLite.
      table_name (str): Nome da tabela a ser criada.
      schema (str): Schema SQL da tabela com placeholder {table_name}.

  Raises:
      sqlite3.Error: Se ocorrer erro durante a criação da tabela.

  Examples:
      >>> cursor = conn.cursor()
      >>> create_table(cursor, 'users', 'CREATE TABLE {table_name} (id INTEGER PRIMARY KEY)')
  """
  try:
    logger.info(f"Criando a tabela '{table_name}'...")
    cursor.execute(schema.format(table_name=table_name))
    logger.info(f"Tabela '{table_name}' criada com sucesso.")
  except sqlite3.Error as e:
    logger.error(f"Falha ao criar a tabela '{table_name}': {e}")
    raise


def create_database(db_path: str = 'database/database.db') -> None:
  """
  Inicializa o banco de dados SQLite criando as tabelas necessárias.

  Cria um banco de dados SQLite no caminho especificado e inicializa
  as tabelas 'history' e 'models' usando os schemas importados.

  Args:
      db_path (str, optional): Caminho para o arquivo do banco de dados.
                               Padrão: 'database/database.db'.

  Raises:
      sqlite3.Error: Se ocorrer erro durante a criação do banco ou tabelas.

  Examples:
      >>> create_database()  # Usa o caminho padrão
      >>> create_database('custom/path/mydb.db')  # Caminho personalizado
  """
  logger.info(f"Inicializando criação do banco de dados em '{db_path}'...")
  try:
    with closing(sqlite3.connect(db_path)) as conn:
      with closing(conn.cursor()) as cursor:
        create_table(cursor, 'history', HISTORY_SCHEMA)
        create_table(cursor, 'models', MODELS_SCHEMA)
        create_table(cursor, 'prompts', PROMPTS_SCHEMA)
      conn.commit()
    logger.info("Banco de dados e tabelas criados com sucesso.")
  except sqlite3.Error as e:
    logger.error(f"Falha ao criar o banco de dados: {e}")
    raise


if __name__ == "__main__":
  logger.debug("Schema da tabela:")
  os.makedirs("database", exist_ok=True)
  create_database()
