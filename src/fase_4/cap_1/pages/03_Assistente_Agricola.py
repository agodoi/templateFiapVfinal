"""
Assistente Agrícola (UX de consultoria).

Permite entrada manual de parâmetros e retorna uma recomendação simples
com nível de risco e explicação amigável para o produtor.
"""

import streamlit as st
from src.data_loader import load_csv
from src.preprocessing import derive_volume_irrigacao
from src.recommendations import recommend
from src.ui import render_section_divider, render_info_card

st.set_page_config(page_title='Assistente Agrícola', layout='wide')
st.title('03 - Assistente Agrícola')

df = load_csv()
st.sidebar.header('Entrada manual')
um = st.sidebar.number_input('Umidade solo', value=float(df.umidade_solo.mean()))
temp = st.sidebar.number_input('Temperatura', value=float(df.temperatura.mean()))
nut = st.sidebar.number_input('Nutrientes N', value=float(df.nutrientes_N.mean()))

df2 = derive_volume_irrigacao(df)
vol = max(0.0, (60 - um) * 0.8 + max(0, temp - 28) * 1.5)

if st.sidebar.button('Gerar recomendação'):
    rec = recommend(umidade_solo=um, temperatura=temp, nutrientes_N=nut, volume_estimado=vol)
    render_section_divider('Previsão e Nível de Risco')
    # simple risk level
    if vol < 10:
        risk = ('🟢 Baixo', 'Baixa prioridade de irrigação.')
    elif vol < 25:
        risk = ('🟡 Médio', 'Irrigação moderada recomendada.')
    else:
        risk = ('🔴 Alto', 'Irrigação imediata recomendada.')
    st.markdown(f"**Nível de risco:** {risk[0]} - {risk[1]}")
    render_section_divider('Recomendação Agrícola')
    render_info_card('Recomendação', rec, icon='🌿')
    render_section_divider('Explicação amigável')
    st.write(f'Com base em umidade {um:.0f}%, temperatura {temp:.1f}°C e nutrientes {nut:.0f}, recomenda-se:')
    st.write(rec)
