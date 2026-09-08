"""
Página de Exploração de Dados (EDA).

Contém visuais interativos (histogramas, boxplots, heatmap) e um bloco
simples de insights automáticos gerados a partir das estatísticas.
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_csv
from src.preprocessing import derive_volume_irrigacao
import plotly.express as px
from src.ui import render_section_divider, render_metric_card

st.set_page_config(page_title='Exploração de Dados', layout='wide')
st.title('01 - Exploração de Dados')

df = load_csv()
if df is None or df.empty:
    st.warning('Dados não disponíveis. Verifique `data/sensores_data.csv`.')
    st.stop()

# Top KPIs
cols = st.columns(4)
with cols[0]:
    render_metric_card('Total de registros', df.shape[0])
with cols[1]:
    render_metric_card('Temperatura média (°C)', round(df.temperatura.mean(), 2))
with cols[2]:
    render_metric_card('Umidade média (%)', round(df.umidade_solo.mean(), 2))
with cols[3]:
    render_metric_card('Nutrientes N (média)', round(df.nutrientes_N.mean(), 2))

render_section_divider('Dataframe (amostra)')
st.dataframe(df.head(20))

render_section_divider('Estatísticas Descritivas')
st.write(df.describe())

render_section_divider('Heatmap de Correlação')
corr = df.select_dtypes('number').corr()
figc = px.imshow(corr, color_continuous_scale='Viridis', text_auto=True)
st.plotly_chart(figc, width=800)

render_section_divider('Distribuições & Boxplots')
for col in ['temperatura', 'umidade_solo', 'nutrientes_N']:
    c1, c2 = st.columns([1, 1])
    with c1:
        fig = px.histogram(df, x=col, nbins=30, title=f'Distribuição: {col}', color_discrete_sequence=['#2b7a4a'], text_auto=True)
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        st.plotly_chart(fig, width=600)
    with c2:
        fig2 = px.box(df, y=col, title=f'Boxplot: {col}', color_discrete_sequence=['#13505a'])
        st.plotly_chart(fig2, width=400)

render_section_divider('Volume Irrigação Estimado')
df2 = derive_volume_irrigacao(df)
fig2 = px.scatter(df2, x='umidade_solo', y='volume_irrigacao_estimado', title='Umidade vs Volume Estimado', color_discrete_map={
        '0': '#2a6f97',  # O mesmo verde do seu histograma
        '1': '#d9a05b'       # Um azul padrão mais forte e visível
    })
st.plotly_chart(fig2, width=800)

render_section_divider('Insights Rápidos')
ins = []
tmin, tmax = df.temperatura.min(), df.temperatura.max()
ins.append(f'Temperaturas entre {tmin:.1f}°C e {tmax:.1f}°C.')
hum_med = df.umidade_solo.median()
ins.append(f'A mediana da umidade do solo é {hum_med:.1f}% — verificar necessidades de irrigação quando abaixo de 50%.')
if abs(corr.loc['temperatura','umidade_solo']) > 0.3:
    ins.append('Existe correlação notável entre temperatura e umidade do solo.')
for i in ins:
    st.write('- ', i)
