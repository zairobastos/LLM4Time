import streamlit as st
import pandas as pd
from database.crud_models import CrudModels
import database.crud_models as Models
from api.api import Provider
from dotenv import set_key
import os

ENV_PATH = ".env"

# ---------------- Funções utilitárias ----------------

def save_model_env(env_vars: dict):
  """
  Salva as variáveis no .env.

  env_vars: Dict com {chave: valor}.
  """
  # Cria o arquivo .env se ele não existir
  if not os.path.exists(ENV_PATH):
    with open(ENV_PATH, 'w') as f:
      f.write("")

  # Salva cada chave/valor no .env
  for k, v in env_vars.items():
    set_key(ENV_PATH, k, v)

def rename_model_env(old_model: str, new_model: str, provider: str):
  """
  Renomeia variáveis de ambiente de um modelo no arquivo .env.
  Apenas o prefixo das chaves é alterado, os valores permanecem iguais.

  old_model: Nome atual do modelo.
  new_model: Novo nome para o modelo.
  provider: Provedor da API (ex: lmstudio, openai, azure).
  """
  old_prefix = f"{provider}_{old_model.replace('-', '_')}_"
  new_prefix = f"{provider}_{new_model.replace('-', '_')}_"
  if not os.path.exists(ENV_PATH): return
  with open(ENV_PATH) as f:
    lines = f.readlines()
  with open(ENV_PATH, "w") as f:
    for line in lines:
      if line.startswith(old_prefix):
        # Substitui apenas o prefixo, não altera valores
        f.write(line.replace(old_prefix, new_prefix, 1))
      else:
        f.write(line)

def remove_model_env(model: str, provider: str):
  """
  Remove variáveis de ambiente associadas a um modelo específico do arquivo .env.

  model: Nome do modelo.
  provider: Provedor da API (ex: lmstudio, openai, azure).
  """
  prefix = f"{provider}_{model.replace("-", "_")}_"
  if not os.path.exists(ENV_PATH): return
  with open(ENV_PATH) as f:
    lines = f.readlines()
  with open(ENV_PATH, "w") as f:
    for line in lines:
      if not line.startswith(prefix):
        f.write(line)

def save_model(model: str, provider: str, env_vars: dict):
  """
  Registra o modelo no banco de dados e salva suas variáveis no .env.
  Exibe alerta se o modelo já existir.

  model: Nome do modelo.
  provider: Provedor da API (lmstudio, openai, azure).
  env_vars: Dict com {chave: valor}.
  """
  try:
    CrudModels().insert(name=model, provider=provider)
    save_model_env(env_vars)
    st.toast("Configurações salvas com sucesso!", icon="✅")
  except Models.ModelAlreadyExistsError as e:
    print(f"[ERROR] {e}")
    provider_name = str(Provider(provider))
    st.toast(f"O modelo **{model}** para **{provider_name}** já existe.", icon="❌")
  except Exception as e:
    st.toast(f"Erro ao salvar as configurações: {e}", icon="❌")

def remove_model(models: list):
  """
  Remove um modelo do banco de dados e suas variáveis do .env.

  models: Lista de tuplas (model, provider).
  """
  CrudModels().remove_many(models)
  remove_model_env(model, provider)
  st.rerun()

def rename_model(old_model: str, new_model: str, provider: str):
  """
  Renomeia um modelo do banco de dados e suas variáveis do .env.

  old_model: Nome do modelo antigo.
  new_model: Nome do modelo novo.
  provider: Provedor da API (lmstudio, openai, azure).
  """
  try:
    CrudModels().rename(
      old_name=old_model,
      new_name=new_model,
      provider=provider
    )
    rename_model_env(old_model, new_model, provider)
    st.rerun()
  except Models.ModelAlreadyExistsError as e:
    print(f"[ERROR] {e}")
    provider_name = str(Provider(provider))
    st.error(f"O modelo **{new_model}** para **{provider_name}** já existe.", icon="❌")
  except Models.ModelNotFoundError as e:
    print(f"[ERROR] {e}")
    provider_name = str(Provider(provider))
    st.error(f"Modelo **{old_model}** para **{provider_name}** não encontrado.", icon="❌")
  except Exception as e:
    st.error(f"Erro ao renomear o modelo: {e}", icon="❌")

# ---------------- Estado inicial ----------------

# Inicializa o estado se ainda não estiver definido
if "mode" not in st.session_state:
  st.session_state.mode = "lmstudio"  # padrão: LM Studio

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
    st.session_state.mode = "lmstudio"

with col2:
  if st.button(
    "OpenAI / Ollama",
    help="Acesse a API para executar modelos de linguagem remotamente.",
    use_container_width=True,
    type="primary",
  ):
    st.session_state.mode = "openai"

with col3:
  if st.button(
    "OpenAI Azure",
    help="Acesse a API para executar modelos de linguagem remotamente.",
    use_container_width=True,
    type="primary",
  ):
    st.session_state.mode = "azure"

# ---------------- Configurações específicas ----------------

if st.session_state.mode == "lmstudio":
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
elif st.session_state.mode == "openai":
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
      f"openai_{model}_key".replace("-", "_"): api_key,
      f"openai_{model}_base_url".replace("-", "_"): base_url
    }
    save_model(model, "openai", env_vars)
  elif save and (not api_key or not model or not base_url):
    st.toast(
      "Por favor, preencha todos os campos antes de salvar as configurações.",
      icon="⚠️"
    )

elif st.session_state.mode == "azure":
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
      f"azure_{model}_key".replace("-", "_"): api_key,
      f"azure_{model}_api_version".replace("-", "_"): api_version,
      f"azure_{model}_endpoint".replace("-", "_"): endpoint
		}
    save_model(model, "azure", env_vars)
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
    provider_name = str(Provider(provider))
    st.write(f"Tem certeza que deseja excluir o modelo **{model}** da API **{provider_name}**?")
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
models = CrudModels().select_all()

if models:
  info = []
  for model in models:
      model_id, model_name, provider = model
      info.append({
        "Modelo": f"🤖 {model_name}",
        "API": str(Provider(provider)),
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
