import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. Definição dos Parâmetros (Primeiro passo, obrigatório)
PARAMETROS = {
    'SOJA': {'umidade_min': 60.0, 'umidade_max': 80.0, 'ph_min': 6.0, 'ph_max': 7.0, 'ph_ideal': 6.5},
    'CAFE': {'umidade_min': 70.0, 'umidade_max': 80.0, 'ph_min': 5.5, 'ph_max': 6.5, 'ph_ideal': 6.0}
}

CALENDARIO = {
    'SOJA': {'MT': {'P': [8], 'K': [9], 'N': [11]}, 'GO': {'P': [9], 'K': [10], 'N': [12]}},
    'CAFE': {'MG': {'P': [9], 'N': [10, 12, 2], 'K': [11, 1, 3]}, 'SP': {'P': [10], 'N': [11, 1, 3], 'K': [12, 2, 4]}}
}

def obter_taxa_consumo(mes, cultura):
    if cultura == 'SOJA':
        return 1.5 if mes in [11, 12, 1, 2] else 0.8
    return 2.0 if mes in [9, 10] else 1.2

# 2. Configuração das Fazendas
fazendas = []
for i in range(1, 101):
    if i <= 25: fazendas.append({'ID_FAZENDA': i, 'CULTURA': 'SOJA', 'ESTADO': 'MT'})
    elif i <= 50: fazendas.append({'ID_FAZENDA': i, 'CULTURA': 'SOJA', 'ESTADO': 'GO'})
    elif i <= 75: fazendas.append({'ID_FAZENDA': i, 'CULTURA': 'CAFE', 'ESTADO': 'MG'})
    else: fazendas.append({'ID_FAZENDA': i, 'CULTURA': 'CAFE', 'ESTADO': 'SP'})

# 3. Inicialização dos Estados (Agora que PARAMETROS existe, isso vai funcionar)
estado_fazendas = {f['ID_FAZENDA']: {'ph': PARAMETROS[f['CULTURA']]['ph_ideal'], 'umi': 75.0, 
                                     'timer_n': 0, 'timer_p': 0, 'timer_k': 0, 
                                     'done_n': [], 'done_p': [], 'done_k': []} for f in fazendas}

# 4. Geração dos Dados
data_inicial = datetime(2022, 1, 1)
data_final = datetime(2025, 12, 31)
dias_totais = (data_final - data_inicial).days + 1
dados = []

print("Gerando dados...")

for dia in range(dias_totais):
    data_atual = data_inicial + timedelta(days=dia)
    mes = data_atual.month
    
    # Reset anual
    if data_atual.month == 1 and data_atual.day == 1:
        for f in fazendas:
            mem = estado_fazendas[f['ID_FAZENDA']]
            mem['done_n'], mem['done_p'], mem['done_k'] = [], [], []

    for f in fazendas:
        mem = estado_fazendas[f['ID_FAZENDA']]
        cal = CALENDARIO[f['CULTURA']][f['ESTADO']]
        
        n, p, k = 1, 1, 1
        # Lógica de Nutrientes
        for key, timer, lista, meses_alvo in [('N', 'timer_n', 'done_n', cal['N']), 
                                              ('P', 'timer_p', 'done_p', cal['P']), 
                                              ('K', 'timer_k', 'done_k', cal['K'])]:
            if mem[timer] > 0:
                mem[timer] -= 1
                if key == 'N': n = 0
                elif key == 'P': p = 0
                else: k = 0
            elif mes in meses_alvo and mes not in mem[lista] and random.random() < 0.05:
                mem[timer] = random.randint(2, 4)
                mem[lista].append(mes)
                if key == 'N': n = 0
                elif key == 'P': p = 0
                else: k = 0
        
        # Umidade e pH
        taxa = obter_taxa_consumo(mes, f['CULTURA'])
        mem['umi'] -= random.uniform(taxa * 0.5, taxa * 1.5)
        
        irrigar = (mem['umi'] < PARAMETROS[f['CULTURA']]['umidade_min'] and n==1 and p==1 and k==1)
        bomba = "LIGADA" if (irrigar or mem['umi'] < 40) else "DESLIGADA"
        if bomba == "LIGADA": mem['umi'] = PARAMETROS[f['CULTURA']]['umidade_max']
            
        mem['ph'] += random.uniform(-0.01, 0.01)
        ph = round(mem['ph'], 2)
        
        dados.append({
            'ID_FAZENDA': f['ID_FAZENDA'], 
            'DATA_LEITURA': data_atual.strftime('%Y-%m-%d'), 
            'N_STATUS': n, 'P_STATUS': p, 'K_STATUS': k, 
            'LDR_VALOR': int((ph/14)*4095),
            'PH_VALOR': f"{ph}".replace('.', ','), 
            'UMIDADE_VALOR': f"{round(mem['umi'], 2)}".replace('.', ','),
            'BOMBA_STATUS': bomba
        })

df = pd.DataFrame(dados)
caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensores_v8_final.csv')
df.to_csv(caminho, sep=';', index=False)
print(f"Sucesso! Arquivo gerado em: {caminho}")