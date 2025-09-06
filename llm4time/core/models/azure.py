"""
Módulo para integração com modelos Azure OpenAI em séries temporais.
"""

from .base import Model
from openai import AzureOpenAI as Client
import time


class AzureOpenAI(Model):
  """
  Classe para integração com modelos Azure OpenAI para previsão de séries temporais.

  Attributes:
    model (str): Nome do modelo Azure OpenAI.
    api_key (str): Chave de API para autenticação.
    azure_endpoint (str): URL do endpoint Azure OpenAI.
    api_version (str): Versão da API Azure OpenAI.
  """

  def __init__(
      self,
      model: str,
      api_key: str,
      azure_endpoint: str,
      api_version: str,
  ) -> None:
    """
    Inicializa a classe AzureOpenAI com configurações de conexão.

    Args:
        model (str): Nome do modelo Azure OpenAI.
        api_key (str): Chave de API para autenticação.
        azure_endpoint (str): URL do endpoint Azure OpenAI.
        api_version (str): Versão da API Azure OpenAI.
    """
    self.model = model
    self.api_key = api_key
    self.azure_endpoint = azure_endpoint
    self.api_version = api_version

  def predict(
      self,
      content: str,
      temperature: float = 0.7,
      **kwargs
  ) -> tuple[str, int, int, float]:
    """
    Envia uma requisição de chat para um modelo OpenAI Azure e retorna a resposta com métricas.

    Args:
        content (str): Conteúdo da mensagem do usuário a ser enviada.
        temperature (float, optional): Grau de aleatoriedade da resposta.
                                       Padrão: 0.7.
        **kwargs: Argumentos adicionais passados para `client.chat.completions.create`.

    Returns:
        tuple[str, int, int, float]: Tupla contendo:
            - response: Resposta do modelo.
            - prompt_tokens: Número de tokens usados no prompt.
            - response_tokens: Número de tokens usados na resposta.
            - response_time: Tempo total da requisição em segundos.

    Examples:
        >>> response, prompt_tokens, response_tokens, time_sec = model.predict(
        ...     content="Série temporal: [199.99, 190.10, 180.01, 178.45, 160.33]. Preveja próximos 3 valores.",
        ...     temperature=0.5
        ... )
        >>> print(response)
        '[149.25, 140.10, 128.50]'
    """
    client = Client(
        api_key=self.api_key,
        azure_endpoint=self.azure_endpoint,
        api_version=self.api_version
    )

    params = {
        "model": self.model,
        "messages": [{"role": "user", "content": content}],
        "temperature": temperature
    }
    params.update(kwargs)

    start_time = time.time()
    response = client.chat.completions.create(**params)
    end_time = time.time()

    response_text = response.choices[0].message.content
    response_text = self._clean_response(response_text)

    usage = response.usage
    total_tokens_prompt = usage.prompt_tokens
    total_tokens_response = usage.completion_tokens
    response_time = end_time - start_time

    return response_text, total_tokens_prompt, total_tokens_response, response_time
