import streamlit as st
import pandas as pd
from lib.crud import crud_models
from utils.env import (
    normalize, save_model_env, rename_model_env, remove_model_env)

# LLM4Time
from llm4time.core.models import Provider
from llm4time.persistence.crud_models import ModelNotFoundError
from llm4time.persistence.crud_models import ModelAlreadyExistsError


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
  st.rerun()


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

st.write("### API")
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
        f"openai_{normalize(model)}_key": api_key,
        f"openai_{normalize(model)}_base_url": base_url
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
        f"azure_{normalize(model)}_key": api_key,
        f"azure_{normalize(model)}_api_version": api_version,
        f"azure_{normalize(model)}_endpoint": endpoint
    }
    save_model(model, Provider.AZURE, env_vars)
  elif save and (not model or not api_key or not api_version or not endpoint):
    st.toast(
        "Por favor, preencha todos os campos antes de salvar as configurações.",
        icon="⚠️"
    )


# ---------------- Dialog confirmação de exclusão ----------------

@st.dialog("Confirmar exclusão")
def confirmation_dialog(models: list[tuple[str, str]]):
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


# ---------------- Modelos Configurados ----------------

st.write("---")
st.write("### Modelos Configurados")
models = crud_models().select_all()

if models:
  info = []
  for model in models:
    model_id, model_name, provider = model
    info.append({
        "Modelo": f"🤖 {model_name}",
        "API": provider,
        "Remover": False
    })

  data = st.data_editor(
      pd.DataFrame(info),
      column_config={
          "Remover": st.column_config.CheckboxColumn(
              "Remover",
              help="Marque para remover o modelo",
              default=False,
              width=1
          )
      },
      disabled=["API"],
      hide_index=True,
      use_container_width=True
  )

  # Detecta e processa modelos renomeados automaticamente
  for idx, row in data.iterrows():
    old_model = models[idx][1]
    new_model = row["Modelo"].replace("🤖 ", "")
    provider = models[idx][2]
    if old_model != new_model:
      rename_model(old_model, new_model, provider)

  # Detecta modelos para excluir
  models_to_delete = []
  for idx, row in data.iterrows():
    if row["Remover"]:
      _, model, provider = models[idx]
      models_to_delete.append((model, provider))

  # 'Modelo' ou 'modelos'
  n = len(models_to_delete)
  s = "s" if n > 1 else ""

  if models_to_delete and st.button(label=f"🗑️ Remover {n} modelo{s}", type="primary"):
    confirmation_dialog(models_to_delete)
else:
  st.write("Nenhum modelo configurado.")


# ---------------- Prompt personalizado ----------------

st.write("---")
st.write("### Prompt Personalizado")
prompt = st.text_area(
    "Prompt",
    help="Digite o prompt que deseja utilizar.",
    placeholder="Ex: Prever a demanda de produtos para os próximos 30 dias.",
    height=200
)
save_prompt = st.button(
    "💾 Salvar Prompt",
    help="Clique para salvar o prompt.",
    type="primary",
)
