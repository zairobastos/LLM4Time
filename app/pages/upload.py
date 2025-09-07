import streamlit as st
from utils.paths import abspath
from datetime import datetime
import pandas as pd
import os

# LLM4Time
from llm4time.core.data import loader
from llm4time.core.data import preprocessor
from llm4time.core.data import imputation
from llm4time.core.data import manager


# ---------------- Funções utilitárias ----------------

def upload():
  uploaded_file = st.session_state.uploaded_file
  try:
    # Reseta as variáveis
    for var in ["columns", "standardize_op", "normalize_op", "freq",
                "freq_interval", "imputation_op", "imputation_method",
                "window", "span", "order", "file"]:
      st.session_state[var] = None
    st.session_state.step = 1

    _, ext = os.path.splitext(uploaded_file.name)
    ext = ext.lower()

    if ext in ".csv":
      df = pd.read_csv(uploaded_file)
    elif ext in ".xlsx":
      df = pd.read_excel(uploaded_file)
    elif ext == ".json":
      df = pd.read_json(uploaded_file)
    elif ext == ".parquet":
      df = pd.read_parquet(uploaded_file)
    else:
      st.toast(f"Extensão não suportada: {ext}", icon="🚨")
      return

    configuration_dialog(df)
  except Exception as e:
    if uploaded_file is not None:
      st.toast(f"Erro ao carregar o arquivo: {e}", icon="🚨")


def rename_file(old_name, new_name):
  """Função para renomear arquivo."""
  try:
    original_path = abspath(f"uploads/{old_name}")
    new_path = abspath(f"uploads/{new_name}")

    # Valida nome do arquivo.
    if not new_name.strip():
      st.error("❌ Nome do arquivo não pode estar vazio.")
      return

    # Verifica se o arquivo original existe.
    if not os.path.exists(original_path):
      st.error(f"❌ Arquivo não encontrado: {old_name}")
      return

    # Verifica se o novo nome já existe.
    if os.path.exists(new_path) and original_path != new_path:
      st.error(f"❌ Já existe um arquivo com o nome '{new_name}'.")
      return

    # Caracteres inválidos para nomes de arquivo.
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    if any(char in new_name for char in invalid_chars):
      st.error(f"❌ Nome contém caracteres especiais.")
      return

    os.rename(original_path, new_path)
    st.rerun()
  except Exception as e:
    st.error(f"❌ Erro ao renomear {old_name}: {str(e)}")


# ---------------- Dialog de tratamento de dados ----------------

@st.dialog("Seleção e Tratamento de Dados")
def configuration_dialog(df):
  # --- ETAPA 1: Seleção das colunas e método de tratamento de dados ---
  if st.session_state.step == 1:
    columns = df.columns.tolist()
    date_col = st.selectbox("Selecione a coluna para a data:", columns, index=0, key="date_key",
                            help="Coluna de referência temporal que indica quando cada valor foi registrado.")
    value_col = st.selectbox("Selecione a coluna de valores:", columns, index=0, key="value_key",
                             help="Coluna que contém os dados que você deseja prever.")
    st.session_state.columns = {"date": date_col, "value": value_col}

    if date_col == value_col:
      st.warning("As colunas devem ser diferentes.")
    else:
      standardize_op = st.radio("O que fazer com valores duplicados?", ["Manter o primeiro", "Manter o último", "Somar valores duplicados"],
                                index=0, key="standardize_op_key", help="Dados duplicados acontecem quando há repetição de datas na série temporal.")
      st.session_state.standardize_op = standardize_op

  # --- ETAPA 2: Seleção de normalização e método de imputação de dados ---
  if st.session_state.step == 2:
    normalize_op = st.radio("Deseja normalizar os dados?", ["Sim", "Não"],
                            index=1, key="normalize_op_key", help="Garante que todas as datas/horas entre o início e o fim do dataset estejam presentes.")
    st.session_state.normalize_op = normalize_op

    if normalize_op == "Sim":
      col1, col2 = st.columns(2)
      with col1:
        freq = st.selectbox("Frequência:", options=["Diário", "Semanal", "Mensal", "Anual", "Hora", "Minuto"], index=0,
                            key="freq_key", help="Define a unidade de tempo da série temporal (Diário, Semanal, Mensal, etc.)")
        st.session_state.freq = freq
      with col2:
        freq_interval = st.number_input("Intervalo:", min_value=1, max_value=60, value=1, step=1,
                                        key="freq_interval_key", help="Define a cada quantas unidades da frequência os dados serão considerados.")
        st.session_state.freq_interval = freq_interval

    imputation_op = st.radio("Deseja imputar os valores ausentes?", ["Sim", "Não"],
                             index=1, key="imputation_op_key", help="Preenche os valores ausentes do dataset conforme o método selecionado.")
    st.session_state.imputation_op = imputation_op

    if imputation_op == "Sim":
      imputation_method_op = [
          "Média",
          "Mediana",
          "Última Observação",
          "Próxima Observação",
          "Média Móvel Simples",
          "Média Móvel Exponencial",
          "Interpolação Linear",
          "Interpolação Spline",
          "Preencher com zero"
      ]
      imputation_method = st.selectbox(
          "Selecione o método de imputação:", imputation_method_op, index=0, key="imputation_method_key")
      st.session_state.imputation_method = imputation_method

      if imputation_method == "Média Móvel Simples":
        st.session_state.window = st.slider(
            "Tamanho da janela", min_value=1, max_value=30, value=3, key="window_key")
      elif imputation_method == "Média Móvel Exponencial":
        st.session_state.span = st.slider(
            "Valor do span", min_value=1, max_value=30, value=3, key="span_key")
      elif imputation_method == "Interpolação Spline":
        st.session_state.order = st.slider(
            "Ordem", min_value=1, max_value=5, value=2, key="order_key")

  # --- ETAPA 3: Nome do arquivo ---
  if st.session_state.step == 3:
    uploaded_file = st.session_state.uploaded_file
    st.session_state.file = st.text_input(
        "Salvar arquivo como:", value=uploaded_file.name, key="file_key").strip()
    if os.path.isfile(abspath(f"uploads/{st.session_state.file}")):
      st.warning(f"Arquivo '{st.session_state.file}' já existe.")

  # -- BOTÕES --
  def next_step():
    st.session_state.step += 1

  def prev_step():
    st.session_state.step -= 1

  # Aplica as configurações no dataset
  def configure_dataset(df):
    # Aplica tratamento de dados duplicados
    date_col = st.session_state.columns["date"]
    value_col = st.session_state.columns["value"]
    standardize_op = st.session_state.standardize_op

    print(df.columns)

    if standardize_op == "Manter o primeiro":
      df = preprocessor.standardize(df, date_col, value_col, duplicates='first')
    elif standardize_op == "Manter o último":
      df = preprocessor.standardize(df, date_col, value_col, duplicates='last')
    elif standardize_op == "Somar valores duplicados":
      df = preprocessor.standardize(df, date_col, value_col, duplicates='sum')

    # Garante intervalo completo de datas
    normalize_op = st.session_state.normalize_op

    if normalize_op == "Sim":
      freq = {"Diário": "D", "Semanal": "W",
              "Mensal": "M", "Anual": "Y",
              "Hora": "h", "Minuto": "min"}[st.session_state.freq]
      freq_interval = st.session_state.freq_interval
      freq = freq if freq_interval == 1 else f"{freq_interval}{freq}"
      df = preprocessor.normalize(df, freq)

    # Aplica imputação de dados ausentes
    imputation_op = st.session_state.imputation_op
    imputation_method = st.session_state.imputation_method

    if imputation_op == "Sim":
      if imputation_method == "Média":
        df = imputation.mean(df, decimals=2)
      elif imputation_method == "Mediana":
        df = imputation.median(df)
      elif imputation_method == "Última Observação":
        df = imputation.ffill(df)
      elif imputation_method == "Próxima Observação":
        df = imputation.bfill(df)
      elif imputation_method == "Média Móvel Simples":
        window = st.session_state.window
        df = imputation.sma(df, window)
      elif imputation_method == "Média Móvel Exponencial":
        span = st.session_state.span
        df = imputation.ema(df, span)
      elif imputation_method == "Interpolação Linear":
        df = imputation.linear_interpolation(df)
      elif imputation_method == "Interpolação Spline":
        order = st.session_state.order
        df = imputation.spline_interpolation(df, order)
      elif imputation_method == "Preencher com zero":
        df = imputation.zero(df)

    return df

  col1, col2 = st.columns(2, gap="large")
  with col1:
    if st.session_state.step > 1:
      st.button("Voltar", on_click=prev_step, use_container_width=True)
  with col2:
    if st.session_state.step == 3:
      path = abspath(f"uploads/{st.session_state.file}")
      if st.button("Confirmar", use_container_width=True, type="primary", disabled=os.path.isfile(path)):
        df = configure_dataset(df)
        manager.save(df, path)
        st.rerun()
    else:
      disabled = False
      if st.session_state.step == 1:
        disabled = not (st.session_state.columns and
                        st.session_state.columns["date"] != st.session_state.columns["value"])
      st.button("Próximo", on_click=next_step,
                use_container_width=True, disabled=disabled)


# ---------------- Dialog confirmação de exclusão ----------------

@st.dialog("Confirmar exclusão")
def confirmation_dialog(datasets: list):
  count = len(datasets)

  if count == 1:
    st.write(f"Tem certeza que deseja excluir o dataset **{datasets[0]}**?")
  else:
    st.write(f"Tem certeza que deseja excluir **{count} datasets**?")

  st.caption("**⚠️ Esta ação não poderá ser desfeita.**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Cancelar", use_container_width=True):
      st.rerun()
  with col2:
    if st.button("Excluir", use_container_width=True, type="primary"):
      for dataset in datasets:
        try:
          os.remove(abspath(f"uploads/{dataset}"))
        except FileNotFoundError:
          st.toast(f"Arquivo '{dataset}' não encontrado.", icon="⚠️")
        except Exception as e:
          st.toast(f"Erro ao excluir '{dataset}': {str(e)}", icon="⚠️")
      st.rerun()


# ---------------- Interface do usuário ----------------

st.write("### Faça o upload do seu arquivo com os dados da série temporal.")
st.write("O arquivo deve conter uma coluna com as datas e outra coluna com os valores a serem previstos.")
uploaded_file = st.file_uploader(
    "Escolha um arquivo",
    on_change=upload,
    key="uploaded_file",
    type=["csv", "xlsx", "json", "parquet"]
)


# ---------------- Datasets disponíveis ----------------

datasets = os.listdir(abspath("uploads")) if os.path.exists(abspath("uploads")) else []

if datasets:
  info = []
  for dataset in datasets:
    file = abspath(f"uploads/{dataset}")

    if os.path.exists(file):
      file_size = os.path.getsize(file)
      file_size_mb = round(file_size / (1024 * 1024), 2)

      mod_time = os.path.getmtime(file)
      mod_date = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")

      file_extension = os.path.splitext(dataset)[1].upper() or "CSV"

      try:
        row_count = len(loader.load_data(file))
      except Exception:
        row_count = "N/A"
    else:
      file_size_mb = 0
      mod_date = "N/A"
      file_extension = "N/A"

    info.append({
        "Arquivo": f"📁 {dataset}",
        "Tipo": file_extension,
        "Linhas": row_count,
        "Tamanho (MB)": file_size_mb,
        "Modificação": mod_date,
        "Excluir": False
    })

  data = st.data_editor(
      pd.DataFrame(info),
      column_config={
          "Excluir": st.column_config.CheckboxColumn(
              "Excluir",
              help="Marque para excluir o arquivo",
              default=False
          )
      },
      disabled=["Linhas", "Tipo", "Tamanho (MB)", "Modificação"],
      hide_index=True,
      use_container_width=True
  )

  # Detecta e processa arquivos renomeados automaticamente
  for idx, row in data.iterrows():
    old_name = datasets[idx]
    new_name = row["Arquivo"].replace("📁 ", "")
    if old_name != new_name:
      rename_file(old_name, new_name)

  # Detecta arquivos para excluir
  datasets_to_delete = []
  for idx, row in data.iterrows():
    if row["Excluir"]:
      datasets_to_delete.append(datasets[idx])

  # 'Dataset' ou 'datasets'
  n = len(datasets_to_delete)
  s = "s" if n > 1 else ""

  if datasets_to_delete and st.button(label=f"Remover {n} dataset{s}"):
    confirmation_dialog(datasets_to_delete)
