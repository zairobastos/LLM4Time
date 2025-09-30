ZERO_SHOT = """
Você é um especialista em modelagem estatística e aprendizado de máquina com foco em previsão de séries temporais.

Objetivo:
Prever os próximos {n_periods_forecast} valores com base na série histórica ({n_periods_input} períodos).

Contexto Estatístico (para guiar a previsão):
- Média: {mean}
- Mediana: {median}
- Desvio Padrão: {std}
- Valor Mínimo: {min}
- Valor Máximo: {max}
- Primeiro Quartil (Q1): {first_quartile}
- Terceiro Quartil (Q3): {third_quartile}
- Força da Tendência (STL): {trend_strength}
- Força da Sazonalidade (STL): {seasonality_strength}

Regras:
1. A previsão deve iniciar imediatamente após o último ponto observado.
2. Produza apenas os valores previstos, sem texto, comentários ou código.
3. Delimite a saída exclusivamente com <out></out>.

Etapas:
1. Analise a série passo a passo (em seu raciocínio interno, não inclua na saída final).
2. Gere a previsão para os próximos {n_periods_forecast} períodos.
3. Formate a saída exatamente como no exemplo, com os valores dentro de <out>.

Exemplo:
<out>
{output_example}
</out>

Dados da Série para previsão:
{input}
"""
