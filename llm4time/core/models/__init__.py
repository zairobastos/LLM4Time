from .openai import *
from .azure import *
from .lmstudio import *

from enum import Enum


class Provider(str, Enum):
  LM_STUDIO = 'LM_STUDIO'
  OPENAI = 'OPENAI'
  AZURE = 'AZURE'

  def __str__(self):
    return {
        Provider.LM_STUDIO: "LM Studio",
        Provider.OPENAI: "OpenAI / Ollama",
        Provider.AZURE: "OpenAI Azure",
    }[self]

  @classmethod
  def enum(cls, name: str):
    for member in cls:
      if str(member) == name:
        return member
    return None
