# Fase 2 - Cap 6 - Python e além

## Identificação

**Fase:** 2
**Capítulo:** 6
**Grupo:** H.M.N.R.V.

---

## Descrição da Atividade

Sistema de gestão agrícola com Python avançado utilizando:

- **POO com dataclasses** - Modelagem de dados com classes `Cultura`, `Insumos`, `Financeiro`, `FarmData`
- **Estruturas de dados** - Listas, dicionários, tuples
- **Manipulação de arquivos** - CSV e JSON (leitura e exportação)
- **Conexão com banco de dados** - Oracle Database
- **Integração com R** - Execução de scripts R para estatísticas e API meteorológica

## Tema do Agronegócio

**Cana-de-açúcar** - O Brasil é líder mundial na produção de cana-de-açúcar, com safras recordes anualmente. O projeto contempla a gestão completa desde o plantio até a colheita, incluindo controle de perdas e análise de produtividade.

## Arquivos

- `menu_principal.py` - Sistema principal com menu CRUD completo e interface terminal estilizada
- `conectar_bd.py` - Conexão com banco de dados Oracle
- `inserir_dados.py` - Inserção de dados no Oracle
- `dados_cana.json` - Arquivo de configuração JSON para cultura de cana-de-açúcar

## Funcionalidades

- **Dados de Plantio** - Cadastro e cálculo de área (retângulo para café, círculo para soja)
- **Gestão de Insumos** - Cálculo de adubo, água, fosfato, herbicida, pesticida e fertilizante
- **Financeiro** - Cálculo de produtividade, receita, lucro e gastos por método de aplicação
- **Análise de Qualidade** - Classificação de grãos (café) e umidade do solo (soja)
- **Exportação** - CSV e JSON com dados de plantio
- **Estatísticas (R)** - Execução de script R para análise estatística
- **Meteorologia (R)** - Consulta de previsão do tempo via API
- **Banco de Dados** - Persistência no Oracle

## Tecnologias

- Python 3.10+
- Oracle Database (oracledb)
- pandas
- R (para estatísticas e API meteorológica)

## Execução

```bash
pip install -r requirements.txt
python menu_principal.py
```

## Requisitos Oracle

- Banco de dados Oracle disponível em `oracle.fiap.com.br:1521/ORCL`
- Credenciais configuradas em `conectar_bd.py`
