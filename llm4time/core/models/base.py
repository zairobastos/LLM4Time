import re


class Model:
  def __init__(self, model: str) -> None:
    self.model = model

  def _clean_response(self, response: str) -> str:
    # remove qualquer bloco <think>...</think>
    return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
