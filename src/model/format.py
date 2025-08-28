import json
import re
import numpy as np
import pandas as pd
from io import StringIO
from enum import Enum

# ---------------------- FORMATOS ----------------------
class TSFormat(str, Enum):
  ARRAY = 'ARRAY'
  CUSTOM = 'CUSTOM'
  TSV = 'TSV'
  PLAIN = 'PLAIN'
  JSON = 'JSON'
  MARKDOWN = 'MARKDOWN'
  CONTEXT = 'CONTEXT'
  SYMBOL = 'SYMBOL'
  CSV = 'CSV'

# ---------------------- TIPOS ----------------------
class TSType(str, Enum):
  NUMERIC = 'NUMERIC'
  TEXTUAL = 'TEXTUAL'

# ---------------------- FORMATADORES ----------------------
def format_array(data) -> str:
  if data and isinstance(data[0], (tuple, list)):
    data = [v for _, v in data]
  return "[" + ", ".join(map(str, data)) + "]"

def format_custom(data) -> str:
  return "Date|Value\n" + "\n".join(f"{d}|{v}" for d, v in data)

def format_tsv(data) -> str:
  return "Date\tValue\n" + "\n".join(f"{d}\t{v}" for d, v in data)

def format_plain(data) -> str:
  return "\n".join(f"Date: {d}, Value: {v}" for d, v in data)

def format_json(data) -> str:
  return json.dumps([{"Date": d, "Value": v} for d, v in data])

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
  TSFormat.ARRAY: format_array,
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
def parse_array(data: str) -> list:
  return data.strip("[]").split(", ")

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
  return [(v["Date"], v["Value"]) for v in json.loads(data)]

def parse_markdown(data: str) -> list:
  data = data.strip().splitlines()
  data = [line.strip().strip("|") for line in [data[0]] + data[2:]]
  df = pd.read_csv(StringIO("\n".join(data)), sep="|", engine="python", skipinitialspace=True)
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
  TSFormat.ARRAY: parse_array,
  TSFormat.CUSTOM: parse_custom,
  TSFormat.TSV: parse_tsv,
  TSFormat.PLAIN: parse_plain,
  TSFormat.JSON: parse_json,
  TSFormat.MARKDOWN: parse_markdown,
  TSFormat.CONTEXT: parse_context,
  TSFormat.SYMBOL: parse_symbol,
  TSFormat.CSV: parse_csv
}

# ---------------------- NORMALIZADORES ----------------------

def normalize_missing(v):
  if v is None or (isinstance(v, float) and np.isnan(v)):
    return "nan"
  return v

def denormalize_missing(v):
  if str(v).lower() == "nan":
    return np.nan
  return v

# ---------------------- CODIFICADORES ----------------------

def encode_numeric(data: list) -> list:
  if data and isinstance(data[0], (tuple, list)):
    return [(d, normalize_missing(v)) for d, v in data]
  return [normalize_missing(v) for v in data]

def encode_textual(data: list) -> list:
  if data and isinstance(data[0], (tuple, list)):
    return [(d, ' '.join(str(normalize_missing(v)))) for d, v in data]
  return [' '.join(str(normalize_missing(v))) for v in data]

ENCODERS = {
  TSType.NUMERIC: encode_numeric,
  TSType.TEXTUAL: encode_textual
}

# ---------------------- DECODIFICADORES ----------------------
def decode_numeric(data: list) -> list:
  if data and isinstance(data[0], (tuple, list)):
    data = [denormalize_missing(v) for _, v in data]
  else:
    data = [denormalize_missing(v) for v in data]
  return [float(v) if not pd.isna(v) else np.nan for v in data]

def decode_textual(data: list) -> list:
  if data and isinstance(data[0], (tuple, list)):
    data = [denormalize_missing(v) for _, v in data]
  else:
    data = [denormalize_missing(v) for v in data]
  return [float(str(v).replace(' ', '')) if not pd.isna(v) else np.nan for v in data]

DECODERS = {
  TSType.NUMERIC: decode_numeric,
  TSType.TEXTUAL: decode_textual
}

# ---------------------- FUNÇÕES PÚBLICAS ----------------------
def format_timeseries(ts: list, ts_format: TSFormat, ts_type: TSType = TSType.NUMERIC) -> str:
  """
  Formata uma lista de tuplas (data, valor) para uma string no formato especificado.
  """
  if ts_format not in FORMATTERS:
    raise ValueError(f"Formato desconhecido: {format}")
  if ts_type not in ENCODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  return FORMATTERS[ts_format](ENCODERS[ts_type](ts))

def parse_timeseries(ts: str, ts_format: TSFormat, ts_type: TSType = TSType.NUMERIC) -> list:
  """
  Converte uma string formatada de volta para uma lista de tuplas (data, valor).
  """
  if ts_format not in PARSERS:
    raise ValueError(f"Formato desconhecido: {ts_format}")
  if ts_type not in DECODERS:
    raise ValueError(f"Tipo desconhecido: {ts_type}")
  try:
    return DECODERS[ts_type](PARSERS[ts_format](ts))
  except:
    return DECODERS[TSType.NUMERIC](PARSERS[TSFormat.ARRAY](ts))
