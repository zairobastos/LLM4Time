import pandas as pd
import streamlit as st
from lib.crud import crud_models
from lib.crud import crud_prompts
from utils.env import (
    normalize, save_model_env, rename_model_env, remove_model_env)

# LLM4Time
from llm4time.core.models import Provider
from llm4time.persistence.crud_models import ModelNotFoundError
from llm4time.persistence.crud_models import ModelAlreadyExistsError
from llm4time.persistence.crud_prompts import PromptNotFoundError
from llm4time.persistence.crud_prompts import PromptAlreadyExistsError


# ---------------- Funções utilitárias ----------------

def save_model(model: str, provider: Provider, env_vars: dict) -> None:
  """
  Registra o modelo no banco de dados e salva suas variáveis no .env.
  Exibe alerta se o modelo já existir.

  model (str): Nome do modelo.
  provider (Provider): Provedor da API.
  env_vars (dict): Dict com {chave: valor}.
  """
  try:
    crud_models().insert(
        name=model, provider=str(provider))
    save_model_env(env_vars)
    st.toast("Configurações salvas com sucesso!", icon="✅")
  except ModelAlreadyExistsError as e:
    print(f"[ERROR] {e}")
    st.toast(
        f"O modelo **{model}** para **{str(provider)}** já existe.", icon="❌")
  except Exception as e:
    st.toast(f"Erro ao salvar as configurações: {e}", icon="❌")


def remove_model(models: list[tuple]) -> None:
  """
  Remove um modelo do banco de dados e suas variáveis do .env.

  models (list[tuple]): Lista de tuplas (model, provider).
  """
  crud_models().remove_many(models)
  for model, provider in models:
    remove_model_env(model, Provider.enum(provider))


def rename_model(old_model: str, new_model: str, provider: str) -> None:
  """
  Renomeia um modelo do banco de dados e suas variáveis do .env.

  old_model (str): Nome do modelo antigo.
  new_model (str): Nome do modelo novo.
  provider (str): Nome do provedor da API.
  """
  try:
    crud_models().rename(
        old_name=old_model,
        new_name=new_model,
        provider=provider
    )
    rename_model_env(old_model, new_model, Provider.enum(provider))
    st.rerun()
  except ModelAlreadyExistsError as e:
    print(f"[ERROR] {e}")
    st.error(
        f"O modelo **{new_model}** para **{provider}** já existe.", icon="❌")
  except ModelNotFoundError as e:
    print(f"[ERROR] {e}")
    st.error(
        f"Modelo **{old_model}** para **{provider}** não encontrado.", icon="❌")
  except Exception as e:
    st.error(f"Erro ao renomear o modelo: {e}", icon="❌")


# ---------------- Estado inicial ----------------

# Inicializa o estado se ainda não estiver definido
if "mode" not in st.session_state:
  st.session_state.mode = Provider.LM_STUDIO  # padrão: LM Studio


# ---------------- Seleção de API ----------------

st.write(f"### API")
col1, col2, col3 = st.columns(3)
with col1:
  if st.button(
      "LM Studio",
      help="Acesse o LM Studio para executar modelos de linguagem localmente.",
      use_container_width=True,
      type="primary",
  ):
    st.session_state.mode = Provider.LM_STUDIO

with col2:
  if st.button(
      "OpenAI / Ollama",
      help="Acesse a API para executar modelos de linguagem remotamente.",
      use_container_width=True,
      type="primary",
  ):
    st.session_state.mode = Provider.OPENAI

with col3:
  if st.button(
      "OpenAI Azure",
      help="Acesse a API para executar modelos de linguagem remotamente.",
      use_container_width=True,
      type="primary",
  ):
    st.session_state.mode = Provider.AZURE


# ---------------- Configurações específicas ----------------

if st.session_state.mode == Provider.LM_STUDIO:
  st.write(
      "Você será redirecionado para o LM Studio. Caso não tenha o LM Studio instalado, "
      "você pode baixá-lo [aqui](https://lmstudio.ai)."
  )
  model = st.text_input(
      "Modelo",
      help="Digite o nome do modelo que deseja utilizar no LM Studio.",
      placeholder="Ex: deepseek-r1"
  )
  save = st.button(
      "💾 Salvar Configurações",
      help="Clique para salvar as configurações.",
      type="primary",
  )

elif st.session_state.mode == Provider.OPENAI:
  st.write(
      "Você será redirecionado para a API. Caso não tenha uma chave de API, "
      "você pode obter uma [aqui](https://platform.openai.com/signup)."
  )
  api_key = st.text_input(
      "Chave da API",
      type="password",
      help="Digite a chave da API que deseja utilizar.",
      placeholder="Ex: sk-1234567890abcdef1234567890abcdef1234567890abcdef"
  )
  model = st.text_input(
      "Modelo",
      help="Digite o nome do modelo que deseja utilizar.",
      placeholder="Ex: gpt-3.5-turbo"
  )
  base_url = st.text_input(
      "Base URL",
      help="Digite o base_url que deseja utilizar.",
      placeholder="Ex: my_base_url"
  )
  save = st.button(
      "💾 Salvar Configurações",
      help="Clique para salvar as configurações.",
      type="primary",
  )
  if api_key and model and base_url and save:
    env_vars = {
        normalize(f"{Provider.OPENAI}_{model}_key"): api_key,
        normalize(f"{Provider.OPENAI}_{model}_base_url"): base_url
    }
    save_model(model, Provider.OPENAI, env_vars)
  elif save and (not api_key or not model or not base_url):
    st.toast(
        "Por favor, preencha todos os campos antes de salvar as configurações.",
        icon="⚠️"
    )

elif st.session_state.mode == Provider.AZURE:
  st.write(
      "Você será redirecionado para a API. Caso não tenha uma chave de API, "
      "você pode obter uma [aqui](https://portal.azure.com)."
  )
  api_key = st.text_input(
      "Chave da API",
      type="password",
      help="Digite a chave da API que deseja utilizar.",
      placeholder="Ex: sk-1234567890abcdef1234567890abcdef1234567890abcdef"
  )
  model = st.text_input(
      "Modelo",
      help="Digite o nome do modelo que deseja utilizar.",
      placeholder="Ex: gpt-3.5-turbo"
  )
  api_version = st.text_input(
      "Versão da API",
      help="Digite a versão da API que deseja utilizar.",
      placeholder="Ex: 2024-05-01-preview"
  )
  endpoint = st.text_input(
      "Endpoint",
      help="Digite o endpoint que deseja utilizar.",
      placeholder="Ex: https://<resource-name>.services.ai.azure.com"
  )
  save = st.button(
      "💾 Salvar Configurações",
      help="Clique para salvar as configurações.",
      type="primary",
  )
  if model and api_key and api_version and endpoint and save:
    env_vars = {
        normalize(f"{Provider.AZURE}_{model}_key"): api_key,
        normalize(f"{Provider.AZURE}_{model}_api_version"): api_version,
        normalize(f"{Provider.AZURE}_{model}_endpoint"): endpoint
    }
    save_model(model, Provider.AZURE, env_vars)
  elif save and (not model or not api_key or not api_version or not endpoint):
    st.toast(
        "Por favor, preencha todos os campos antes de salvar as configurações.",
        icon="⚠️"
    )


# ---------------- Confirmação de exclusão de modelos ----------------

@st.dialog("Confirmar exclusão")
def models_dialog(models: list[tuple[str, str]]):
  n = len(models)

  if n == 1:
    model, provider = models[0]
    st.write(
        f"Tem certeza que deseja excluir o modelo **{model}** da API **{provider}**?")
  else:
    st.write(f"Tem certeza que deseja excluir **{n} modelos**?")

  st.caption("**⚠️ Esta ação não poderá ser desfeita.**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Cancelar", use_container_width=True):
      st.rerun()
  with col2:
    if st.button("Excluir", use_container_width=True, type="primary"):
      remove_model(models)
      st.rerun()


# ---------------- Modelos Configurados ----------------

st.write("---")
st.write("### Modelos Configurados")
models = crud_models().select_all()

if models:
  df_models = st.data_editor(
      pd.DataFrame([
          {"Modelo": f"🤖 {model_name}", "API": provider, "Excluir": False}
          for _, model_name, provider in models]),
      disabled=["API"],
      hide_index=True,
      use_container_width=True)

  # Detecta e processa modelos renomeados automaticamente
  for idx, row in df_models.iterrows():
    old_model = models[idx][1]
    new_model = row["Modelo"].replace("🤖 ", "")
    provider = models[idx][2]
    if old_model != new_model:
      rename_model(old_model, new_model, provider)

  # Detecta modelos para excluir
  models_to_delete = [
      (models[idx][1], models[idx][2])
      for idx, row in df_models.iterrows()
      if row["Excluir"]]

  # 'Modelo' ou 'modelos'
  n = len(models_to_delete)
  s = "s" if n > 1 else ""

  if models_to_delete and st.button(label=f"🗑️ Excluir {n} modelo{s}", type="primary"):
    models_dialog(models_to_delete)
else:
  st.info("Nenhum modelo encontrado.")


# ---------------- Prompt personalizado ----------------

st.write("---")
st.write("### Prompts Personalizados")

prompts = crud_prompts().select_all()
action = st.radio("Escolha a ação:", options=["Criar", "Editar"])
prompt_name, prompt_content, prompt_variables = "", "", {}

if action == "Criar":
  prompt_name = st.text_input("Nome", placeholder="Ex: Previsão de preços")

elif action == "Editar":
  prompt_name = st.selectbox("Prompt", options=[p["name"] for p in prompts])
  if prompt_name:
    try:
      prompt_data = crud_prompts().select(prompt_name)
      prompt_content = prompt_data["content"]
      prompt_variables = prompt_data["variables"]
    except PromptNotFoundError:
      st.error("Prompt não encontrado.")


df_variables = st.data_editor(
    pd.DataFrame(
        [{"Chave": k, "Valor": v} for k, v in prompt_variables.items()]
    ) if prompt_variables else pd.DataFrame(columns=["Chave", "Valor"]),
    hide_index=True,
    num_rows="dynamic",
    use_container_width=True
)
prompt_variables = {row["Chave"]: row["Valor"]
                    for _, row in df_variables.iterrows() if row["Chave"]}


col1, col2 = st.columns(2)
with col1:
  prompt_content = st.text_area(
      label="Prompt",
      value=prompt_content,
      placeholder="Ex: Faça a previsão dos próximos {n_periods_forecast} valores com base nos dados históricos fornecidos:\n\n{input}\n\nA saída deve ser uma lista contendo apenas os valores previstos.",
      label_visibility="collapsed",
      height=200)

with col2:
  global_variables = {
      "input": "Date,Value\n2016-07-01,38.662\n2016-07-01,37.124\n2016-07-01,36.465\n2016-07-01,33.609\n2016-07-01,31.851\n2016-07-01,30.532\n2016-07-01,30.093\n2016-07-01,29.873\n2016-07-01,29.653\n2016-07-01,29.213\n2016-07-01,27.456\n2016-07-01,27.456\n2016-07-01,27.236\n2016-07-01,26.577\n2016-07-01,26.797\n2016-07-01,26.797\n2016-07-01,26.797\n2016-07-01,26.577\n2016-07-01,26.577\n2016-07-01,26.138\n2016-07-01,26.138\n2016-07-01,25.698\n2016-07-01,25.918\n2016-07-01,25.918\n2016-07-02,25.918\n2016-07-02,26.358\n2016-07-02,26.138\n2016-07-02,25.698\n2016-07-02,25.698\n2016-07-02,25.918",
      "input_example": "Date,Value\n2016-07-01,38.662\n2016-07-01,37.124\n2016-07-01,36.465\n2016-07-01,33.609",
      "output_example": "Date,Value\n2016-07-01,38.662\n2016-07-01,37.124\n2016-07-01,36.465\n2016-07-01,33.609\n2016-07-01,31.851\n2016-07-01,30.532\n2016-07-01,30.093",
      "examples": (
          "Exemplo 1:\n"
          "Período (histórico):\nDate,Value\n2016-07-01,38.662\n2016-07-01,37.124\n2016-07-01,36.465\n2016-07-01,33.609\n2016-07-01,31.851\n2016-07-01,30.532\n2016-07-01,30.093\n\n"
          "Período (previsto):\nDate,Value\n2016-07-01,29.873\n2016-07-01,29.653\n2016-07-01,29.213\n2016-07-01,27.456\n2016-07-01,27.456\n2016-07-01,27.236\n2016-07-01,26.577\n"
      ),
      "n_periods_input": 30,
      "n_periods_forecast": 7,
      "n_periods_example": 7
  }
  try:
    global_variables.update(**prompt_variables)
    st.code(prompt_content.format(**global_variables), language="python", height=200)
  except KeyError as e:
    st.code(f"Erro: chave {e} não encontrada.", language="python", height=200)
  except Exception as e:
    st.code(f"Erro: {e}", language="python", height=200)


if st.button(
    "💾 Salvar Prompt",
    help="Clique para salvar o prompt",
    type="primary"
):
  try:
    if action == "Criar":
      crud_prompts().insert(name=prompt_name, content=prompt_content, variables=prompt_variables)
      st.rerun()

    elif action == "Editar":
      crud_prompts().update(prompt_name, prompt_content, prompt_variables)
      st.toast(f"Prompt **'{prompt_name}'** atualizado com sucesso!", icon="✅")

  except PromptAlreadyExistsError:
    st.warning(f"Já existe um prompt chamado **'{prompt_name}'**. Escolha outro nome.")
  except PromptNotFoundError:
    st.warning(f"Prompt **'{prompt_name}'** não encontrado.")
  except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")


# ---------------- Confirmação de exclusão de prompts ----------------

@st.dialog("Confirmar exclusão")
def prompts_dialog(prompt_names: list[str]):
  n = len(prompt_names)

  if n == 1:
    prompt_name = prompt_names[0]
    st.write(
        f"Tem certeza que deseja excluir o prompt **'{prompt_name}'**?")
  else:
    st.write(f"Tem certeza que deseja excluir **{n} prompts**?")

  st.caption("**⚠️ Esta ação não poderá ser desfeita.**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Cancelar", use_container_width=True):
      st.rerun()
  with col2:
    if st.button("Excluir", use_container_width=True, type="primary"):
      crud_prompts().remove_many(prompt_names)
      st.rerun()


# ---------------- Meus Prompts ----------------

st.write("---")
st.write("### Meus Prompts")

if prompts:
  df_prompts = st.data_editor(
      pd.DataFrame([
          {"Nome": f"📄 {p['name']}", "Excluir": False}
          for p in prompts]),
      hide_index=True,
      use_container_width=True)

  # Detecta e processa prompts renomeados automaticamente
  try:
    for idx, row in df_prompts.iterrows():
      old_name = prompts[idx]["name"]
      new_name = row["Nome"].replace("📄 ", "")
      if old_name != new_name:
        crud_prompts().rename(old_name, new_name)
  except PromptAlreadyExistsError:
    st.warning(f"Já existe um prompt chamado **'{new_name}'**. Escolha outro nome.")
  except PromptNotFoundError:
    st.warning(f"Prompt **'{old_name}'** não encontrado.")
  except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")

  # Detecta prompts para excluir
  prompts_to_delete = [
      prompts[idx]["name"]
      for idx, row in df_prompts.iterrows()
      if row["Excluir"]]

  # 'prompt' ou 'prompts'
  n = len(prompts_to_delete)
  s = "s" if n > 1 else ""

  if prompts_to_delete and st.button(label=f"🗑️ Excluir {n} prompt{s}", type="primary"):
    prompts_dialog(prompts_to_delete)
else:
  st.info("Nenhum prompt encontrado.")


# ---------------- Variáveis Globais ----------------

st.write("---")
st.write("### Variáveis Globais")
st.write("Use variáveis globais para criar prompts dinâmicos preenchidos em tempo de execução.")

st.table(pd.DataFrame([
    {"Chave": "`{input}`",
     "Valor": "Série temporal de entrada formatada conforme o formato e o tipo."},
    {"Chave": "`{input_example}`",
     "Valor": "Exemplo de entrada contendo os primeiros 4 períodos formatados."},
    {"Chave": "`{output_example}`",
     "Valor": "Exemplo de saída contendo o mesmo número de períodos a serem previstos formatados."},
    {"Chave": "`{examples}`",
     "Valor": "Exemplos contendo histórico e previsão, conforme a estratégia de amostragem."},
    {"Chave": "`{n_periods_input}`",
     "Valor": "Número total de períodos na série temporal de entrada."},
    {"Chave": "`{n_periods_forecast}`",
     "Valor": "Número de períodos a serem previstos."},
    {"Chave": "`{n_periods_example}`",
     "Valor": "Número de períodos em cada exemplo."},
]).style.set_properties(
    subset=["Valor"], **{"color": "gray"}))
