"""
Landing page (entry point) for the FarmTech Solutions Streamlit app.

This file intentionally contains only presentation code (no business
logic). It composes the landing page using helpers from `src.ui` and
reads KPI data via `src.data_loader.load_csv`. The goal is to keep this
module focused on layout and storytelling.
"""

import streamlit as st
from pathlib import Path
from src.ui import render_page_header, render_info_card, render_section_divider, render_metric_card, load_image_if_exists
from src.data_loader import load_csv

st.set_page_config(page_title='FarmTech Solutions', layout='wide')

render_page_header(
    'FarmTech Solutions',
    'Assistente Agrícola Inteligente\nMonitoramento, análise preditiva e apoio à decisão agrícola com Inteligência Artificial.',
    icon='🌾',
    banner='assets/banner.png'
)

st.markdown('')

# Quick overview cards
cols = st.columns(4)
cards = [
    ("Sensores IoT", "Coleta contínua de temperatura, umidade e telemetria.", "🌱"),
    ("Machine Learning", "Modelos preditivos para irrigação e risco.", "📊"),
    ("Oracle Database", "Persistência confiável e integração corporativa.", "🗄️"),
    ("Recomendações Agrícolas", "Ações práticas para otimizar produção e água.", "🚜"),
]
for c, info in zip(cols, cards):
    with c:
        render_info_card(info[0], info[1], info[2])

render_section_divider('KPIs Principais')
# Load data for KPIs (non-fatal if missing)
df = None
try:
    df = load_csv()
except Exception:
    df = None

if df is None or df.empty:
    st.warning('Dados não disponíveis para KPIs. Coloque o CSV em `data/sensores_data.csv`.')
else:
    # Compute a few high-level metrics for executive overview
    total = df.shape[0]
    mean_temp = round(df.temperatura.mean(), 2)
    mean_hum = round(df.umidade_solo.mean(), 2)
    # simple irrigation rate proxy (heuristic)
    irr_rate = round(((60 - df.umidade_solo).clip(lower=0)).mean(), 2)
    kcols = st.columns(4)
    with kcols[0]:
        render_metric_card('Total de registros', total)
    with kcols[1]:
        render_metric_card('Temperatura média (°C)', mean_temp)
    with kcols[2]:
        render_metric_card('Umidade média (%)', mean_hum)
    with kcols[3]:
        render_metric_card('Taxa irrigação (proxy)', irr_rate)

render_section_divider('Fluxo Visual do Sistema')
with st.container():
    # Usamos a classe "ft-metric" aqui para herdar o mesmo design dos cards de números
    fluxo_html = """
    <div class="ft-metric" style="padding: 16px; border-radius: 8px; border: 1px solid #e0e0e0; background-color: #f9fbf9; text-align: center;">
        <div class="ft-flow" style="color: #043927; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">
            Sensores IoT &rarr; Oracle Database &rarr; Machine Learning &rarr; Dashboard &rarr; Tomada de Decisão
        </div>
    </div>
    """
    st.markdown(fluxo_html, unsafe_allow_html=True)
    
render_section_divider('Benefícios do Projeto')
bcols = st.columns(4)
benefits = [
    ("Agricultura Inteligente", "Decisões baseadas em dados."),
    ("Economia de Água", "Irrigação otimizada reduz desperdício."),
    ("Monitoramento em Tempo Real", "Ações reativas e proativas."),
    ("Suporte à Decisão", "Recomendações práticas para produtores."),
]
for c, b in zip(bcols, benefits):
    with c:
        render_info_card(b[0], b[1], "✅")
