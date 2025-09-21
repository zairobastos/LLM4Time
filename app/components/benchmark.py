import pandas as pd
import streamlit as st
import plotly.express as px

# LLM4Time
from llm4time.core.evaluate.metrics import Metrics


class Benchmark:
  """
  Classe especializada em componentes da página 'benchmark'.
  """

  @staticmethod
  def best_models_section():
    """
    Exibe uma tabela com os melhores modelos de linguagem.
    """
    df2 = pd.DataFrame({
        'Posição': [1, 2, 3],
        'Modelo': ['GPT-4', 'Claude 3', 'Gemini Pro'],
        'Pontuação': [100, 95, 90],
        'Organização': ['OpenAI', 'Anthropic', 'Google DeepMind'],
        'Licença': ['Comercial', 'Comercial', 'Comercial'],
    })

    st.dataframe(
        data=df2,
        column_config={
            'Posição': st.column_config.NumberColumn(
                format="# %s",
                pinned='left',
                help="Posição do modelo no ranking"
            ),
            'Modelo': st.column_config.TextColumn(
                help="Nome do modelo de linguagem"
            ),
            'Pontuação': st.column_config.NumberColumn(
                format="%d",
                help="Pontuação do modelo em tarefas específicas"
            ),
            'Organização': st.column_config.TextColumn(
                help="Organização responsável pelo modelo"
            ),
            'Licença': st.column_config.TextColumn(
                help="Tipo de licença do modelo"
            )
        },
        hide_index=True,
        use_container_width=True
    )

  @staticmethod
  def best_results_section(results: list, col_names: list):
    """
    Exibe os melhores resultados experimentais agrupados
    por configuração e com base nas métricas de erro.
    """
    df = pd.DataFrame(results, columns=col_names)

    # Filtra apenas colunas necessárias
    cols_to_show = ["dataset", "model", "temperature",
                    "ts_type", "prompt_type", "examples",
                    "sampling", "ts_format", "periods",
                    "response_time", "smape", "mae", "rmse"]
    df = df[[c for c in cols_to_show if c in df.columns]]

    # Seleciona melhores resultados
    sort_cols = ["smape", "mae", "rmse"]
    group_cols = ["dataset", "model", "temperature",
                  "ts_type", "prompt_type", "examples",
                  "sampling", "ts_format", "periods"]
    df_best = (df.sort_values(by=sort_cols)
               .groupby(group_cols, as_index=False)
               .first())

    # Calcula SEM
    df_sem = (df.groupby(group_cols)
                .agg(
                    sem_smape=("smape", lambda x: Metrics.sem(x.tolist())),
                    sem_mae=("mae", lambda x: Metrics.sem(x.tolist())),
                    sem_rmse=("rmse", lambda x: Metrics.sem(x.tolist())),
                    runs=("smape", "count"))
                .reset_index())
    df_best = df_best.merge(df_sem, on=group_cols, how="left")

    # Renomeia colunas
    df_best = df_best.rename(columns={
        "dataset": "Dataset",
        "model": "Modelo",
        "temperature": "Temperatura",
        "ts_type": "Série",
        "prompt_type": "Prompt",
        "ts_format": "Formato",
        "examples": "Exemplos",
        "sampling": "Amostragem",
        "periods": "Períodos",
        "response_time": "Tempo (s)",
        "smape": "sMAPE",
        "mae": "MAE",
        "rmse": "RMSE",
        "sem": "SEM",
        "sem_smape": "SEM (sMAPE)",
        "sem_mae": "SEM (MAE)",
        "sem_rmse": "SEM (RMSE)",
        "runs": "Execuções"
    })

    st.dataframe(
        data=df_best,
        column_config={
            "Dataset": st.column_config.TextColumn(help="Nome do dataset"),
            "Modelo": st.column_config.TextColumn(help="Nome do modelo de linguagem"),
            "Temperatura": st.column_config.NumberColumn(help="Parâmetro de temperatura usado no modelo"),
            "Série": st.column_config.TextColumn(help="Tipo de série temporal"),
            "Prompt": st.column_config.TextColumn(help="Tipo de prompt utilizado"),
            "Formato": st.column_config.TextColumn(help="Formato da série temporal"),
            "Examplos": st.column_config.NumberColumn(help="Número de exemplos"),
            "Amostragem": st.column_config.TextColumn(help="Estratégia de amostragem"),
            "Períodos": st.column_config.NumberColumn(help="Número de períodos previstos"),
            "Tempo (s)": st.column_config.NumberColumn(help="Tempo de execução em segundos"),
            "sMAPE": st.column_config.NumberColumn(help="Erro percentual simétrico médio"),
            "MAE": st.column_config.NumberColumn(help="Erro absoluto médio"),
            "RMSE": st.column_config.NumberColumn(help="Raiz do erro quadrático médio"),
            "SEM (sMAPE)": st.column_config.NumberColumn(help="Erro padrão da média (sMAPE)"),
            "SEM (MAE)": st.column_config.NumberColumn(help="Erro padrão da média (MAE)"),
            "SEM (RMSE)": st.column_config.NumberColumn(help="Erro padrão da média (RMSE)"),
            "Execuções": st.column_config.NumberColumn(help="Número de vezes que a configuração foi rodada")
        },
        hide_index=True,
        use_container_width=True)
