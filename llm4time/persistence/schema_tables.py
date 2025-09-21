HISTORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model TEXT,
  temperature REAL,
  dataset TEXT,
  start_date TEXT,
  end_date TEXT,
  periods INTEGER,
  prompt TEXT,
  prompt_type TEXT CHECK(prompt_type IN ('ZERO_SHOT', 'FEW_SHOT', 'COT','COT_FEW', 'CUSTOM')),
  examples INTEGER,
  sampling TEXT CHECK(sampling IN ('FRONTEND', 'BACKEND', 'RANDOM', 'UNIFORM')),
  ts_format TEXT CHECK(ts_format IN ('ARRAY', 'TSV', 'PLAIN', 'JSON', 'MARKDOWN', 'CONTENT', 'SYMBOL', 'CSV', 'CUSTOM')),
  ts_type TEXT CHECK(ts_type IN ('NUMERIC', 'TEXTUAL')),
  y_val TEXT,
  y_pred TEXT,
  smape REAL,
  mae REAL,
  rmse REAL,
  total_tokens_prompt INTEGER,
  total_tokens_response INTEGER,
  total_tokens INTEGER,
  response_time REAL,
  mean_val REAL,
  mean_pred REAL,
  median_val REAL,
  median_pred REAL,
  std_val REAL,
  std_pred REAL,
  min_val REAL,
  min_pred REAL,
  max_val REAL,
  max_pred REAL
)"""

MODELS_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  provider TEXT NOT NULL,
  UNIQUE(name, provider)
)"""

PROMPTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  content TEXT NOT NULL,
  variables TEXT
)"""
