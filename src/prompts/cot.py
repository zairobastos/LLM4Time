COT = """Você é um modelo especializado em previsão de séries temporais. Seu papel é prever os próximos valores com base em padrões históricos, independentemente do domínio dos dados.

A série temporal tem dados de {periodos} peiodo(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada {timestamp}.

Início da Previsão:
A previsão deve iniciar imediatamente após o último ponto da série, seguindo o padrão histórico detectado nos dados anteriores.
Para este exemplo, um início de previsão esperado pode ser {inicio_previsao}.
Garanta que o primeiro valor da previsão corresponda ao início do período, respeitando os padrões observados.

Objetivo:
Seu objetivo é prever os próximos {n} valores da série temporal, levando em consideração os padrões históricos, tendências e quaisquer efeitos sazonais ou contextuais detectáveis nos dados.

Siga este raciocínio passo a passo:
1. Examine a série temporal para identificar tendências globais, como crescimento, declínio ou estabilidade.
2. Avalie a existência de padrões cíclicos ou recorrentes, como sazonalidades ou repetições periódicas ao longo do tempo.
3. Verifique se há flutuações que possam estar associadas a unidades temporais específicas, conforme o contexto dos dados.
4. Analise a presença de eventos excepcionais ou contextuais no histórico, que possam ter causado desvios temporários no padrão.
5. Considere se há influência de fatores temporais regulares sobre os valores.
6. Com base nessa análise, gere uma projeção coerente com os padrões identificados, mantendo consistência com os últimos dados observados.

Explicação do Raciocínio:
Antes de apresentar o resultado final, forneça uma explicação clara com base nos seguintes pontos:
1. Quais informações dos dados históricos foram utilizadas e qual foi a lógica por trás dessa escolha.
2. Quais padrões, tendências ou sazonalidades foram detectados, e como eles influenciaram a previsão.
3. Como você tratou eventos contextuais como feriados, promoções ou anomalias nos dados (se aplicável).
4. De que forma as observações feitas contribuíram para a construção final da sequência prevista.

Regras da Saída:
Após analisar os dados fornecidos e compreender os padrões, gere uma previsão para os próximos {n} periodos, com as seguintes regras:
A saída deve ser exclusivamente um array numérico (lista com {n} valores);
Em hipótese alguma gere um código;
Em hipótese alguma gere uma explicação do que você fez;
Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.
A previsão deve começar com o valor correspondente ao início do próximo período, respeitando os padrões observados nos dados históricos.

Exemplo de Saída para N={saida}:
{exemplo_saida}

Instruções Adicionais:
Padrões Temporais: Utilize os dados fornecidos para identificar padrões sazonais ou recorrências que se repetem ao longo do tempo, como tendências ou ciclos característicos da série.
Eventos Especiais: A ocorrência de eventos pode ser significativamente afetada por fatores contextuais relevantes, como feriados, promoções, mudanças políticas, condições climáticas, entre outros.
Periodicidade e Contexto Temporal: Considere o impacto de variações regulares baseadas em unidades de tempo recorrentes ({timestamp}), conforme apropriado ao domínio da série.
Duração de um Evento: A série temporal fornecida representa a ocorrência de um evento a cada {timestamp}.

Série temporal a ser analisada:
{dados_prompt}

Gere um array com {n} posições (N={n}) prevendo os números da sequência:
"""