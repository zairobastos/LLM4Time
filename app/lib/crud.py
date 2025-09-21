from utils.paths import abspath

# LLM4Time
from llm4time.persistence.crud_models import CrudModels
from llm4time.persistence.crud_prompts import CrudPrompts
from llm4time.persistence.crud_history import CrudHistory


def crud_models():
  return CrudModels(abspath("database/database.db"))


def crud_prompts():
  return CrudPrompts(abspath("database/database.db"))


def crud_history():
  return CrudHistory(abspath("database/database.db"))
