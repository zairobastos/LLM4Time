Pré-processamento e tratamento de dados
========================================

Este módulo contém todas as funcionalidades relacionadas ao carregamento,
pré-processamento, imputação e gerenciamento de dados para análise de séries temporais.

.. contents:: Sumário
    :local:

Leitura de dados
----------------
.. automodule:: llm4time.core.data.loader
   :members:
   :undoc-members:

Pré-processamento
-----------------
.. automodule:: llm4time.core.data.preprocessor
   :members:
   :undoc-members:

Métodos de imputação
--------------------
.. automodule:: llm4time.core.data.imputation
   :members:
   :undoc-members:

Gerenciamento de dados
----------------------
.. automodule:: llm4time.core.data.manager
   :members:
   :undoc-members:


Prompts e formatações
=====================

Este módulo contém todas as funcionalidades relacionadas à criação, formatação
e gerenciamento de prompts para modelos de linguagem aplicados a análise de séries temporais.

.. contents:: Sumário
    :local:

Tipos de prompts
----------------
.. automodule:: llm4time.core.prompts
   :members:
   :undoc-members:

Formatos de série temporal
--------------------------
.. automodule:: llm4time.core.formatting.parsers
   :members:
   :undoc-members:

Tipos de série temporal
-----------------------
.. automodule:: llm4time.core.formatting.encoders.decoders
   :members:
   :undoc-members:

Geração de prompts
------------------
.. automodule:: llm4time.core.prompt
   :members:
   :undoc-members:

Formatação de dados
-------------------
.. automodule:: llm4time.core.formatter
   :members:
   :undoc-members:


Previsão com LLMs
=================

Este módulo contém todas as funcionalidades relacionadas à utilização de modelos de linguagem
de grande escala (LLMs) para previsão e análise de séries temporais, incluindo diferentes
provedores de API e configurações de modelos.

.. contents:: Sumário
    :local:

Modelos
-------
.. automodule:: llm4time.core.models
   :members: Provider
   :undoc-members:

.. automodule:: llm4time.core.models.openai
   :members:
   :undoc-members:

.. automodule:: llm4time.core.models.azure
   :members:
   :undoc-members:

.. automodule:: llm4time.core.models.lmstudio
   :members:
   :undoc-members:


Métricas de avaliação
=====================

Este módulo contém todas as funcionalidades relacionadas à avaliação de performance
de modelos de previsão, incluindo métricas de erro, análises estatísticas e
indicadores específicos para séries temporais.

.. contents:: Sumário
    :local:

Métricas de erro
----------------
.. automodule:: llm4time.core.evaluate.metrics
   :members:
   :undoc-members:

Estatísticas
------------
.. automodule:: llm4time.core.evaluate.statistics
   :members:
   :undoc-members:

Avaliação de performance de previsões de séries temporais
---------------------------------------------------------
.. automodule:: llm4time.core.metrics
   :members:
   :undoc-members:


Visualização
============

Este módulo contém todas as funcionalidades relacionadas à criação de visualizações
e gráficos para análise de séries temporais.

.. contents:: Sumário
    :local:

Gráficos interativos
--------------------
.. automodule:: llm4time.visualization.plots
   :members:
   :undoc-members:
