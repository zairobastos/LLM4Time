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
        Provider.OPENAI: "OpenAI",
        Provider.AZURE: "Azure",
    }[self]

  @classmethod
  def enum(cls, name: str):
    for m in cls:
      if str(m) == name:
        return m
    return None
