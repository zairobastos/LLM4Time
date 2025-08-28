import streamlit as st
from datetime import datetime
import pandas as pd
import os

# ---------------- Funções utilitárias ----------------

def upload():
  """Lida com o processo de upload de um arquivo."""
  try:
    uploaded_file = st.session_state.uploaded_file
    df = pd.read_csv(uploaded_file)

    # Reseta as variáveis
    for var in ["columns", "duplicate_treatment", "regularize_data", "frequency", "frequency_interval",
                "impute_data", "imputation_method", "window", "span", "order", "csv_name"]:
      st.session_state[var] = None

    st.session_state.step = 1
    configuration_dialog(df, uploaded_file)

  except Exception as e:
    if uploaded_file is not None:
      st.toast(f"Erro ao carregar o arquivo: {e}", icon="🚨")


def rename_file(old_name, new_name):
  """Função para renomear arquivo."""
  try:
    original_path = os.path.join("uploads", old_name)
    new_path = os.path.join("uploads", new_name)

    # Valida nome do arquivo
    if not new_name.strip():
      st.error("❌ Nome do arquivo não pode estar vazio.")
      return

    # Verifica se o arquivo original existe
    if not os.path.exists(original_path):
      st.error(f"❌ Arquivo não encontrado: {old_name}")
      return

    # Verifica se o novo nome já existe
    if os.path.exists(new_path) and original_path != new_path:
      st.error(f"❌ Já existe um arquivo com o nome '{new_name}'.")
      return

    # Caracteres inválidos para nomes de arquivo
    invalid_chars = ['<','>',':','"','|','?','*','\\','/']
    if any(char in new_name for char in invalid_chars):
      st.error(f"❌ Nome contém caracteres especiais.")
      return

    os.rename(original_path, new_path)
    st.rerun()
  except Exception as e:
    st.error(f"❌ Erro ao renomear {old_name}: {str(e)}")

# ---------------- Dialog de tratamento de dados ----------------

@st.dialog("Seleção e Tratamento de Dados")
def configuration_dialog(dataset: str, uploaded_file: str):
  # --- ETAPA 1: Seleção das colunas e método de tratamento de dados ---
  if st.session_state.step == 1:
    columns_op = dataset.columns.tolist()
    date_col = st.selectbox("Selecione a coluna para a data:", columns_op, index=0, key="date_key", help="Coluna de referência temporal que indica quando cada valor foi registrado")
    value_col = st.selectbox("Selecione a coluna de valores:", columns_op, index=0, key="value_key", help="Coluna que contém os dados que você deseja prever")
    st.session_state.columns = {"date": date_col, "value": value_col}

    if date_col == value_col:
      st.warning("As colunas devem ser diferentes.")
    else:
      duplicate_treatment = st.radio("O que fazer com valores duplicados?", ["Manter o primeiro", "Manter o último", "Somar valores duplicados"], index=0, key="duplicate_treatment_key", help="Dados duplicados acontecem quando há repetição de datas na série temporal")
      st.session_state.duplicate_treatment = duplicate_treatment

  # --- ETAPA 2: Seleção de uniformidade e método de imputação de dados ---
  if st.session_state.step == 2:
    regularize_data = st.radio("Deseja uniformizar os dados?", ["Sim", "Não"], index=1, key="regularize_data_key", help="Garante que todas as datas entre o início e o fim do dataset estejam presentes")
    st.session_state.regularize_data = regularize_data

    if regularize_data == "Sim":
      col1, col2 = st.columns(2)
      with col1:
        frequency = st.selectbox("Frequência:", options=["Diário", "Semanal", "Mensal", "Anual", "Hora", "Minuto"], index=0, key="frequency_key", help="Define a unidade de tempo da série temporal (Diário, Semanal, Mensal, etc.)")
        st.session_state.frequency = frequency
      with col2:
        frequency_interval = st.number_input("Intervalo:", min_value=1, max_value=60, value=1, step=1, key="frequency_interval_key", help="Define a cada quantas unidades da frequência os dados serão considerados")
        st.session_state.frequency_interval = frequency_interval

    impute_data = st.radio("Deseja imputar os dados ausentes?", ["Sim", "Não"], index=1, key="impute_data_key", help="Preenche os valores ausentes do dataset conforme o método selecionado")
    st.session_state.impute_data = impute_data

    if impute_data == "Sim":
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
      imputation_method = st.selectbox("Selecione o método de imputação:", imputation_method_op, index=0, key="imputation_method_key")
      st.session_state.imputation_method = imputation_method

      if imputation_method == "Média Móvel Simples":
        st.session_state.window = st.slider("Tamanho da janela", min_value=1, max_value=30, value=3, key="window_key")
      elif imputation_method == "Média Móvel Exponencial":
        st.session_state.span = st.slider("Valor do span", min_value=1, max_value=30, value=3, key="span_key")
      elif imputation_method == "Interpolação Spline":
        st.session_state.order = st.slider("Ordem", min_value=1, max_value=5, value=2, key="order_key")

  # --- ETAPA 3: Nome do arquivo CSV ---
  if st.session_state.step == 3:
    st.session_state.csv_name = st.text_input("Nome para salvar o CSV", value=os.path.splitext(uploaded_file.name)[0], key="csv_name_key").strip()
    if os.path.isfile(f"uploads/{st.session_state.csv_name}.csv"):
      st.warning(f"Arquivo '{st.session_state.csv_name}.csv' já existe.")

  # -- BOTÕES --
  def next_step():
    st.session_state.step += 1

  def prev_step():
    st.session_state.step -= 1

  # Aplica as configurações no dataset
  def configure_dataset():
    # Cria uma cópia apenas das colunas selecionadas
    date_col = st.session_state.columns["date"]
    value_col = st.session_state.columns["value"]
    df = dataset[[date_col, value_col]].copy()

    # Renomeia as colunas para "date" e "value"
    df.rename(columns={date_col: "date", value_col: "value"}, inplace=True)
    # Ordena pela coluna "date" em ordem crescente
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values('date', ascending=True).reset_index(drop=True)

    # Aplica tratamento de dados duplicados
    duplicate_treatment = st.session_state.duplicate_treatment

    if duplicate_treatment == "Manter o primeiro":
      df = df.drop_duplicates(subset="date", keep="first")
    elif duplicate_treatment == "Manter o último":
      df = df.drop_duplicates(subset="date", keep="last")
    elif duplicate_treatment == "Somar valores duplicados":
      df = df.groupby("date", as_index=False)['value'].sum(min_count=1)

    # Garante intervalo completo de datas
    regularize_data = st.session_state.regularize_data
    frequency = st.session_state.frequency
    frequency_interval = st.session_state.frequency_interval

    if regularize_data == "Sim":
      freq_options = {"Diário": "D", "Semanal": "W", "Mensal": "M", "Anual": "Y", "Hora": "h", "Minuto": "min"}
      frequency = freq_options[frequency] if frequency_interval == 1 else f"{frequency_interval}{freq_options[frequency]}"
      df_range = pd.date_range(start=df["date"].min(), end=df["date"].max(), freq=frequency)
      df_range = pd.DataFrame({"date": df_range })
      df = pd.merge(df_range, df, on="date", how="left")

    # Aplica imputação de dados ausentes
    impute_data = st.session_state.impute_data
    imputation_method = st.session_state.imputation_method
    window = st.session_state.window
    span = st.session_state.span
    order = st.session_state.order

    if impute_data == "Sim":
      if imputation_method == "Média":
        df["value"] = df["value"].fillna(round(df["value"].mean(), 2))
      elif imputation_method == "Mediana":
        df["value"] = df["value"].fillna(df["value"].median())
      elif imputation_method == "Última Observação":
        df["value"] = df["value"].ffill().bfill()
      elif imputation_method == "Próxima Observação":
        df["value"] = df["value"].bfill().ffill()
      elif imputation_method == "Média Móvel Simples":
        df["value"] = df["value"].fillna(df["value"].rolling(window=window, min_periods=1).mean()).ffill().bfill()
      elif imputation_method == "Média Móvel Exponencial":
        df["value"] = df["value"].fillna(df["value"].ewm(span=span, adjust=False).mean()).ffill().bfill()
      elif imputation_method == "Interpolação Linear":
        df["value"] = df["value"].interpolate(method='linear').ffill().bfill()
      elif imputation_method == "Interpolação Spline":
        try:
          df["value"] = df["value"].interpolate(method='spline', order=order).ffill().bfill()
        except:
          df["value"] = df["value"].interpolate(method='linear').ffill().bfill()
      elif imputation_method == "Preencher com zero":
        df["value"] = df["value"].fillna(0)

    return df

  col1, col2 = st.columns(2, gap="large")
  with col1:
    if st.session_state.step > 1:
      st.button("Voltar", on_click=prev_step, use_container_width=True)
  with col2:
    if st.session_state.step == 3:
      csv_path = f"uploads/{st.session_state.csv_name}.csv"
      if st.button("Confirmar", use_container_width=True, type="primary", disabled=os.path.isfile(csv_path)):
        df = configure_dataset()
        df.to_csv(csv_path, index=False)
        st.rerun()
    else:
      disabled = False
      if st.session_state.step == 1:
        disabled = not (st.session_state.columns and
                        st.session_state.columns["date"] != st.session_state.columns["value"])
      st.button("Próximo", on_click=next_step, use_container_width=True, disabled=disabled)

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
          os.remove(f"uploads/{dataset}")
        except FileNotFoundError:
          st.toast(f"Arquivo '{dataset}' não encontrado.", icon="⚠️")
        except Exception as e:
          st.toast(f"Erro ao excluir '{dataset}': {str(e)}", icon="⚠️")
      st.rerun()

# ---------------- Interface do usuário ----------------

st.write("### Faça o upload do seu arquivo com os dados da série temporal.")
st.write("O arquivo deve conter uma coluna do tipo 'date' com as datas e outra coluna com os valores a serem previstos.")
uploaded_file = st.file_uploader("Escolha um arquivo", on_change=upload, key="uploaded_file", type="csv")


# ---------------- Datasets disponíveis ----------------

datasets = os.listdir("uploads") if os.path.exists("uploads") else []

if datasets:
  info = []
  for dataset in datasets:
    file_path = os.path.join("uploads", dataset)

    if os.path.exists(file_path):
      file_size = os.path.getsize(file_path)
      file_size_mb = round(file_size / (1024 * 1024), 2)

      mod_time = os.path.getmtime(file_path)
      mod_date = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")

      file_extension = os.path.splitext(dataset)[1].upper() or "CSV"

      try:
        row_count = len(pd.read_csv(file_path))
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
