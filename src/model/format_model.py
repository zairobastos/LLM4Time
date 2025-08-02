import json
import re
import pandas as pd
from io import StringIO
from enum import Enum

# ---------------------- FORMATOS ----------------------
class TSFormat(str, Enum):
  CUSTOM = "custom"
  TSV = "tsv"
  PLAIN = "plain"
  JSON = "json"
  MARKDOWN = "markdown"
  CONTEXT = "context"
  SYMBOL = "symbol"
  CSV = "CSV"

# ---------------------- TIPOS ----------------------
class TSType(str, Enum):
  NUMERIC = "numeric"
  TEXTUAL = "textual"

# ---------------------- FORMATADORES ----------------------
def format_custom(data) -> str:
  return "Date|Value\n" + "\n".join(f"{d}|{v}" for d, v in data)

def format_tsv(data) -> str:
  return "Date\tValue\n" + "\n".join(f"{d}\t{v}" for d, v in data)

def format_plain(data) -> str:
  return "\n".join(f"Date: {d}, Value: {v}" for d, v in data)

def format_json(data) -> str:
  return "\n".join(json.dumps({"Date": d, "Value": v}) for d, v in data)

def format_markdown(data) -> str:
  return "|Date|Value|\n|---|---|\n" + "\n".join(f"|{d}|{v}|" for d, v in data)

def format_context(data) -> str:
  return "Date,Value\n" + "\n".join(f"{d},[{v}]" for d, v in data)

def format_symbol(data) -> str:
  def direction(i: int) -> str:
    if i == 0: return "→"
    return "↑" if data[i][1] > data[i-1][1] else "↓" if data[i][1] < data[i-1][1] else "→"
  return "Date,Value,DirectionIndicator\n" + "\n".join(f"{d},{v},{direction(i)}" for i, (d, v) in enumerate(data))

def format_csv(data) -> str:
  return "Date,Value\n" + "\n".join(f"{d},{v}" for d, v in data)

FORMATTERS = {
  TSFormat.CUSTOM: format_custom,
  TSFormat.TSV: format_tsv,
  TSFormat.PLAIN: format_plain,
  TSFormat.JSON: format_json,
  TSFormat.MARKDOWN: format_markdown,
  TSFormat.CONTEXT: format_context,
  TSFormat.SYMBOL: format_symbol,
  TSFormat.CSV: format_csv
}

# ---------------------- ANALISADORES ----------------------
def parse_custom(data: str) -> list:
  df = pd.read_csv(StringIO(data), sep="|")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

def parse_tsv(data: str) -> list:
  df = pd.read_csv(StringIO(data), sep="\t")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

def parse_plain(data: str) -> list:
  out = []
  for line in data.strip().splitlines():
    match = re.match(r'Date:\s*([^,]+),\s*Value:\s*(.*)', line.strip())
    if match: out.append((match[1], match[2]))
  return out

def parse_json(data: str) -> list:
  out = []
  for line in data.strip().splitlines():
    try:
      obj = json.loads(line)
      out.append((obj["Date"], obj["Value"]))
    except Exception:
      continue
  return out

def parse_markdown(data: str) -> list:
  lines = data.strip().splitlines()
  lines = [line.strip().strip("|") for line in [lines[0]] + lines[2:]]
  df = pd.read_csv(StringIO("\n".join(lines)), sep="|", engine="python", skipinitialspace=True)
  df.columns = [c.strip() for c in df.columns]
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

def parse_context(data: str) -> list:
  df = pd.read_csv(StringIO(data))
  df["Value"] = df["Value"].astype(str).str.strip("[]")
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

def parse_symbol(data: str) -> list:
  df = pd.read_csv(StringIO(data))
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

def parse_csv(data: str) -> list:
  df = pd.read_csv(StringIO(data))
  return list(df[["Date", "Value"]].itertuples(index=False, name=None))

PARSERS = {
  TSFormat.CUSTOM: parse_custom,
  TSFormat.TSV: parse_tsv,
  TSFormat.PLAIN: parse_plain,
  TSFormat.JSON: parse_json,
  TSFormat.MARKDOWN: parse_markdown,
  TSFormat.CONTEXT: parse_context,
  TSFormat.SYMBOL: parse_symbol,
  TSFormat.CSV: parse_csv
}

# ---------------------- CODIFICADORES ----------------------
def encode_numeric(data: list) -> list:
    return data

def encode_textual(data: list) -> list:
  return [(d, ' '.join(str(v))) for d, v in data]

ENCODERS = {
  TSType.NUMERIC: encode_numeric,
  TSType.TEXTUAL: encode_textual
}

# ---------------------- DECODIFICADORES ----------------------
def decode_numeric(data: list) -> list:
    return [(d, float(v)) for d, v in data]

def decode_textual(data: list) -> list:
    return [(d, float(str(v).replace(' ', ''))) for d, v in data]

DECODERS = {
  TSType.NUMERIC: decode_numeric,
  TSType.TEXTUAL: decode_textual
}

# ---------------------- FUNÇÕES PÚBLICAS ----------------------
def list_to_string(data: list, ts_format: TSFormat, ts_type: TSType = TSType.NUMERIC) -> str:
  """
  Formata uma lista de tuplas (data, valor) para uma string no formato especificado.
  """
  if ts_format not in FORMATTERS:
    raise ValueError(f"Formato desconhecido: {format}")
  if ts_type not in ENCODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  return FORMATTERS[ts_format](ENCODERS[ts_type](data))

def string_to_list(data: str, ts_format: TSFormat, ts_type: TSType = TSType.NUMERIC) -> list:
  """
  Converte uma string formatada de volta para uma lista de tuplas (data, valor).
  """
  if ts_format not in PARSERS:
    raise ValueError(f"Formato desconhecido: {ts_format}")
  if ts_type not in DECODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  return DECODERS[ts_type](PARSERS[ts_format](data))
