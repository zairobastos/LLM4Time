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
  prompt_type TEXT CHECK(prompt_type IN ('ZERO_SHOT', 'FEW_SHOT', 'COT','COT_FEW')),
  ts_format,
  ts_type,
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
