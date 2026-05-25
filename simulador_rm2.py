import streamlit as st
import pandas as pd

# Função para carregar dados
@st.cache_data
def carregar_questoes():
    df = pd.read_csv('questoes.csv')
    # Organiza em um dicionário estruturado para o app
    base = {}
    for tema in df['tema'].unique():
        base[tema] = df[df['tema'] == tema].to_dict('records')
    return base

# Substitua seu dicionário antigo por:
QUESTOES = carregar_questoes()

# Ajuste na parte do QUIZ onde acessa as questões:
# Onde estava q['opcoes'], agora precisamos montar a lista dinamicamente:
# q['opcoes'] = [q['op_a'], q['op_b'], q['op_c'], q['op_d'], q['op_e']]
