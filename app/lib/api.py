from utils.env import normalize
from dotenv import load_dotenv
import pandas as pd
import random
import time
import os

# LLM4Time
from llm4time.core.models import Provider, LMStudio, OpenAI, AzureOpenAI
from llm4time.core.formatting import TSFormat, TSType
from llm4time.core.formatter import format


load_dotenv()


class API:
  def __init__(self, model: str, provider: Provider, temperature: float):
    """
    Classe responsável por manipular a API do modelo.

    Args:
      model (str): Modelo a ser utilizado.
      provider (Provider): Provedor da API (LM Studio, OpenAI, Azure).
      temperature (float): Temperatura do modelo.
    """
    self.model = model
    self.provider = provider
    self.temperature = temperature

  def response(self, content: str, **kwargs) -> tuple[str, int, int, float]:
    if self.provider == Provider.LM_STUDIO:
      return self._lmstudio(content, **kwargs)
    elif self.provider == Provider.OPENAI:
      return self._openai(content, **kwargs)
    elif self.provider == Provider.AZURE:
      return self._azure_openai(content, **kwargs)
    else:
      print(f"[ERROR] Provedor desconhecido: {self.provider}")
      return None, None, None, None

  def _lmstudio(self, content: str, **kwargs):
    return self._call_client(lambda model: LMStudio(model), content, **kwargs)

  def _openai(self, content: str, **kwargs):
    api_key = os.getenv(normalize(f"{self.provider}_{self.model}_key"))
    base_url = os.getenv(normalize(f"{self.provider}_{self.model}_base_url"))
    print(f"[INFO] BASE_URL: {base_url}")
    return self._call_client(lambda model: OpenAI(api_key=api_key, base_url=base_url, model=model), content, **kwargs)

  def _azure_openai(self, content: str, **kwargs):
    api_key = os.getenv(normalize(f"{self.provider}_{self.model}_key"))
    endpoint = os.getenv(normalize(f"{self.provider}_{self.model}_endpoint"))
    api_version = os.getenv(normalize(f"{self.provider}_{self.model}_api_version"))
    print(f"[INFO] ENDPOINT: {endpoint}")
    print(f"[INFO] API_VERSION: {api_version}")
    return self._call_client(
        lambda model: AzureOpenAI(
            api_key=api_key, azure_endpoint=endpoint, api_version=api_version, model=model),
        content,
        **kwargs
    )

  def _call_client(self, client_class, content: str, **kwargs) -> tuple[str, int, int, float]:
    try:
      client = client_class(self.model)
      response = client.predict(
          content, temperature=self.temperature, **kwargs)
      response_text, total_tokens_prompt, total_tokens_response, response_time = response
      print(f"[INFO] Resposta: {response_text}")
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt}")
      print(f"[INFO] Tokens Resposta: {total_tokens_response}")
      print(f"[INFO] Tempo: {response_time:.2f} segundos")
      return response_text, total_tokens_prompt, total_tokens_response, response_time
    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  @staticmethod
  def mock(periods: int, ts_format: TSFormat, ts_type: TSType) -> tuple[str, int, int, float]:
    response_time = round(random.uniform(0.5, 2.5), 2)
    total_tokens_prompt = random.randint(10, 500)
    total_tokens_response = random.randint(10, 500)

    # Gera uma resposta aleatória
    dates = pd.date_range(start='2018-01-01', periods=periods, freq='D')
    values = [round(random.uniform(0, 500), 4) for _ in range(periods)]
    response = [(d.strftime('%Y-%m-%d'), v) for d, v in zip(dates, values)]

    # Formata a resposta
    response_text = format(response, ts_format, ts_type)

    time.sleep(response_time * 0.1)  # Tempo de espera
    print(f"[MOCK] Resposta: {response_text}")
    print(f"[MOCK] Tokens Prompt: {total_tokens_prompt}")
    print(f"[MOCK] Tokens Resposta: {total_tokens_response}")
    print(f"[MOCK] Tempo: {response_time:.2f} segundos")

    return response_text, total_tokens_prompt, total_tokens_response, response_time
