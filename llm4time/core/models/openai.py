"""
Módulo para integração com modelos OpenAI em séries temporais.
"""

from .base import Model
from openai import OpenAI as Client
import time


class OpenAI(Model):
  """
  Classe para integração com modelos OpenAI para previsão de séries temporais.

  Attributes:
    model (str): Nome do modelo OpenAI.
    api_key (str): Chave de API para autenticação.
    base_url (str): URL base do endpoint OpenAI.
  """

  def __init__(
      self,
      model: str,
      api_key: str,
      base_url: str
  ) -> None:
    """
    Inicializa a classe OpenAI com configurações de conexão.

    Args:
        model (str): Nome do modelo OpenAI.
        api_key (str): Chave de API para autenticação.
        base_url (str): URL base do endpoint OpenAI.
    """
    self.model = model
    self.api_key = api_key
    self.base_url = base_url

  def predict(
      self,
      content: str,
      temperature: float = 0.7,
      **kwargs
  ) -> tuple[str, int, int, float]:
    """
    Envia uma requisição de chat para um modelo OpenAI e retorna a resposta com métricas.

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
    client = Client(api_key=self.api_key, base_url=self.base_url)

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
