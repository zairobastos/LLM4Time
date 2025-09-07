Introdução
==========

`LLM4Time <https://github.com/zairobastos/LLM4Time>`_ é uma biblioteca Python modular para previsão de séries temporais utilizando modelos de linguagem (LLMs). Ela oferece uma arquitetura flexível que permite o tratamento de dados, geração de prompts, previsão de séries temporais, avaliação de métricas e visualização interativa.

Key Features
------------

O LLM4Time oferece uma ampla gama de recursos. Alguns de seus principais recursos incluem:

- `Pré-processamento e tratamento de dados </LLM4Time/modules/root.html>`_
- `Geração de prompts e formatações </LLM4Time/modules/root.html#prompts-e-formatacoes>`_
- `Previsão com LLMs </LLM4Time/modules/root.html#previsao-com-llms>`_
- `Métricas de avaliação </LLM4Time/modules/root.html#metricas-de-avaliacao>`_
- `Visualização interativa </LLM4Time/modules/root.html#visualizacao>`_


Pré-processamento e tratamento de dados
=======================================

1. Carregamento dos dados
-------------------------

.. code-block:: python

  from llm4time.core.data import loader
  from llm4time.core.evaluate import Statistics

  # Carrega os dados CSV, XLSX, JSON ou Parquet
  df = loader.load_data("etth2.csv")

  # Estatísticas descritivas
  stats = Statistics(df['OT'])
  print(f"Média: {stats.mean}")
  print(f"Mediana: {stats.median}")
  print(f"1° Quartil: {stats.first_quartile}")
  print(f"3° Quartil: {stats.third_quartile}")
  print(f"Desvio padrão: {stats.std}")
  print(f"Mínimo: {stats.min}")
  print(f"Máximo: {stats.max}")
  print(f"Quantidade de dados ausentes: {stats.missing_count}")
  print(f"Percentual de dados ausentes: {stats.missing_percentage}")


2. Pré-processamento
--------------------

.. code-block:: python

  from llm4time.core.data import preprocessor

  # Padroniza para o formato de série temporal
  df = preprocessor.standardize(
    df,
    date_col='date',    # Nome da coluna que contém as datas/timestamps
    value_col='OT',     # Nome da coluna que contém os valores da série temporal
    duplicates='first'  # Como tratar linhas duplicadas: 'first' mantém a primeira ocorrência
  )

  # Garante que todas as datas/horas estejam presentes.
  df = preprocessor.normalize(df, freq='h')

3. Imputação de dados ausentes
------------------------------

.. code-block:: python

  from llm4time.core.data import imputation

  # Substitui os valores ausentes pela média da coluna 'value'.
  df = imputation.mean(df)

4. Divisão dos dados
--------------------

.. code-block:: python

  from llm4time.core.data import preprocessor

  # Divide o conjunto de dados em treinamento e validação
  train, y_val = preprocessor.split(
    df,
    start_date='2016-06-01 00:00:00', # Início do conjunto de treinamento
    end_date='2016-12-01 00:00:00',   # Fim do conjunto de treinamento
    periods=24                        # Número de períodos para previsão
  )


Geração de prompts
==================

5. Gerando prompt zero-shot
---------------------------

.. code-block:: python

  from llm4time.core import prompt
  from llm4time.core import PromptType, TSFormat, TSType

  content = prompt.generate(
      train,       # Conjunto de treino [(date, value), ...]
      periods=24,  # Número de períodos que queremos prever
      prompt_type=PromptType.ZERO_SHOT,  # Tipo de prompt: ZERO_SHOT (sem exemplos)
      ts_format=TSFormat.ARRAY,          # Formato da série temporal
      ts_type=TSType.NUMERIC             # Tipo de codificação dos valores da série
  )


Previsão com LLMs
=================

6. Instanciando um modelo OpenAI
--------------------------------

.. code-block:: python

  from llm4time.core.models import OpenAI

  model = OpenAI(
    model='gpt-4o',  # Nome do modelo OpenAI a ser utilizado.
    api_key='...',   # Chave de API para autenticação no serviço OpenAI.
    base_url='..'    # URL base do endpoint OpenAI.
  )

7. Gerando uma previsão
-----------------------

.. code-block:: python

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


Avaliação de métricas
=====================

8. Métricas de erro
-------------------

.. code-block:: python

  from llm4time.core import formatter
  from llm4time.core.metrics import evaluate

  # Converte a string da resposta em uma lista numérica.
  y_pred = formatter.parse(
    response,
    ts_format=TSFormat.ARRAY,
    ts_type=TSType.NUMERIC
  )

  metrics, val_stats, pred_stats = evaluate(y_val, y_pred)

  # Métricas de erro
  print(f"sMAPE: {metrics.smape}") # Erro percentual simétrico médio
  print(f"MAE: {metrics.mae}")     # Erro absoluto médio
  print(f"RMSE: {metrics.rmse}")   # Raiz do erro quadrático médio


Visualização interativa
=======================

9. Gráficos comparativos entre valores reais e previstos
--------------------------------------------------------

.. code-block:: python

  from llm4time.visualization import plots

  # Gera um gráfico comparativo entre valores reais e previstos.
  plots.plot_forecast("Comparação entre valores reais e previstos", y_val, y_pred)

  # Gera um gráfico de barras comparando estatísticas descritivas.
  plots.plot_forecast_statistics("Comparação estatística", y_val, y_pred)


Referências
===========

.. code-block:: latex

  @article{zairo2025prompt,
    title={Prompt-Driven Time Series Forecasting with Large Language Models},
    author={Zairo Bastos and João David Freitas and José Wellington Franco and Carlos Caminha},
    journal={Proceedings of the 27th International Conference on Enterprise Information Systems - Volume 1: ICEIS},
    year ={2025},
  }


Licença
=======

Este projeto está licenciado sob a `MIT License <https://github.com/zairobastos/LLM4Time/blob/main/LICENSE>`_.


Contato
=======

Em caso de dúvidas, sugestões ou feedback:

- 📧 E-mail: zairobastos@gmail.com
- 🔗 LinkedIn: `Zairo Bastos <https://www.linkedin.com/in/zairobastos/>`_
