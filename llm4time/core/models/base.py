import re


class Model:
  def __init__(self, model: str) -> None:
    self.model = model

  def _clean_response(self, response: str) -> str:
    return re.findall(r'<out>(.*?)</out>', response, re.DOTALL)[-1].strip()
