# Fase2_Cap1_R

Estudo para analisar a necessidade de irrigação na cultura cafeira de São Paulo, realizado no âmbito do curso de Inteligência Artificial da FIAP.



**OBJETIVO & METODOLOGIA**

Este documento sintetiza a inteligência de dados aplicada à agricultura de precisão, integrando um modelo de balanço hídrico e agrometeorologia. Para adequado aprofundamento das análises, restringimos o estudo à cultura de café (Coffea arabica) na região de Franca, no estado de São Paulo. Ainda como marco temporal para análise dos dados, fixamos a data de início do plantio em 01/01/2020 e utilizamos dados até 31/12/2025. 

A escolha do município de Franca para esta análise justifica-se por sua posição estratégica como o coração da Região da Alta Mogiana, reconhecida globalmente pela excelência na produção de café arábica. A região apresenta condições edafoclimáticas singulares, com altitudes elevadas e solos do tipo Latossolo Vermelho, que possuem características físicas ideais para a retenção hídrica, mas que exigem um manejo de precisão devido à sazonalidade das chuvas. Além disso, a disponibilidade de dados históricos robustos pela estação meteorológica A708 (INMET) permite uma modelagem estatística fiel à realidade local, tornando Franca um laboratório ideal para a implementação de protocolos de irrigação voltados ao conforto hídrico e à alta produtividade. 

O embasamento técnico e a estruturação lógica deste estudo foram consolidados por meio de interações com a inteligência artificial generativa Gemini (Google, 2026), utilizada como ferramenta de suporte à decisão e engenharia de dados. Através de prompts estruturados, a ferramenta auxiliou na síntese de conceitos agrometeorológicos complexos, na automação de cálculos de balanço hídrico via linguagem Python, na organização de dataset fundamentados e na obtenção de fontes de dados confiáveis. Essa colaboração permitiu a integração eficiente entre o conhecimento científico tradicional e a agilidade do processamento de dados computacional.



**VARIÁVEIS**

Diferente dos modelos convencionais de sobrevivência, a metodologia proposta fundamenta-se na irrigação de conforto hídrico, cujo objetivo primordial é mitigar qualquer nível de estresse fisiológico para maximizar o potencial produtivo e a eficiência no enchimento de grãos. Para a construção do dataset e do modelo preditivo, foram selecionadas variáveis biofísicas e climatológicas essenciais, conforme descrito no Dicionário de Dados do projeto:

a.	Evapotranspiração de Referência (ET0): representa a demanda de perda de água do ecossistema baseada em dados atmosféricos (radiação, temperatura, vento e umidade). Os dados foram obtidos no CIIAGRO (2026) e foi escolhido o processamento pela metodologia Penman-Monteith, calculado na plataforma.

b.	Coeficiente da Cultura (Kc): fator de ajuste que correlaciona a ET0 com a demanda real do cafeeiro em diferentes estágios fenológicos (formação, florada, granagem e repouso). Dados obtidos por meio de código sugerido pela generativa Gemini (Google, 2026) para geração de data set que representasse a evolução da planta.

c.	Evapotranspiração da Cultura (ETC): é a lâmina de água consumida pela planta (mm/dia), conforme sua evolução e fase produtiva. É obtida a partir da multiplicação da Evapotranspiração de Referência (ET0) e o Coeficiente da Cultura (Kc). Na fase de formação, o consumo médio é mantido em patamares reduzidos (aproximadamente 2,7 mm/dia), dado o menor índice de área foliar. Com o amadurecimento do cafezal e a entrada na fase produtiva, o consumo torna-se sazonal e intensificado: durante os períodos de expansão dos frutos (janeiro a março), o consumo atinge seus picos (superando 5,4 mm/dia), exigindo máxima eficiência do sistema de irrigação. Já nos períodos de maturação e repouso vegetativo, o modelo reduz a oferta hídrica para induzir a uniformidade da colheita, demonstrando que o volume total de água manejado é diretamente proporcional à atividade metabólica da planta em cada época do ano.

d.	Capacidade de Água Disponível (CAD): volume de água que o solo de Franca consegue reter e disponibilizar para as raízes, variável progressiva de acordo com o desenvolvimento da planta, em decorrência da profundida atingida pelas raízes em suas diferentes fases.  Na fase de Formação (1º ano), o CAD foi fixado em 30 mm, refletindo raízes superficiais que exploram pouco volume de solo. Na fase adulta, o CAD expande-se para 75 mm, considerando a maturidade radicular que permite o acesso a reservas hídricas em camadas mais profundas. Esta variação impede subestimar o estresse em plantas jovens ou superestimar a necessidade de rega em plantas adultas, otimizando o recurso hídrico. Dados obtidos por meio de código sugerido pela generativa Gemini (Google, 2026) para geração de data set que representasse a evolução da planta.

e.	Fator de Disponibilidade (f): fração da água do solo que pode ser consumida antes que a planta sofra estresse. Neste estudo, otimizou-se o fator de disponibilidade. Enquanto o manejo tradicional de irrigação utiliza convencionalmente um valor fixo de 0,5 — permitindo que a planta consuma até 50% da reserva de água do solo antes da reposição — este estudo adaptou o índice para patamares de conforto hídrico. Nas fases de maior sensibilidade fisiológica, como a florada, o fator foi reduzido para 0,25, garantindo que a planta nunca atinja o ponto de estresse hídrico. Essa estratégia visa manter o estoma da planta aberto por mais tempo, maximizando a taxa fotossintética e, consequentemente, a produtividade final, evitando que a planta utilize energia para mecanismos de sobrevivência em detrimento da produção de biomassa e frutos.



**ANÁLISE**

A análise comparativa anual dos dois sistemas de irrigação utilizados no estudo revela uma discrepância acentuada entre o modelo de Estresse Hídrico e o modelo Otimizado, evidenciando como critérios de manejo mais rigorosos impactam o consumo de recursos. Observa-se no gráfico a seguir que o sistema Otimizado (azul) apresenta volumes de irrigação consistentemente superiores, atingindo picos de demanda nos anos de 2022 e 2023, o que se traduz em uma maior frequência de acionamento do sistema. Essa estratégia visa manter a planta em um estado de conforto hídrico permanente, resultando em um volume total acumulado significativamente maior em relação ao sistema de Estresse (laranja), que permite uma depleção mais profunda do estoque de água no solo antes de intervir.

A métrica de Diferença (cinza) destaca o custo de oportunidade hídrico entre os dois modelos, mostrando que a busca pelo rendimento máximo via sistema otimizado exige um aporte de água que chega a dobrar em determinados períodos. No entanto, é notável que, apesar do aumento no volume total, a eficiência de acionamento (quantidade de vezes irrigada) não cresce na mesma proporção linear, sugerindo que o sistema otimizado realiza irrigações mais volumosas para garantir a saturação do solo.

Aqui está o parágrafo focado na hipótese da bienalidade para complementar sua análise:

Como informado anteiormente, o dataset foi criado com o apoio de IA generativa e por isso há que se avaliar com cautela se os resultados são condizentes com a realidade. Em especial, destaca-se a variação observada no consumo hídrico entre os períodos de 2022/2023 e 2024/2025. Uma das possibilidades é que a IA tenha reprozido a característica bianual da cultura do café, característica da região da Alta Mogiana. Sob essa perspectiva, o biênio 2022/2023 teria representado o ciclo de "safra alta" (ano de carga), no qual a planta direciona seus recursos fisiológicos para a maturação dos frutos, elevando o coeficiente da cultura (Kc) e, consequentemente, a demanda por evapotranspiração. Em contrapartida, o ciclo 2024/2025 refletiria o período de "safra baixa" ou de recuperação vegetativa, onde a menor carga pendente e o estresse térmico acumulado resultam em uma atividade fisiológica mais contida. Essa alternância produtiva justifica por que, mesmo sendo plantas cronologicamente mais maduras, os espécimes de 2024/2025 apresentaram um consumo hídrico inferior ao biênio anterior no balanço simulado.



**FONTES**

CENTRO INTEGRADO DE INFORMAÇÕES AGROMETEOROLÓGICAS (CIIAGRO). Janela do Fruticultor: manejo para irrigação. Campinas: Instituto Agronômico (IAC), [s.d.]. Disponível em: http://www.ciiagro.org.br/janeladofruticultor/irrigacao.php. Acesso em: 18 abr. 2026.

GOOGLE GEMINI. [Código de programação Python para manejo de irrigação do café conforme estágio de desenvolvimento da planta]. Versão abr. 2026. São Paulo: Google, 2026. Disponível em: https://gemini.google.com/. Acesso em: 19 abr. 2026.

INSTITUTO NACIONAL DE METEOROLOGIA (Brasil). Banco de Dados Meteorológicos para Ensino e Pesquisa (BDMEP). Dados históricos de precipitação: estação Franca (A708). Brasília, DF: INMET, 2026. Disponível em: https://portal.inmet.gov.br/dadoshistoricos. Acesso em: 19 abr. 2026.

**FUNCIONALIDADES**

- Balanço Hídrico Diário: cálculo automático de estoque de água no solo baseado em precipitação e evapotranspiração.
- Comparação de Modelos: avaliação simultânea de dois gatilhos de irrigação diferentes (Estresse vs. Otimizado).
- Controlo de Fenologia: ajuste dinâmico do Coeficiente da Cultura (Kc) conforme o estágio de desenvolvimento da planta.
- Relatórios Consolidados:geração de tabelas detalhadas diárias, mensais e anuais, incluindo somatórios totais do período.
- Visualização de Dados: gráfico comparativo de barras e linhas que correlaciona o volume irrigado com a frequência de acionamento do sistema.

**PRÉ-REQUISITOS**

Para executar este script, necessita de ter o R (versão 4.0 ou superior) instalado. Recomendamos o uso do RStudio.

As seguintes bibliotecas devem ser instaladas:dplyr, lubridate, ggplot2 e tidyr.

**DATASET**

O script utiliza como entrada o ficheiro `Dataset - 2026.04.19 19h07.csv`. As principais colunas contém:
- Data: identificador temporal (suporta formato serial Excel).
- Estagio: fase fenológica (ex: Floração, Frutificação).
- Precipitacao: volume de chuva em mm.
- ET0: evapotranspiração de referência da região.
- KC: coeficiente da cultura para o estágio específico.
- CAD_Max: capacidade de Água Disponível máxima do solo.

**AUTORES**

GRUPO 50
Heitor Exposito de Souza / rm566013  
Marco Antônio Rodrigues Siqueira / rm569975
Nádia Nakamura Vieira / rm568906
Rafael Bassami / rm569930
Vinícius Xavier da Silva / rm572108
