from .decode_numeric import decode_numeric
from .decode_textual import decode_textual

from enum import Enum


class TSType(str, Enum):
  NUMERIC = 'NUMERIC'
  TEXTUAL = 'TEXTUAL'


DECODERS = {
    TSType.NUMERIC: decode_numeric,
    TSType.TEXTUAL: decode_textual
}
