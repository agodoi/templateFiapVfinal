Análise de Dados do Agronegócio

Identificação

Nome: Rafael Bassani
RM: XXXXX
Fase: 2
Capítulo: 7

---

Objetivo do Trabalho

O objetivo deste trabalho foi coletar dados reais do agronegócio a partir de fontes públicas e realizar uma análise exploratória utilizando a linguagem R.

Foram utilizados dados da CONAB (Companhia Nacional de Abastecimento), com foco em diferentes culturas agrícolas ao longo dos anos.

---

Fonte dos Dados

Os dados foram obtidos a partir da CONAB, que disponibiliza relatórios de balanço de oferta e demanda de diversas commodities agrícolas.
'https://www.gov.br/conab/pt-br/atuacao/informacoes-agropecuarias/safras/safra-de-graos/boletim-da-safra-de-graos/6o-levantamento-safra-2025-26/site_previsao_de_safra-por_produto-mar-2026.xlsx'

A base utilizada contempla informações como:

Produção
Consumo
Estoque
Importação e exportação

Para o trabalho, foram selecionadas as seguintes culturas:

Algodão
Arroz
Feijão
Milho
Trigo

---

Construção da Base de Dados

A base foi estruturada manualmente no Excel, contendo **30 linhas e 7 colunas**, organizadas da seguinte forma:

ID → identificador da linha
Produto → tipo de cultura *(variável qualitativa nominal)*
Safra → período da produção
Ano → *(variável quantitativa discreta)*
Producao_mil_ton → *(variável quantitativa contínua)*
Consumo_mil_ton → *(variável quantitativa contínua)*
Nivel_Producao → *(variável qualitativa ordinal: Baixa, Média, Alta)*

A variável **Nivel_Producao** foi criada com base nos valores de produção, classificando os dados em níveis para facilitar a análise.

---

Importação dos Dados no R

Foi utilizado o pacote 'readxl' para leitura do arquivo Excel:

```r
if (!"readxl" %in% installed.packages()) {
  install.packages("readxl")
}
library(readxl)

dados <- read_excel("caminho_do_arquivo.xlsx")
```

Após a importação, foram realizadas validações com:

```r
str(dados)
summary(dados)
nrow(dados)
```

---

Análise da Variável Quantitativa

A variável escolhida para análise foi:

Producao_mil_ton

Medidas de Tendência Central

 Média
 Mediana
 Moda

Medidas de Dispersão

 Mínimo
 Máximo
 Amplitude
 Variância
 Desvio padrão

Medidas Separatrizes

 Quartis
 Percentis

---

Análise Gráfica

Histograma

O histograma mostrou que os dados possuem **assimetria à direita**, com concentração de valores menores e alguns valores muito altos.

Boxplot

O boxplot evidenciou a presença de **outliers**, principalmente relacionados ao milho, que apresenta produção muito superior às demais culturas.

---

Análise da Variável Qualitativa

Foram utilizados gráficos de barras para análise das variáveis qualitativas:

Frequência por Produto

Mostra a distribuição das culturas na base, garantindo equilíbrio dos dados.

Frequência por Nível de Produção

Mostra a predominância de produções classificadas como **Média**, indicando concentração em valores intermediários.

---

Análise Complementar (Diferencial)

Como complemento, foi realizada uma análise por cultura ao longo do tempo.

Foi criado um gráfico para cada produto contendo:

 Produção por ano
 Linha da média
 Linhas de média + desvio padrão
 Linhas de média - desvio padrão

Esse tipo de análise permite identificar:

 Tendências de crescimento ou queda
 Estabilidade da produção
 Variações fora do padrão

### 🔍 Principais observações

Milho → maior volume de produção e maior variabilidade
Feijão → comportamento mais estável
Algodão → tendência de crescimento
Trigo → crescimento inicial seguido de estabilização

---

Conclusão

A análise permitiu identificar padrões relevantes na produção agrícola brasileira, destacando diferenças importantes entre as culturas.

Além da análise estatística básica, a análise por cultura trouxe uma visão mais aprofundada sobre o comportamento dos dados ao longo do tempo, agregando valor ao trabalho.

---

Considerações Finais

O uso de dados reais contribuiu para tornar a análise mais próxima de um cenário real.

A utilização do R facilitou a exploração dos dados e a geração de gráficos que ajudam na interpretação dos resultados.
