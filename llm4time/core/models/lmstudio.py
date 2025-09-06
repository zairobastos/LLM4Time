"""
Módulo para integração com modelos LM Studio em séries temporais.
"""

from .base import Model
import lmstudio as lms
import time


class LMStudio(Model):
  """
  Classe para integração com modelos LM Studio para previsão de séries temporais.

  Attributes:
    model (str): Nome ou caminho do modelo LM Studio.
  """

  def __init__(self, model: str) -> None:
    """
    Inicializa a classe LMStudio com o modelo especificado.

    Args:
        model (str): Nome ou caminho do modelo LM Studio.
    """
    self.model = model

  def predict(
      self,
      content: str,
      temperature: float = 0.7,
      **kwargs
  ) -> tuple[str, int, int, float]:
    """
    Envia uma requisição para o modelo LM Studio e retorna a resposta com métricas.

    Args:
        content (str): Conteúdo da mensagem do usuário a ser enviada.
        temperature (float, optional): Grau de aleatoriedade da resposta.
                                       Padrão: 0.7.
        **kwargs: Argumentos adicionais passados para `client.respond`.

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
    client = lms.llm(self.model)

    config = {"temperature": temperature}
    config.update(kwargs)

    start_time = time.time()
    response = client.respond(content, config=config)
    end_time = time.time()

    response_text = response.text if hasattr(
        response, 'text') else str(response)
    response_text = self._clean_response(response_text)

    total_tokens_prompt = response.stats.prompt_tokens_count if hasattr(
        response, "stats") else 0
    total_tokens_response = response.stats.predicted_tokens_count if hasattr(
        response, "stats") else 0

    return response_text, total_tokens_prompt, total_tokens_response, end_time - start_time
