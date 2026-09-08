# Fase 3 - Cap 1 - Etapas de uma Máquina Agrícola 🌿

## Identificação

**Fase:** 3
**Capítulo:** 1
**Grupo:** H.M.N.R.V.

---

## Descrição da Atividade

Integração das entregas da Fase 3 - Capítulo 1 com foco em banco de dados Oracle (carga e validação de dados IoT), visualização interativa em dashboard para apoio à gestão de fazendas, e exploração e modelagem de Machine Learning para culturas agrícolas.

## Módulos da Solução

- **Oracle (Banco de Dados):** simulação e carga de dados históricos, validação via consultas SQL.
- **Dashboard:** visualização interativa com indicadores de irrigação, nutrientes e umidade.
- **Machine Learning:** análise exploratória e modelagem preditiva para culturas agrícolas.

## Tecnologias

- Python 3.12+
- pandas, numpy, scikit-learn
- Streamlit, Plotly
- Oracle Database (oracledb, SQL Developer)

## Arquivos e Ativos

**Oracle**
- `scripts/Sensores_Dataset.py` - simulação e geração de datasets.
- `scripts/irrigacao.ino` - base da lógica de sensores da Fase 2.
- `sql/consultas_oracle.sql` - consultas SQL de validação.
- `evidenciais/Fase3_Cap1_BancoOracle_Documentacao_Passos.pdf` - documentação do processo.

**Dashboard**
- `scripts/Dashboard.py` - aplicação Streamlit.

**Machine Learning**
- `ViniciusXavier_RM572108_fase3_cap1.ipynb` - notebook com análises e modelos.

**Datasets**
- `datasets/sensores_v8_final.csv`
- `datasets/clientes_v7.csv`
- `datasets/fazendas_v8_final.csv`
- `datasets/cultivo_v7.csv`

## Execução

**Oracle (simulação e carga)**
1. Gere os dados: `python Sensores_Dataset.py`.
2. Importe os CSVs no Oracle SQL Developer com:
   - Delimitador: `;`
   - Separador decimal: `,`
   - Formato de data: `YYYY-MM-DD`
3. Valide as cargas com as consultas de `sql/consultas_oracle.sql`.

**Dashboard**
1. Instale dependências:
   ```bash
   pip install streamlit pandas oracledb plotly python-dotenv
   ```
2. Crie `.env` na raiz do projeto *(um arquivo `.env.example` está disponível no repositório como modelo)*:
   ```env
   ORACLE_USER=seu_usuario
   ORACLE_PASSWORD=sua_senha
   ORACLE_DSN=host:porta/servico
   ```
3. Execute:
   ```bash
   streamlit run src/fase_3/cap_1/scripts/Dashboard.py
   ```

**Machine Learning**
1. Abra o notebook `ViniciusXavier_RM572108_fase3_cap1.ipynb`.
2. Execute as células para gerar gráficos, perfis por cultura e modelos.

## Dashboard

- **Total de irrigação (mensal):** barras com frequência de acionamento da bomba.
- **Reposição de nutrientes (N, P, K):** barras empilhadas por mês.
- **Projeção de umidade 2026:** linhas com referências mínimas por cultura.
- **Filtros em cascata:** Estado -> Cultura -> Cliente -> Fazenda.

## Resultados e Análises

**Culturas analisadas (ML)**

| Cultura | Destaques no perfil |
|---|---|
| Milho | N elevado, K baixo, temperaturas amenas |
| Algodão | Maior teor de N da base (117,77), precipitação moderada |
| Banana | Alto P (82) e N (100), temperatura elevada, pH levemente ácido |

**Modelos e acurácia**

| Modelo | Acurácia |
|---|---|
| Naive Bayes | 1,000 |
| Extra Trees | 0,995 |
| Gradient Boosting | 0,991 |
| MLP (Rede Neural) | 0,989 |
| LDA | 0,977 |

## Equipe

- Heitor Exposito de Sousa - RM 566013
- Marco Antônio Rodrigues Siqueira - RM 569975
- Nádia Nakamura Vieira - RM 568906
- Rafael Bassani - RM 569930
- Vinicius Xavier da Silva - RM 572108

## Vídeos Demonstrativos

- **Oracle:** https://youtu.be/0ck84D-usvI
- **Dashboard:** https://youtu.be/Xqunrf7JC_4
- **Machine Learning:** https://youtu.be/hyinBzCXlk8
