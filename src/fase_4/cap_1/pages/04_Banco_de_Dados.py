"""
Página de integração com o banco de dados Oracle.

Fornece operações de teste de conexão, criação de tabela e upload do CSV
para a tabela `CS_SENSORES_IOT`. Apresenta também contadores e previews
de tabelas relevantes.
"""

import streamlit as st
from src.config import get_oracle_config
from src import load_csv
from src.database import (
    get_connection,
    test_connection,
    list_tables,
    load_clima,
    load_fazendas,
    load_sensores_iot,
    create_sensores_iot_table,
    insert_sensores_iot_from_dataframe,
    detect_fazenda_pk,
)
from src.ui import render_section_divider, render_info_card, render_metric_card

st.set_page_config(page_title='Banco de Dados', layout='wide')
st.title('04 - Banco de Dados (Oracle)')

st.write('Status da configuração de ambiente:')
oracle_cfg = get_oracle_config()
connected = False
try:
    connected = test_connection()
except Exception:
    connected = False

if connected:
    st.success('Conexão Oracle: 🟢 Conectado')
else:
    st.error('Conexão Oracle: 🔴 Desconectado')

if not oracle_cfg.is_configured:
    st.error('Variáveis de ambiente Oracle não configuradas. Veja `.env.example`.')
    st.stop()

if st.button('Testar conexão Oracle'):
    ok = test_connection()
    if ok:
        st.success('Conexão Oracle OK')
    else:
        st.error('Falha na conexão Oracle. Verifique .env e a rede (DSN).')

if st.button('Listar tabelas'):
    try:
        conn = get_connection()
        tables = list_tables(conn)
        st.write(tables)
        conn.close()
    except Exception as e:
        st.error(f'Erro ao listar tabelas: {e}')

render_section_divider('Status e Contadores')
try:
    conn = get_connection()
    tables = list_tables(conn)
    num_tables = len(tables) if tables else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card('Número de tabelas', num_tables)
    # Counts for specific tables
    try:
        dfc = load_clima(conn)
        c2 = dfc.shape[0] if dfc is not None else 0
    except Exception:
        c2 = 0
    try:
        dff = load_fazendas(conn)
        c3 = dff.shape[0] if dff is not None else 0
    except Exception:
        c3 = 0
    try:
        # Prefer view VW_DADOS_AGRICOLAS_ML when available
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM VW_DADOS_AGRICOLAS_ML")
            c4 = cur.fetchone()[0]
            cur.close()
        except Exception:
            dfs = load_sensores_iot(conn, n=1)
            c4 = dfs.shape[0] if dfs is not None else 0
    except Exception:
        c4 = 0
    # show counters
    st.metric('Registros CS_CLIMA', c2)
    st.metric('Registros CS_FAZENDAS', c3)
    st.metric('Registros CS_SENSORES_IOT (mostra)', c4)
    conn.close()
except Exception as e:
    st.info('Não foi possível conectar para obter contadores.')

render_section_divider('Integração de Dados')
st.write('Fluxo: CSV → Oracle. A tabela `CS_SENSORES_IOT` consolida leituras de sensores IoT para análises e relatórios.')

if st.button('Criar tabela CS_SENSORES_IOT'):
    try:
        conn = get_connection()
        create_sensores_iot_table(conn)
        conn.close()
        st.success('Tabela criada (ou já existia).')
    except Exception as e:
        st.error(f'Erro ao criar: {e}')

force_insert = st.checkbox('Forçar inserção mesmo se já existirem registros (não recomendado)')
if st.button('Popular CS_SENSORES_IOT com CSV'):
    try:
        df = load_csv()
        conn = get_connection()
        inserted = insert_sensores_iot_from_dataframe(conn, df, allow_if_exists=force_insert)
        conn.close()
        if inserted == 0:
            st.info('Tabela já possui dados. Nenhum registro inserido. Marque Forçar inserção para sobrescrever.')
        else:
            st.success(f'{inserted} registros inseridos em CS_SENSORES_IOT')
    except Exception as e:
        st.error(f'Erro ao inserir: {e}')

render_section_divider('Preview de tabelas relevantes')
try:
    conn = get_connection()
    st.subheader('CS_CLIMA (amostra)')
    try:
        dfc = load_clima(conn)
        st.dataframe(dfc)
    except Exception:
        st.info('Não foi possível carregar CS_CLIMA ou tabela vazia')

    st.subheader('CS_FAZENDAS (amostra)')
    try:
        dff = load_fazendas(conn)
        st.dataframe(dff)
    except Exception:
        st.info('Não foi possível carregar CS_FAZENDAS ou tabela vazia')

    st.subheader('CS_SENSORES_IOT (amostra)')
    try:
        # prefer view
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM VW_DADOS_AGRICOLAS_ML WHERE ROWNUM <= 200')
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            import pandas as _pd
            dfv = _pd.DataFrame(rows, columns=cols)
            if dfv.empty:
                st.info('VW_DADOS_AGRICOLAS_ML está vazia ou não existe')
            else:
                st.dataframe(dfv)
            cur.close()
        except Exception:
            dfs = load_sensores_iot(conn, n=50)
            if dfs.empty:
                st.info('CS_SENSORES_IOT não existe ou está vazia')
            else:
                st.dataframe(dfs)
    except Exception:
        st.info('Não foi possível carregar CS_SENSORES_IOT')
    conn.close()
except Exception as e:
    st.error(f'Erro ao mostrar previews: {e}')
