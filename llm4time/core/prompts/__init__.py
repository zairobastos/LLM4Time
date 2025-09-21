from .zero_shot import *
from .few_shot import *
from .cot import *
from .cot_few import *

from enum import Enum


class PromptType(str, Enum):
  ZERO_SHOT = 'ZERO_SHOT'
  FEW_SHOT = 'FEW_SHOT'
  COT = 'COT'
  COT_FEW = 'COT_FEW'
  CUSTOM = 'CUSTOM'
