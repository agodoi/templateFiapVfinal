import os
from pathlib import Path

import streamlit as st
import pandas as pd
import oracledb
import plotly.express as px
from dotenv import load_dotenv

# --- Configuração ---
load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env")

ORACLE_USER = os.environ["ORACLE_USER"].lower()
ORACLE_PASSWORD = os.environ["ORACLE_PASSWORD"].lower()
ORACLE_DSN = os.environ["ORACLE_DSN"]

st.set_page_config(layout="wide", page_title="Dashboard Agrícola")

@st.cache_data
def get_data_from_oracle():
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
    query = """
        SELECT 
            c.NOME AS NOME_CLIENTE, f.LOCALIZACAO AS NOME_FAZENDA,
            f.ESTADO, f.CULTURA, s.DATA_LEITURA, 
            s.N_STATUS, s.P_STATUS, s.K_STATUS, 
            s.BOMBA_STATUS, s.UMIDADE_VALOR
        FROM SENSORES s
        JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
        JOIN CLIENTES c ON f.ID_CLIENTE = c.ID_CLIENTE
        ORDER BY f.LOCALIZACAO, s.DATA_LEITURA
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    df['DATA_LEITURA'] = pd.to_datetime(df['DATA_LEITURA'])
    df['UMIDADE_VALOR'] = pd.to_numeric(df['UMIDADE_VALOR'].astype(str).str.replace(',', '.'), errors='coerce')
    df['ANO'] = df['DATA_LEITURA'].dt.year
    df['MES'] = df['DATA_LEITURA'].dt.month
    df['MES_ANO'] = df['DATA_LEITURA'].dt.to_period('M').astype(str)
    
    for col in ['N_STATUS', 'P_STATUS', 'K_STATUS']:
        df[f'{col}_REPOSICAO'] = (df.groupby('NOME_FAZENDA')[col].diff().fillna(0) == 1).astype(int)
        
    return df

df = get_data_from_oracle()

st.title("Dashboard de Gestão Agrícola")

# --- Filtros (Cascata) ---
st.sidebar.header("Filtros")
estado_sel = st.sidebar.multiselect("Filtrar por Estado", df['ESTADO'].unique())
cultura_sel = st.sidebar.multiselect("Filtrar por Cultura", df['CULTURA'].unique())

df_base = df.copy()
if estado_sel: df_base = df_base[df_base['ESTADO'].isin(estado_sel)]
if cultura_sel: df_base = df_base[df_base['CULTURA'].isin(cultura_sel)]

clientes_sel = st.sidebar.multiselect("Selecione o(s) Cliente(s)", df_base['NOME_CLIENTE'].unique())
fazendas_disp = df_base[df_base['NOME_CLIENTE'].isin(clientes_sel)]['NOME_FAZENDA'].unique() if clientes_sel else df_base['NOME_FAZENDA'].unique()
fazendas_sel = st.sidebar.multiselect("Selecione a(s) Fazenda(s)", fazendas_disp)

df_filt = df_base.copy()
if clientes_sel: df_filt = df_filt[df_filt['NOME_CLIENTE'].isin(clientes_sel)]
if fazendas_sel: df_filt = df_filt[df_filt['NOME_FAZENDA'].isin(fazendas_sel)]

# --- Visualização ---
if df_filt.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    # 1. Irrigação
    st.subheader("Total de Irrigação (Mensal)")
    df_irrig = df_filt[df_filt['BOMBA_STATUS'] == 'LIGADA'].groupby('MES_ANO').size().reset_index(name='Total_Ligacoes')
    fig_irrig = px.bar(df_irrig, x='MES_ANO', y='Total_Ligacoes', height=400, title="Vezes Ligada por Mês")
    st.plotly_chart(fig_irrig, use_container_width=True)

    # 2. Nutrientes
    st.subheader("Ocorrências de Reposição de Nutrientes (N, P, K)")
    df_nutri_rep = df_filt.groupby('MES_ANO')[['N_STATUS_REPOSICAO', 'P_STATUS_REPOSICAO', 'K_STATUS_REPOSICAO']].sum().reset_index()
    df_nutri_melt = df_nutri_rep.melt(id_vars=['MES_ANO'], value_vars=['N_STATUS_REPOSICAO', 'P_STATUS_REPOSICAO', 'K_STATUS_REPOSICAO'])
    fig_nutri = px.bar(df_nutri_melt, x='MES_ANO', y='value', color='variable', barmode='stack', height=400)
    st.plotly_chart(fig_nutri, use_container_width=True)

    # 3. Projeção de Umidade (Zoom Dinâmico)
    st.subheader("Projeção de Umidade para 2026 (Baseada no Histórico)")
    df_filt['Categoria'] = df_filt['ESTADO'] + " | " + df_filt['CULTURA']
    df_hist = df_filt[df_filt['ANO'] < 2026]
    df_proj = df_hist.groupby(['MES', 'Categoria'])['UMIDADE_VALOR'].mean().reset_index()
    df_proj['Data_Proj'] = df_proj['MES'].apply(lambda m: f"2026-{m:02d}")
    
    fig_proj = px.line(df_proj, x='Data_Proj', y='UMIDADE_VALOR', color='Categoria', 
                       title="Tendência de Umidade 2026", markers=True)
    
    # Cálculo dinâmico do Range para zoom ideal
    min_val = df_proj['UMIDADE_VALOR'].min()
    max_val = df_proj['UMIDADE_VALOR'].max()
    margem = (max_val - min_val) * 0.1 # 10% de margem
    fig_proj.update_yaxes(range=[min_val - margem, max_val + margem])
    
    fig_proj.add_hline(y=45, line_dash="dash", line_color="green", annotation_text="Mínimo Café (45%)")
    fig_proj.add_hline(y=55, line_dash="dot", line_color="orange", annotation_text="Mínimo Soja (55%)")
    st.plotly_chart(fig_proj, use_container_width=True)