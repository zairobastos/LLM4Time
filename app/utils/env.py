from dotenv import set_key
from utils.paths import abspath
import unicodedata
import re
import os

# LLM4Time
from llm4time.core.models import Provider

ENV_PATH = abspath(".env")


def normalize(text: str) -> str:
  # Remove acentos
  text = unicodedata.normalize('NFKD', text).encode(
      'ASCII', 'ignore').decode('utf-8')
  # Substitui caracteres indesejados por "_"
  text = re.sub(r'[^a-zA-Z0-9]', '_', text)
  # Substitui múltiplos "_" consecutivos por apenas um "_"
  text = re.sub(r'_+', '_', text)
  # Remove "_" do início e do fim
  text = text.strip('_')
  # Converte para letras minúsculas
  return text.lower()


def save_model_env(env_vars: dict):
  """
  Salva as variáveis no .env.

  env_vars (dict): Dict com {chave: valor}.
  """
  # Cria o arquivo .env se ele não existir
  if not os.path.exists(ENV_PATH):
    with open(ENV_PATH, 'w') as f:
      f.write("")

  # Salva cada chave/valor no .env
  for k, v in env_vars.items():
    set_key(ENV_PATH, k, v)


def rename_model_env(old_model: str, new_model: str, provider: Provider):
  """
  Renomeia variáveis de ambiente de um modelo no arquivo .env.
  Apenas o prefixo das chaves é alterado, os valores permanecem iguais.

  old_model (str): Nome atual do modelo.
  new_model (str): Novo nome para o modelo.
  provider (Provider): Provedor da API.
  """
  old_prefix = f"{normalize(provider)}_{normalize(old_model)}_"
  new_prefix = f"{normalize(provider)}_{normalize(new_model)}_"
  if not os.path.exists(ENV_PATH):
    return
  with open(ENV_PATH) as f:
    lines = f.readlines()
  with open(ENV_PATH, "w") as f:
    for line in lines:
      if line.startswith(old_prefix):
        # Substitui apenas o prefixo, não altera valores
        f.write(line.replace(old_prefix, new_prefix, 1))
      else:
        f.write(line)


def remove_model_env(model: str, provider: Provider):
  """
  Remove variáveis de ambiente associadas a um modelo específico do arquivo .env.

  model (str): Nome do modelo.
  provider (Provider): Provedor da API.
  """
  prefix = f"{normalize(provider)}_{normalize(model)}_"
  if not os.path.exists(ENV_PATH):
    return
  with open(ENV_PATH) as f:
    lines = f.readlines()
  with open(ENV_PATH, "w") as f:
    for line in lines:
      if not line.startswith(prefix):
        f.write(line)
