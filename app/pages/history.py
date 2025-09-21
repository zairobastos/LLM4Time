import os
import streamlit as st
from lib.crud import crud_history
from utils.paths import abspath

# LLM4Time
from llm4time.core.prompts import PromptType
from llm4time.visualization import plots


# ---------------- Dialog confirmação de exclusão ----------------

@st.dialog("Confirmar exclusão")
def confirmation_dialog(dataset: str, prompt_types: list):
  st.write(
      f"Tem certeza que deseja limpar o histórico do dataset **{dataset}** para os prompts abaixo?")
  st.markdown("\n".join(f"- **{prompt_type}**" for prompt_type in prompt_types))
  st.caption("**⚠️ Esta ação não poderá ser desfeita.**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Cancelar", use_container_width=True):
      st.rerun()
  with col2:
    if st.button("Limpar", use_container_width=True, type="primary"):
      try:
        crud_history().remove_many(dataset, prompt_types)
        st.rerun()
      except Exception as e:
        st.toast(f"Erro ao limpar o histórico: {str(e)}", icon="⚠️")

# ---------------- Sidebar ----------------


with st.sidebar:
  st.write(" ### 🔍 Parâmetros da Busca")

  datasets = os.listdir(abspath('uploads'))
  dataset = st.selectbox('Base de Dados', datasets)

  prompt_types = st.multiselect(
      label='Tipo de Prompt',
      options=[f.name for f in PromptType],
      default=[PromptType.ZERO_SHOT.name],
      help="Selecione os tipos de prompts que deseja visualizar. Você pode selecionar mais de um tipo de prompt para comparar os resultados.")

  confirm_view_history = st.button(
      label="Visualizar Previsões",
      help="Clique para visualizar o histórico de previsões dos prompts selecionados.",
      type="primary",
      use_container_width=True)

  confirm_clear_history = st.button(
      label="Limpar Histórico",
      help="Clique para limpar o histórico de previsões dos prompts selecionados.",
      use_container_width=True
  )

# ---------------- Validações ----------------

if confirm_view_history and prompt_types == []:
  st.warning(
      "Por favor, selecione pelo menos um tipo de prompt para visualizar as previsões.")

elif confirm_clear_history and prompt_types == []:
  st.warning(
      "Por favor, selecione pelo menos um tipo de prompt para limpar o histórico.")

# ---------------- Ações ----------------

elif confirm_clear_history:
  confirmation_dialog(dataset, prompt_types)

elif confirm_view_history:
  results = crud_history().select(dataset=dataset, prompt_types=prompt_types)
  for i, result in enumerate(results[::-1]):
    y_val = list(map(float, result[13].strip('[]').split(',')))
    y_pred = eval(result[14])

    st.write(f"### 📊 {result[1]} - {result[8]}".upper())
    st.plotly_chart(
        plots.plot_forecast(
            title=f"{result[3]} / {result[1]} / SMAPE = {result[15]}",
            y_val=y_val,
            y_pred=y_pred
        ),
        use_container_width=True,
        key=f"forecast_{i}"
    )

    st.markdown(
        """
      <style>
        .full-width-table {
          width: 100%;
          border-collapse: collapse;
        }
        .full-width-table th, .full-width-table td {
          padding: 8px;
          text-align: left;
          font-size: 18px;
        }
        .full-width-table th {
          text-align: center;
          background-color: #333;
          color: #fff;
        }
        .centered {
          text-align: center;
          background-color: #333;
          color: #fff;
          font-weight: bold;
        }
        .full-width-table tr:nth-child(even) {
          background-color: #444;
        }
        .full-width-table tr:nth-child(odd) {
          background-color: #666;
        }
        .full-width-table td {
          color: #fff;
          font-weight: bold;
        }
      </style>
      """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
      <table class="full-width-table">
        <tbody>
          <tr>
            <th colspan="3" class="centered">PARÂMETROS DO MODELO</th>
          </tr>
          <tr>
            <td>Modelo</td>
            <td colspan="2">{result[1]}</td>
          </tr>
          <tr>
            <td>Temperatura</td>
            <td colspan="2">{result[2]}</td>
          </tr>
          <tr>
            <th colspan="3" class="centered">PARÂMETROS DO PROMPT</th>
          </tr>
          <tr>
            <td>Base de dados</td>
            <td colspan="2">{result[3]}</td>
          </tr>
          <tr>
            <td>Data de início</td>
            <td colspan="2">{result[4]}</td>
          </tr>
          <tr>
            <td>Data de término</td>
            <td colspan="2">{result[5]}</td>
          </tr>
          <tr>
            <td>Períodos</td>
            <td colspan="2">{result[6]}</td>
          </tr>
          <tr>
            <td>Tipo do prompt</td>
            <td colspan="2">{result[8]}</td>
          </tr>
          <tr>
            <td>Quantidade de exemplos</td>
            <td colspan="2">{result[9]}</td>
          </tr>
          <tr>
            <td>Estratégia de amostragem</td>
            <td colspan="2">{result[10]}</td>
          </tr>
          <tr>
            <td>Formato</td>
            <td colspan="2">{result[11]}</td>
          </tr>
          <tr>
            <td>Tipo de série</td>
            <td colspan="2">{result[12]}</td>
          </tr>
          <tr>
            <th colspan="3" class="centered">RESPOSTA DO MODELO</th>
          </tr>
          <tr>
            <td>Quantidade de tokens do prompt</td>
            <td colspan="2">{result[18]}</td>
          </tr>
          <tr>
            <td>Quantidade de tokens da resposta</td>
            <td colspan="2">{result[19]}</td>
          </tr>
          <tr>
            <td>Total de tokens</td>
            <td colspan="2">{result[20]}</td>
          </tr>
          <tr>
            <td>Tempo de resposta (segundos)</td>
            <td colspan="2">{result[21]}</td>
          </tr>
          <tr>
            <td>Valores exatos</td>
            <td colspan="2">{result[13]}</td>
          </tr>
          <tr>
            <td>Valores previstos</td>
            <td colspan="2">{result[14]}</td>
          </tr>
          <tr>
            <th colspan="3" class="centered">MÉTRICAS</th>
          </tr>
          <tr>
            <td>sMAPE</td>
            <td colspan="2">{result[15]}</td>
          </tr>
          <tr>
            <td>MAE</td>
            <td colspan="2">{result[16]}</td>
          </tr>
          <tr>
            <td>RMSE</td>
            <td colspan="2">{result[17]}</td>
          </tr>
          <tr>
            <th colspan="3" class="centered">ESTATÍSTICAS</th>
          </tr>
          <tr>
            <th>Métrica</th>
            <th>Valores Reais</th>
            <th>Valores Previstos</th>
          </tr>
          <tr>
            <td>Média</td>
            <td align="center">{result[22]}</td>
            <td align="center">{result[23]}</td>
          </tr>
          <tr>
            <td>Mediana</td>
            <td align="center">{result[24]}</td>
            <td align="center">{result[25]}</td>
          </tr>
          <tr>
            <td>Desvio Padrão</td>
            <td align="center">{result[29]}</td>
            <td align="center">{result[27]}</td>
          </tr>
          <tr>
            <td>Valor Mínimo</td>
            <td align="center">{result[28]}</td>
            <td align="center">{result[29]}</td>
          </tr>
          <tr>
            <td>Valor Máximo</td>
            <td align="center">{result[30]}</td>
            <td align="center">{result[31]}</td>
          </tr>
        </tbody>
      </table>
    """,
        unsafe_allow_html=True)

    st.plotly_chart(
        plots.plot_forecast_statistics(
            title="Comparação Estatística",
            y_val=eval(result[13]),
            y_pred=eval(result[14])
        ),
        use_container_width=True,
        key=f"statistics_{i}"
    )

    st.write(f"### PROMPT - {result[8]}")
    st.code(result[7], language='python', line_numbers=True)
    st.write('---')
