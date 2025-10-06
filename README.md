<div align="center">
<img src="https://raw.githubusercontent.com/zairobastos/LLM4Time/main/docs/assets/LLM4Time.svg" width="150" />

# LLM4Time
**A library for time series forecasting using Large Language Models (LLMs)**

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TcQ9RPNrtPHSq5gaMXfBTEV7uEpMA66w?usp=sharing)
[![PyPI version](https://img.shields.io/pypi/v/llm4time.svg)](https://pypi.org/project/llm4time/)
![Python versions](https://img.shields.io/badge/python-3.10+-blue)
[![License](https://img.shields.io/github/license/zairobastos/llm4time.svg)](https://github.com/zairobastos/LLM4Time/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-Sphinx-blue)](https://zairobastos.github.io/LLM4Time/)
</div>

<p align="center">
  <a href="#-get-started">Get Started</a> •
  <a href="https://zairobastos.github.io/LLM4Time/">Documentation</a> •
  <a href="#-referências">References</a> •
  <a href="#-contato">Contact</a>
</p>

## 🧩 Get Started
LLM4Time is a Python library for time series forecasting using Large Language Models (LLMs).
It provides a modular architecture that includes:
- [Data preprocessing and handling](#pré-processamento-e-tratamento-de-dados)
- [Prompt generation](#geração-de-prompts)
- [Forecasting with LLMs](#previsão-com-llms)
- [Metric evaluation](#avaliação-de-métricas)
- [Interactive visualization](#visualização-interativa)

### Installation
```bash
pip install llm4time
```

### Running the Streamlit interface
In addition, we provide a Streamlit-based interface, offering a more intuitive and practical way to interact with the library.

Follow the steps below to clone the repository, set up the environment, and run the application.

#### 1. Clone the repository
```bash
git clone https://github.com/zairobastos/LLM4Time.git
cd LLM4Time
```
#### 2. Create and activate a virtual environment (Optional)
```bash
python -m venv .venv
source .venv/bin/activate      # Bash/Zsh
source .venv/bin/activate.fish # Fish Shell
```
#### 3. Install the dependencies
```bash
pip install -e .
pip install -r requirements.txt -r requirements-streamlit.txt
```
#### 4. Run the application
Using python 🐍
```bash
python app/main.py
```
> Access the application at `http://localhost:8501`

Or using docker 🐋
```bash
docker compose up
```

### Data preprocessing and handling
#### 1. Data loading
```python
from llm4time.core.data import loader
from llm4time.core.evaluate import Statistics

# Data loading using CSV, XLSX, JSON or Parquet
df = loader.load_data("etth2.csv")

# Descriptive statistics
stats = Statistics(df['OT'])
print(f"Mean: {stats.mean}")
print(f"Median: {stats.median}")
print(f"1° Quartile: {stats.first_quartile}")
print(f"3° Quartile: {stats.third_quartile}")
print(f"Standard Deviation: {stats.std}")
print(f"Minimum: {stats.min}")
print(f"Maximum: {stats.max}")
print(f"Number of missing values: {stats.missing_count}")
print(f"Percentage of missing values: {stats.missing_percentage}")
```
#### 2. Data preprocessing
```python
from llm4time.core.data import preprocessor

# Standardize into time series format
df = preprocessor.standardize(
  df,
  date_col='date',    # Column containing dates/timestamps
  value_col='OT',     # Column containing time series values
  duplicates='first'  # How to handle duplicate rows: 'first' keeps the first occurrence
)

# Ensure all timestamps are present
df = preprocessor.normalize(df, freq='h')
```

#### 3. Missing data imputation
```python
from llm4time.core.data import imputation

# Replace missing values with the column mean
df = imputation.mean(df)
```

#### 4. Data split
```python
from llm4time.core.data import preprocessor

# Split the dataset into training and validation sets
train, y_val = preprocessor.split(
  df,
  start_date='2016-06-01 00:00:00', # Start of the training set
  end_date='2016-12-01 00:00:00',   # End of the training set
  periods=24                        # Number of periods to forecast
)
```
### Prompt generation
#### 5. Zero-shot prompt generation
```python
from llm4time.core import prompt
from llm4time.core import PromptType, TSFormat, TSType

content = prompt.generate(
    train,       # Training set [(date, value), ...]
    periods=24,  # Number of periods to forecast
    prompt_type=PromptType.ZERO_SHOT,  # prompt type: ZERO_SHOT (no examples)
    ts_format=TSFormat.ARRAY,          # time series format
    ts_type=TSType.NUMERIC             # Type of encoding for series values
)
```

### Forecasting with LLMs
#### 6. Initializing an OpenAI model
```python
from llm4time.core.models import OpenAI

model = OpenAI(
  model='gpt-4o',  # OpenAI model to be used.
  api_key='...',   # API key for authentication with the OpenAI service.
  base_url='..'    # Base URL of the OpenAI endpoint.
)
```

#### 7. Predicting values
```python
# Forecasting
response, prompt_tokens, response_tokens, time_sec = model.predict(
    content,          # Previously generated prompt
    temperature=0.7,  # Level of randomness in the response
    max_tokens=1000   # Maximum number of tokens in the response
)

print("Model response:", response)
print("Prompt tokens:", prompt_tokens)
print("Response tokens:", response_tokens)
print("Execution time (s):", time_sec)
```

### Metric evaluation
#### 8. Error metrics

```python
from llm4time.core import formatter
from llm4time.core.evaluate.metrics import Metrics

# Converts the response string into a numerical list
y_pred = formatter.parse(
  response,
  ts_format=TSFormat.ARRAY,
  ts_type=TSType.NUMERIC
)

metrics = Metrics(y_val, y_pred)

# Error metrics
print(f"sMAPE: {metrics.smape}") # Symmetric Mean Absolute Percentage Error
print(f"MAE: {metrics.mae}")     # Mean Absolute Error
print(f"RMSE: {metrics.rmse}")   # Root Mean Squared Error
```

### Interactive evaluation
#### 9. Plots comparing actual and predicted values
```python
from llm4time.visualization import plots

# Generate a comparison plot between actual and predicted values
plots.plot_forecast("Comparison between actual and predicted values", y_val, y_pred)

# Generate a bar chart comparing descriptive statistics
plots.plot_forecast_statistics("Statistical comparison", y_val, y_pred)
```
---

## 🔍 References
```latex
@article{zairo2025prompt,
  title={Prompt-Driven Time Series Forecasting with Large Language Models},
  author={Zairo Bastos and João David Freitas and José Wellington Franco and Carlos Caminha},
  journal={Proceedings of the 27th International Conference on Enterprise Information Systems - Volume 1: ICEIS},
  year={2025}
}
```

## 👥 Team
<div align="center">
<table>
  <tr>
    <td align="center" nowrap>
      <a href="https://github.com/zairobastos"><img src="https://github.com/zairobastos.png" style="width: 80px; height: 80px;" alt="Zairo Bastos"/></a>
      <br />
      <sub><b>Zairo Bastos</b></sub>
      <br />
      <sub><i>Master’s student - UFC</i></sub>
      <br />
      <a href="mailto:zairobastos@gmail.com" title="Email">📧</a>
      <a href="https://www.linkedin.com/in/zairobastos/" title="LinkedIn">🔗</a>
    </td>
    <td align="center" nowrap>
      <a href="https://github.com/wesleey"><img src="https://github.com/wesleey.png" style="width: 80px; height: 80px;" alt="Wesley Barbosa"/></a>
      <br />
      <sub><b>Wesley Barbosa</b></sub>
      <br />
      <sub><i>Undergraduate student - UFC</i></sub>
      <br />
      <a href="mailto:wesley.barbosa.developer@gmail.com" title="Email">📧</a>
      <a href="https://www.linkedin.com/in/wesleybarbosasilva/" title="LinkedIn">🔗</a>
    </td>
    <td align="center" nowrap>
      <a href="https://github.com/fernandascarcela"><img src="https://github.com/fernandascarcela.png" style="width: 80px; height: 80px;" alt="Fernanda Scarcela"/></a>
      <br />
      <sub><b>Fernanda Scarcela</b></sub>
      <br />
      <sub><i>Undergraduate student - UFC</i></sub>
      <br />
      <a href="mailto:fernandascla@alu.ufc.br" title="Email">📧</a>
      <a href="https://www.linkedin.com/in/fernanda-scarcela-a95543220/" title="LinkedIn">🔗</a>
    </td>
    <td align="center" nowrap>
      <a href="https://lattes.cnpq.br/4380023778677961"><img src="https://raw.githubusercontent.com/zairobastos/LLM4Time/main/docs/assets/carlos.png" style="width: 80px; height: 80px;" alt="Carlos Caminha"/></a>
      <br />
      <sub><b>Carlos Caminha</b></sub>
      <br />
      <sub><i>Academic advisor - UFC</i></sub>
      <br />
      <a href="mailto:caminha@ufc.br" title="Email">📧</a>
      <a href="https://lattes.cnpq.br/4380023778677961" title="Lattes">🔗</a>
    </td>
    <td align="center" nowrap>
      <a href="https://lattes.cnpq.br/5168415467086883"><img src="https://raw.githubusercontent.com/zairobastos/LLM4Time/main/docs/assets/wellington.png" style="width: 80px; height: 80px;" alt="José Wellington Franco"/></a>
      <br />
      <sub><b>José Wellington Franco</b></sub>
      <br />
      <sub><i>Academic advisor - UFC</i></sub>
      <br />
      <a href="mailto:wellington@crateus.ufc.br" title="Email">📧</a>
      <a href="https://lattes.cnpq.br/5168415467086883" title="Lattes">🔗</a>
    </td>
  </tr>
</table>
</div>

## 📄 License
This project is licensed under the [MIT License](https://github.com/zairobastos/LLM4Time/blob/main/LICENSE).

## 📬 Contact
For questions, suggestions, or feedback:
- 📧 Email: [zairobastos@gmail.com](mailto:zairobastos@gmail.com)
- 🔗 LinkedIn: [Zairo Bastos](https://www.linkedin.com/in/zairobastos/)
