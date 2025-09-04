<div align="center">

# 📊  LLM4Time

Uma biblioteca para previsão de séries temporais com modelos de linguagem.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TcQ9RPNrtPHSq5gaMXfBTEV7uEpMA66w?usp=sharing)
[![PyPI version](https://img.shields.io/pypi/v/llm4time.svg)](https://pypi.org/project/llm4time/)
![Python versions](https://img.shields.io/badge/python-3.10+-blue)
[![License](https://img.shields.io/github/license/zairobastos/llm4time.svg)](https://github.com/zairobastos/LLM4Time/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-Sphinx-blue)](https://zairobastos.github.io/LLM4Time/)
</div>

<p align="center">
  <a href="#-get-started">Get Started</a> •
  <a href="https://zairobastos.github.io/LLM4Time/">Documentação</a> •
  <a href="#-referencias">Referências</a> •
  <a href="#-contato">Contato</a>
</p>

## 🧩 Get Started
**LLM4Time** é uma biblioteca Python para previsão de séries temporais com **modelos de linguagem (LLMs)**.
Ela fornece uma arquitetura modular que abrange:
- [Pré-processamento e tratamento de dados](#pré-processamento-e-tratamento-de-dados)
- [Geração de prompts](#geração-de-prompts)
- [Previsão com LLMs](#previsão-com-llms)
- [Avaliação de métricas](#avaliação-de-métricas)
- [Visualização interativa](#visualização-interativa)

### Instalação
```bash
pip install llm4time
```

### Rodando a interface Streamlit
Além disso, disponibilizamos uma interface via Streamlit, proporcionando uma interação mais intuitiva e prática com a biblioteca.

Siga os passos abaixo para clonar o repositório, configurar o ambiente e executar a aplicação.

#### 1. Clone o repositório
```bash
git clone https://github.com/zairobastos/LLM4Time.git
cd LLM4Time
```
#### 2. Crie e ative um ambiente virtual (Opcional)
```bash
python -m venv venv
source venv/bin/activate      # Bash/Zsh
source venv/bin/activate.fish # Fish Shell
```
#### 3. Instale as dependências
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-streamlit.txt
```
#### 4. Execute a aplicação
Usando python 🐍
```bash
python app/main.py
```
> Acesse a aplicação em `http://localhost:8501`

Ou usando docker 🐋
```bash
docker compose up
```

### Pré-processamento e tratamento de dados
#### 1. Carregamento dos dados
```python
from llm4time.core.data import loader

# Cria um dataset com as colunas 'date' e 'value'.
df = loader.load_data(
  'etth2.csv',        # Caminho do arquivo CSV com os dados
  date_col='date',    # Nome da coluna que contém as datas/timestamps
  value_col='OT',     # Nome da coluna que contém os valores da série temporal
  duplicates='first'  # Como tratar linhas duplicadas: 'first' mantém a primeira ocorrência
)
```
#### 2. Pré-processamento
```python
from llm4time.core.data import preprocessor

# Garante que todas as datas dentro do intervalo estejam presentes.
df = preprocessor.normalize(
  df,
  freq='h',  # Frequência da série temporal ('h' = hora, 'd' = dia, etc.)
  start='2016-07-01 00:00:00',
  end='2018-06-26 19:00:00'
)
```

#### 3. Imputação de dados ausentes
```python
from llm4time.core.data import imputation

# Substitui os valores ausentes pela média da coluna 'value'.
df = imputation.mean(df)
```

#### 4. Divisão dos dados
```python
from llm4time.core.data import preprocessor

# Divide o conjunto de dados em treinamento e validação
train, y_val = preprocessor.split(
  df,
  start_date='2016-06-01 00:00:00', # Início do conjunto de treinamento
  end_date='2016-12-01 00:00:00',   # Fim do conjunto de treinamento
  periods=24                        # Número de períodos para previsão
)
```
### Geração de prompts
#### 5. Gerando prompt zero-shot
```python
from llm4time.core import prompt
from llm4time.core import PromptType, TSFormat, TSType

content = prompt.generate(
    train,       # Conjunto de treino [(date, value), ...]
    periods=24,  # Número de períodos que queremos prever
    prompt_type=PromptType.ZERO_SHOT,  # Tipo de prompt: ZERO_SHOT (sem exemplos)
    ts_format=TSFormat.ARRAY,          # Formato da série temporal
    ts_type=TSType.NUMERIC             # Tipo de codificação dos valores da série
)
```

### Previsão com LLMs
#### 6. Instanciando um modelo OpenAI
```python
  from llm4time.core.models import OpenAI

  model = OpenAI(
    model='gpt-4o',  # Nome do modelo OpenAI a ser utilizado.
    api_key='...',   # Chave de API para autenticação no serviço OpenAI.
    base_url='..'    # URL base do endpoint OpenAI.
  )
```

#### 7. Gerando uma previsão
```python
# Gera a previsão
response, prompt_tokens, response_tokens, time_sec = model.predict(
    content,          # Prompt previamente gerado
    temperature=0.7,  # Grau de aleatoriedade da resposta
    max_tokens=1000   # Número máximo de tokens na resposta
)

print("Resposta do modelo:", response)
print("Número de tokens do prompt:", prompt_tokens)
print("Número de tokens da resposta:", response_tokens)
print("Tempo de execução (s):", time_sec)
```

### Avaliação de métricas
#### 8. Métricas de erro

```python
from llm4time.core import formatter
from llm4time.core.metrics import evaluate

# Converte a string da resposta em uma lista numérica.
y_pred = formatter.parse(
  response,
  ts_format=TSFormat.ARRAY,
  ts_type=TSType.NUMERIC
)

"""
sMAPE: Erro percentual simétrico médio.
MAE: Erro absoluto médio.
RMSE: Raiz do erro quadrático médio.
"""
smape, mae, rmse = evaluate(y_val, y_pred)
print(f"sMAPE: {smape}")
print(f"MAE: {mae}")
print(f"RMSE: {rmse}")
```

### Visualização interativa
#### 9. Gráficos comparativos entre valores reais e previstos
```python
from llm4time.visualization import plots

# Gera um gráfico comparativo entre valores reais e previstos.
plots.plot_forecast("Comparação entre valores reais e previstos", y_val, y_pred)

# Gera um gráfico de barras comparando estatísticas descritivas.
plots.plot_forecast_statistics("Comparação estatística", y_val, y_pred)
```
---

## 🔍 Referências

```latex
@article{zairo2025prompt,
  title={Prompt-Driven Time Series Forecasting with Large Language Models},
  author={Zairo Bastos and João David Freitas and José Wellington Franco and Carlos Caminha},
  journal={Proceedings of the 27th International Conference on Enterprise Information Systems - Volume 1: ICEIS},
  year ={2025},
}
```

## 📄 Licença

Este projeto está licenciado sob a [MIT License](https://github.com/zairobastos/LLM4Time/blob/main/LICENSE).

## 📬 Contato

Em caso de dúvidas, sugestões ou feedback:

- 📧 E-mail: [zairobastos@gmail.com](mailto:zairobastos@gmail.com)
- 🔗 LinkedIn: [Zairo Bastos](https://www.linkedin.com/in/zairobastos/)
