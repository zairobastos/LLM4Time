# Provedores
import lmstudio as lms
from openai import OpenAI, AzureOpenAI

# Utilitárias
import re
import os
import time
import math
import tiktoken
from enum import Enum
from dotenv import load_dotenv

# Mock
import random
import pandas as pd
from src.model.format import TSFormat, TSType, format_timeseries

load_dotenv()

class Provider(str, Enum):
  LM_STUDIO = 'lmstudio'
  OPENAI = 'openai'
  AZURE = 'azure'

  def __str__(self):
    return {
      Provider.LM_STUDIO: "LM Studio",
      Provider.OPENAI: "OpenAI / Ollama",
      Provider.AZURE: "OpenAI Azure",
    }[self]

class API:
  def __init__(self, model:str, provider:Provider, temperature:float):
    """
    Classe responsável por manipular a API do modelo.

    Args:
      model (str): Modelo a ser utilizado.
      provider (Provider): Provedor da API (lmstudio, openai, azure).
      temperature (float): Temperatura do modelo.
    """
    self.model = model
    self.provider = provider
    self.temperature = temperature

  def response(self, content:str, **kwargs):
    """
    Gera a resposta do modelo com base no prompt e temperatura definidos.

    Returns:
      tuple: (response, total_tokens_prompt, total_tokens_response, elapsed_time)
    """
    if self.provider == Provider.LM_STUDIO:
      return self._lmstudio(content, **kwargs)
    elif self.provider == Provider.OPENAI:
      return self._openai(content, **kwargs)
    elif self.provider == Provider.AZURE:
      return self._azure_openai(content, **kwargs)
    else:
      print(f"[ERROR] Provedor desconhecido: {self.provider}")
      return None, None, None, None

  # -------------------- LM Studio --------------------
  def _lmstudio(self, content:str, **kwargs) -> tuple[str, int, int, float]:
    try:
      model_instance = lms.llm(self.model)
      print(f"[INFO] Modelo: {model_instance}")

      config = {"temperature": self.temperature}
      config.update(kwargs)

      start_time = time.time()
      response_obj = model_instance.respond(content, config=config)
      end_time = time.time()

      # Verifica se o objeto tem o atributo `.text`
      response = response_obj.text if hasattr(response_obj, 'text') else str(response_obj)

      if 'deepseek-r1' in self.model:
        result_match = re.search(r'</think>\s*(.*)', response, re.DOTALL)
        if result_match:
          response = result_match.group(1).strip()

      print(f"[INFO] Resposta: {response}")
      total_tokens_prompt = response_obj.stats.prompt_tokens_count if hasattr(response_obj, "stats") else 0
      total_tokens_response = response_obj.stats.predicted_tokens_count if hasattr(response_obj, "stats") else 0
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt} - Tokens Resposta: {total_tokens_response} - Tempo: {end_time - start_time:.2f} segundos")
      return response, total_tokens_prompt, total_tokens_response, end_time - start_time

    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  # -------------------- OpenAI --------------------
  def _openai(self, content:str, **kwargs) -> tuple[str, int, int, float]:
    print(f"[INFO] Modelo: {self.model}")
    key_name = f'openai_{self.model}_key'.replace("-", "_").replace(".", "_")
    base_url_name = f'openai_{self.model}_base_url'.replace("-", "_").replace(".", "_")

    api_key = os.getenv(key_name)
    base_url = os.getenv(base_url_name)
    print(f"[INFO] Base URL: {base_url}")

    client = OpenAI(
      api_key=api_key,
      base_url=base_url
    )

    params = {
      "model": self.model,
      "messages": [{"role": "user", "content": content}],
      "temperature": self.temperature
    }
    params.update(kwargs)

    try:
      start_time = time.time()
      response = client.chat.completions.create(**params)
      end_time = time.time()

      response_text = response.choices[0].message.content
      response_text = API.clean_response(response_text)

      usage = response.usage
      total_tokens_prompt = usage.prompt_tokens
      total_tokens_response = usage.completion_tokens
      response_time = end_time - start_time

      print(f"[INFO] Resposta: {response_text}")
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt}")
      print(f"[INFO] Tokens Resposta: {total_tokens_response}")
      print(f"[INFO] Tempo: {response_time:.2f} segundos")
      return response_text, total_tokens_prompt, total_tokens_response, response_time
    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  # -------------------- Azure --------------------
  def _azure_openai(self, content:str, **kwargs) -> tuple[str, int, int, float]:
    print(f"[INFO] Modelo: {self.model}")
    key_name = f'azure_{self.model}_key'.replace("-", "_").replace(".", "_")
    version_name = f'azure_{self.model}_api_version'.replace("-", "_").replace(".", "_")
    endpoint_name = f'azure_{self.model}_endpoint'.replace("-", "_").replace(".", "_")

    api_key = os.getenv(key_name)
    api_version = os.getenv(version_name)
    endpoint = os.getenv(endpoint_name)
    print(f"[INFO] API Version: {api_version}")
    print(f"[INFO] Endpoint: {endpoint}")

    client = AzureOpenAI(
      api_key=api_key,
      azure_endpoint=endpoint,
      api_version=api_version
    )

    params = {
      "model": self.model,
      "messages": [{"role": "user", "content": content}],
      "temperature": self.temperature
    }
    params.update(kwargs)

    try:
      start_time = time.time()
      response = client.chat.completions.create(**params)
      end_time = time.time()

      response_text = response.choices[0].message.content
      response_text = API.clean_response(response_text)

      usage = response.usage
      total_tokens_prompt = usage.prompt_tokens
      total_tokens_response = usage.completion_tokens
      response_time = end_time - start_time

      print(f"[INFO] Resposta: {response_text}")
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt}")
      print(f"[INFO] Tokens Resposta: {total_tokens_response}")
      print(f"[INFO] Tempo: {response_time:.2f} segundos")
      return response_text, total_tokens_prompt, total_tokens_response, response_time
    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  # -------------------- UTILITÁRIOS --------------------
  @staticmethod
  def mock(periods:int, ts_format:TSFormat, ts_type:TSType) -> tuple[str, int, int, float]:
    response_time = round(random.uniform(0.5, 2.5), 2)
    total_tokens_prompt = random.randint(10, 500)
    total_tokens_response = random.randint(10, 500)

    # Gera uma resposta aleatória
    dates = pd.date_range(start='2018-01-01', periods=periods, freq='D')
    values = [round(random.uniform(0, 500), 4) for _ in range(periods)]
    response = [(d.strftime('%Y-%m-%d'), v) for d, v in zip(dates, values)]

    # Formata a resposta
    response_text = format_timeseries(response, ts_format, ts_type)

    time.sleep(response_time * 0.1) # Tempo de espera
    print(f"[MOCK] Resposta: {response_text}")
    print(f"[MOCK] Tokens Prompt: {total_tokens_prompt}")
    print(f"[MOCK] Tokens Resposta: {total_tokens_response}")
    print(f"[MOCK] Tempo: {response_time:.2f} segundos")
    return response_text, total_tokens_prompt, total_tokens_response, response_time

  @staticmethod
  def clean_response(response:str) -> str:
    # remove qualquer bloco <think>...</think>
    return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

  def max_tokens(self, window:list, ts_format:TSFormat, ts_type:TSType, steps:int) -> int:
    """
    Calcula o máximo de tokens.

    Args:
      window (list): Lista com dados de entrada.
      ts_format (TSFormat): Formato dos dados temporais (ARRAY, CSV, etc.).
      ts_type (TSType): Tipo de série (NUMERIC, TEXTUAL).
      steps (int): Quantidade de valores que se deseja prever.
    """
    if len(window) == 0:
      return None

    content = format_timeseries(window, ts_format, ts_type)
    try:
      encoding = tiktoken.encoding_for_model(self.model)
      total_tokens = len(encoding.encode(content))
    except:
      total_tokens = self.response(content=content)[1]

    avg_tokens_per_step = total_tokens / len(window)
    return math.ceil(avg_tokens_per_step * steps)
