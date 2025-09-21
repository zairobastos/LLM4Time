ZERO_SHOT = """
Você é um modelo especializado em previsão de séries temporais. Seu papel é prever os próximos valores com base em padrões históricos, independentemente do domínio dos dados.

A série temporal tem dados de {n_periods_input} período(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada {freq}.

Início da Previsão:
A previsão deve iniciar imediatamente após o último ponto da série, seguindo o padrão histórico detectado nos dados anteriores.
Para este exemplo, um início de previsão esperado pode ser:
{input_example}
Garanta que o primeiro valor da previsão corresponda ao início do período, respeitando os padrões observados.

Objetivo:
Seu objetivo é prever os próximos {n_periods_forecast} valores da série temporal, levando em consideração os padrões históricos, tendências e quaisquer efeitos sazonais ou contextuais detectáveis nos dados.

Regras da Saída:
Após analisar os dados fornecidos e compreender os padrões, gere uma previsão para os próximos {n_periods_forecast} períodos, com as seguintes regras:
A saída deve ser exclusivamente um array numérico (lista com {n_periods_forecast} valores);
Em hipótese alguma gere um código;
Em hipótese alguma gere uma explicação do que você fez;
Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.
A previsão deve começar com o valor correspondente ao início do próximo período, respeitando os padrões observados nos dados históricos.

Exemplo de Saída para N={n_periods_example}:
{output_example}

Instruções Adicionais:
Padrões Temporais: Utilize os dados fornecidos para identificar padrões sazonais ou recorrências que se repetem ao longo do tempo, como tendências ou ciclos característicos da série.
Eventos Especiais: A ocorrência de eventos pode ser significativamente afetada por fatores contextuais relevantes, como feriados, promoções, mudanças políticas, condições climáticas, entre outros.
Periodicidade e Contexto Temporal: Considere o impacto de variações regulares baseadas em unidades de tempo recorrentes ({freq}), conforme apropriado ao domínio da série.
Duração de um Evento: A série temporal fornecida representa a ocorrência de um evento a cada {freq}.

Série temporal a ser analisada:
{input}

Gere um array com {n_periods_forecast} observações (N={n_periods_forecast}) prevendo os números da sequência:
"""
