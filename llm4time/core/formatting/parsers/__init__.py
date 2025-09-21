from .from_array import from_array
from .from_context import from_context
from .from_csv import from_csv
from .from_custom import from_custom
from .from_json import from_json
from .from_markdown import from_markdown
from .from_plain import from_plain
from .from_symbol import from_symbol
from .from_tsv import from_tsv

from enum import Enum


class TSFormat(str, Enum):
  ARRAY = 'ARRAY'
  TSV = 'TSV'
  PLAIN = 'PLAIN'
  JSON = 'JSON'
  MARKDOWN = 'MARKDOWN'
  CONTEXT = 'CONTEXT'
  SYMBOL = 'SYMBOL'
  CSV = 'CSV'
  CUSTOM = 'CUSTOM'


PARSERS = {
    TSFormat.ARRAY: from_array,
    TSFormat.CONTEXT: from_context,
    TSFormat.CSV: from_csv,
    TSFormat.CUSTOM: from_custom,
    TSFormat.JSON: from_json,
    TSFormat.MARKDOWN: from_markdown,
    TSFormat.PLAIN: from_plain,
    TSFormat.SYMBOL: from_symbol,
    TSFormat.TSV: from_tsv,
}
