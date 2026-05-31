import streamlit as st
import pandas as pd
import random
import os

# Configuração da página
st.set_page_config(page_title="Simulador RM2 - Marinha", page_icon="⚓", layout="centered")

# ── Banco de temas ─────────────────────────────────────────────────────────────
TEMAS = [
    ("interpretacao",  "Interpretação de Texto"),
    ("ortografia",     "Ortografia e Acentuação"),
    ("morfologia",     "Classes de Palavras"),
    ("sintaxe",        "Sintaxe e Análise"),
    ("concordancia",   "Concordância Verbal/Nominal"),
    ("regencia",       "Regência e Crase"),
    ("pontuacao",      "Pontuação"),
    ("semantica",      "Semântica e Figuras de Linguagem"),
    ("vocativo",       "Vocativo"),
]

# ── Mapa de Aulas ──────────────────────────────────────────────────────────────
AULAS = {
    1:  "Frase, Oração, Período",
    2:  "Sujeito",
    3:  "Transitividade Verbal",
    4:  "Complementos Verbais",
    5:  "PIS e PA",
    6:  "Predicativo do Sujeito e Predicativo do Objeto",
    7:  "Adjunto Adverbial",
    8:  "Complemento Nominal",
    9:  "Adjunto Adnominal",
    10: "Vozes Verbais e Agente da Passiva",
    11: "Aposto e Vocativo",
    12: "Orações Subordinadas Substantivas",
    13: "Orações Subordinadas Adjetivas",
    14: "Orações Subordinadas Adverbiais",
    15: "Orações Coordenadas",
    16: "Regência Verbal",
    17: "Regência com Pronome Relativo",
    18: "Crase",
    19: "Concordância Verbal",
    20: "Colocação Pronominal",
    21: "Valores do SE",
    22: "Pontuação",
    23: "Fonética - Pressupostos para Acentuação",
    24: "Acentuação Gráfica",
    25: "Palavras e Expressões",
    26: "Ortografia",
    27: "Hífen",
    28: "Semântica",
    29: "Estrutura e Formação das Palavras",
    30: "Substantivo",
    31: "Adjetivo",
    32: "Artigo",
    33: "Pronome",
    34: "Numeral",
    35: "Verbo",
    36: "Advérbio",
    37: "Preposição",
    38: "Interjeição e Palavras Denotativas",
    39: "Concordância Nominal",
    40: "Valores do QUE",
    41: "Funções da Linguagem",
    42: "Figuras de Linguagem",
    43: "Tipos de Discurso",
    44: "Coesão e Coerência",
    45: "Tipologia Textual",
}

# ── URL base dos PDFs no GitHub ────────────────────────────────────────────────
GITHUB_RAW = "https://raw.githubusercontent.com/lucas-gr-git/projeto_rm2/main/mapa/"

# Nomes exatos dos arquivos por aula (baseado nos prints fornecidos)
ARQUIVOS_POR_AULA = {
    1:  [
        "PORT - AULA 1 - FRASE, ORAÇÃO, PERÍODO - MAPA MENTAL.pdf",
        "PORT - AULA 1 - FRASE, ORAÇÃO, PERÍODO - TABELA-RESUMO - OK.pdf",
    ],
    2:  [
        "PORT - AULA 2 - SUJEITO - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 2 - SUJEITO - PARTE 2 - MAPA MENTAL1.pdf",
        "PORT - AULA 2 - SUJEITO - TABELA-RESUMO - OK.pdf",
    ],
    3:  [
        "PORT - AULA 3 - TRANSITIVIDADE VERBAL - MAPA MENTAL.pdf",
        "PORT - AULA 3 - TRANSITIVIDADE VERBAL - TABELA-RESUMO - OK.pdf",
    ],
    4:  [
        "PORT - AULA 4 - COMPLEMENTOS VERBAIS - MAPA MENTAL.pdf",
        "PORT - AULA 4 - COMPLEMENTOS VERBAIS - SE - MAPA MENTAL.pdf",
        "PORT - AULA 4 - COMPLEMENTOS VERBAIS - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 4 - COMPLEMENTOS VERBAIS - VERBOS CAUSATIVOS E SENTITIVOS - MAPA MENTAL.pdf",
    ],
    5:  [
        "PORT - AULA 5 - PIS E PA - MAPA MENTAL.pdf",
        "PORT - AULA 5 - PIS E PA - TABELA-RESUMO - OK.pdf",
    ],
    6:  [
        "PORT - AULA 6 - PRED SUJEITO E PRED OBJETO - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 6 - PREDICATIVO DO SUJEITO E PREDICATIVO DO OBJETO - MAPA MENTAL.pdf",
    ],
    7:  [
        "PORT - AULA 7 - ADJUNTO ADVERBIAL - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 7 - ADJUNTO ADVERBIAL - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 7 - ADJUNTO ADVERBIAL - TABELA-RESUMO - OK.pdf",
    ],
    8:  [
        "PORT - AULA 8 - COMPLEMENTO NOMINAL - MAPA MENTAL.pdf",
        "PORT - AULA 8 - COMPLEMENTO NOMINAL - TABELA-RESUMO - OK.pdf",
    ],
    9:  [
        "PORT - AULA 9 - ADJUNTO ADNOMINAL - MAPA MENTAL.pdf",
        "PORT - AULA 9 - ADJUNTO ADNOMINAL - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 9 - COMPLEMENTO NOMINAL X ADJUNTO ADNOMINAL - MAPA MENTAL.pdf",
    ],
    10: [
        "PORT - AULA 10 - VOZES VERBAIS E AGENTE DA PASSIVA - MAPA MENTAL.pdf",
        "PORT - AULA 10 - VOZES VERBAIS E AGENTE DA PASSIVA - TABELA-RESUMO - OK.pdf",
    ],
    11: [
        "PORT - AULA 11 - APOSTO E VOCATIVO - MAPA MENTAL.pdf",
        "PORT - AULA 11 - APOSTO, VOCATIVO E PREDICADO - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 11 - PREDICADO - MAPA MENTAL.pdf",
    ],
    12: [
        "PORT - AULA 12 - ORAÇÕES SUBORDINADAS SUBSTANTIVAS - MAPA MENTAL.pdf",
        "PORT - AULA 12 - ORAÇÕES SUBORDINADAS SUBSTANTIVAS - TABELA-RESUMO - OK.pdf",
    ],
    13: [
        "PORT - AULA 13 - ORAÇÕES SUBORDINADAS ADJETIVAS - MAPA MENTAL.pdf",
        "PORT - AULA 13 - ORAÇÕES SUBORDINADAS ADJETIVAS - TABELA-RESUMO - OK.pdf",
    ],
    14: [
        "PORT - AULA 14 - ORAÇÕES SUBORDINADAS ADVERBIAIS - MAPA MENTAL.pdf",
        "PORT - AULA 14 - ORAÇÕES SUBORDINADAS ADVERBIAIS - TABELA-RESUMO - OK.pdf",
    ],
    15: [
        "PORT - AULA 15 - ORAÇÕES COORDENADAS - MAPA MENTAL.pdf",
        "PORT - AULA 15 - ORAÇÕES COORDENADAS - TABELA-RESUMO - OK.pdf",
    ],
    16: [
        "PORT - AULA 16 - REGÊNCIA VERBAL - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 16 - REGÊNCIA VERBAL - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 16 - REGÊNCIA VERBAL - PARTE 3 - MAPA MENTAL.pdf",
        "PORT - AULA 16 - REGÊNCIA VERBAL - PARTE 4 - MAPA MENTAL.pdf",
        "PORT - AULA 16 - REGÊNCIA VERBAL - PARTE 5 - MAPA MENTAL.pdf",
        "PORT - AULA 16 - REGÊNCIA VERBAL - TABELA-RESUMO - OK.pdf",
    ],
    17: [
        "PORT - AULA 17 - REGÊNCIA COM PRONOME RELATIVO - MAPA MENTAL.pdf",
        "PORT - AULA 17 - REGÊNCIA COM PRONOME RELATIVO - TABELA-RESUMO - OK.pdf",
    ],
    18: [
        "PORT - AULA 18 - CRASE - CASOS FACULTATIVOS - MAPA MENTAL.pdf",
        "PORT - AULA 18 - CRASE - CASOS PARTICULARES - MAPA MENTAL.pdf",
        "PORT - AULA 18 - CRASE - CASOS PROIBIDOS - MAPA MENTAL.pdf",
        "PORT - AULA 18 - CRASE - TABELA-RESUMO - OK.pdf",
    ],
    19: [
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - PARTE 3 - MAPA MENTAL.pdf",
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - PARTE 4 - MAPA MENTAL.pdf",
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - PARTE 5 - MAPA MENTAL.pdf",
        "PORT - AULA 19 - CONCORDÂNCIA VERBAL - TABELA-RESUMO - OK.pdf",
    ],
    20: [
        "PORT - AULA 20 - COLOCAÇÃO PRONOMINAL - CASOS FACULTATIVOS - MAPA MENTAL.pdf",
        "PORT - AULA 20 - COLOCAÇÃO PRONOMINAL - MESÓCLISE E ÊNCLISE - MAPA MENTAL.pdf",
        "PORT - AULA 20 - COLOCAÇÃO PRONOMINAL - NAS LOCUÇÕES VERBAIS E APOSSÍNCLISE - MAPA MENTAL.pdf",
        "PORT - AULA 20 - COLOCAÇÃO PRONOMINAL - PRÓCLISE - MAPA MENTAL.pdf",
        "PORT - AULA 20 - COLOCAÇÃO PRONOMINAL - TABELA-RESUMO - OK.pdf",
    ],
    21: [
        "PORT - AULA 21 - VALORES DO SE - MAPA MENTAL.pdf",
        "PORT - AULA 21 - VALORES DO SE - TABELA-RESUMO - OK.pdf",
    ],
    22: [
        "PORT - AULA 22 - PONTUAÇÃO - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 22 - PONTUAÇÃO - VÍRGULA OBRIGATÓRIA - MAPA MENTAL.pdf",
        "PORT - AULA 22 - PONTUAÇÃO - VÍRGULA PROIBIDA E CASOS DE DESLOCAMENTO - MAPA MENTAL.pdf",
    ],
    23: [
        "PORT - AULA 23 - FONÉTICA - PRESSUP ACENTUAÇÃO - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 23 - FONÉTICA - PRESSUPOSTOS PARA ACENTUAÇÃO - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 23 - FONÉTICA - PRESSUPOSTOS PARA ACENTUAÇÃO - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 23 - FONÉTICA - PRESSUPOSTOS PARA ACENTUAÇÃO - PARTE 3 - MAPA MENTAL.pdf",
    ],
    24: [
        "PORT - AULA 24 - ACENTUAÇÃO GRÁFICA - MAPA MENTAL.pdf",
        "PORT - AULA 24 - ACENTUAÇÃO GRÁFICA - TABELA-RESUMO - OK.pdf",
    ],
    25: [
        "PORT - AULA 25 - PALAVRAS E EXPRESSÕES - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 25 - PALAVRAS E EXPRESSÕES - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 25 - PALAVRAS E EXPRESSÕES - PARTE 3 - MAPA MENTAL.pdf",
        "PORT - AULA 25 - PALAVRAS E EXPRESSÕES - TABELA-RESUMO - OK.pdf",
    ],
    26: [
        "PORT - AULA 26 - ORTOGRAFIA - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 26 - ORTOGRAFIA - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 26 - ORTOGRAFIA - PARTE 3 - MAPA MENTAL.pdf",
        "PORT - AULA 26 - ORTOGRAFIA - TABELA-RESUMO - OK.pdf",
    ],
    27: [
        "PORT - AULA 27 - EMPREGO DO HÍFEN - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 27 - HÍFEN - MAPA MENTAL.pdf",
        "PORT - AULA 27 - HÍFEN (NÃO SE EMPREGA E EXCEÇÕES) - MAPA MENTAL.pdf",
        "PORT - AULA 27 - HÍFEN (NAS PALAVRASAS COMPOSTAS) - MAPA MENTAL.pdf",
        "PORT - AULA 27 - HÍFEN (NAS PALAVRASAS DERIVADAS) - MAPA MENTAL.pdf",
    ],
    28: [
        "PORT - AULA 28 - SEMÂNTICA - HOMÔNIMOS E PARÔNIMOS - LISTA EXTRA - OK.pdf",
        "PORT - AULA 28 - SEMÂNTICA - MAPA MENTAL.pdf",
        "PORT - AULA 28 - SEMÂNTICA - TABELA-RESUMO - OK.pdf",
    ],
    29: [
        "PORT - AULA 29 - ESTRUTURA DAS PALAVRAS - MAPA MENTAL.pdf",
        "PORT - AULA 29 - ESTRUTURA DE PALAVRAS - LISTA EXTRA - OK.pdf",
        "PORT - AULA 29 - FORMAÇÃO DAS PALAVRAS - MAPA MENTAL.pdf",
        "PORT - AULA 29 - FORMAÇÃO DE PALAVRAS - TABELA-RESUMO - OK.pdf",
    ],
    30: [
        "PORT - AULA 30 - SUBSTANTIVO - COLETIVOS - LISTA EXTRA - OK.pdf",
        "PORT - AULA 30 - SUBSTANTIVO - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 30 - SUBSTANTIVO - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 30 - SUBSTANTIVO - PARTE 3 - MAPA MENTAL.pdf",
        "PORT - AULA 30 - SUBSTANTIVO - PARTE 4 - MAPA MENTAL.pdf",
        "PORT - AULA 30 - SUBSTANTIVO - PLURAL EM -ÃO - LISTA EXTRA - OK.pdf",
        "PORT - AULA 30 - SUBSTANTIVO COMPLETA - TABELA-RESUMO - OK.pdf",
    ],
    31: [
        "PORT - AULA 31 - ADJETIVO - LOCUÇÕES ADJETIVAS E SUPERLATIVOS - LISTA EXTRA.pdf",
        "PORT - AULA 31 - ADJETIVO - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 31 - ADJETIVO - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 31 - ADJETIVO - TABELA-RESUMO - OK.pdf",
    ],
    32: [
        "PORT - AULA 32 - ARTIGO - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 32 - ARTIGO - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 32 - ARTIGO - TABELA-RESUMO - OK.pdf",
    ],
    33: [
        "PORT - AULA 33 - PRONOME - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 33 - PRONOMES DE TRATAMENTO - MAPA MENTAL.pdf",
        "PORT - AULA 33 - PRONOMES DEMONSTRATIVOS E INTERROGATIVOS - MAPA MENTAL.pdf",
        "PORT - AULA 33 - PRONOMES INDEFINIDOS E POSSESSIVOS - MAPA MENTAL.pdf",
        "PORT - AULA 33 - PRONOMES PESSOAIS - MAPA MENTAL.pdf",
    ],
    34: [
        "PORT - AULA 34 - NUMERAL - MAPA MENTAL.pdf",
        "PORT - AULA 34 - NUMERAL - TABELA-RESUMO - OK.pdf",
    ],
    35: [
        "PORT - AULA 35 - VERBO - IMPERATIVO AFIRMATIVO E IMPERATIVO NEGATIVO - MAPA MENTAL.pdf",
        "PORT - AULA 35 - VERBO - INDICATIVO E SUBJUNTIVO - MAPA MENTAL.pdf",
        "PORT - AULA 35 - VERBO - INFINITIVO E PARTICÍPIO - MAPA MENTAL.pdf",
        "PORT - AULA 35 - VERBO - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 35 - VERBO - TEMPO COMPOSTO E INFINITIVO FLEXIONADO - MAPA MENTAL.pdf",
    ],
    36: [
        "PORT - AULA 36 - ADVÉRBIO - INTERROGATIVOS E GRAU - MAPA MENTAL.pdf",
        "PORT - AULA 36 - ADVÉRBIO - MAPA MENTAL.pdf",
        "PORT - AULA 36 - ADVÉRBIO - TABELA-RESUMO - OK.pdf",
    ],
    37: [
        "PORT - AULA 37 - PREPOSIÇÃO - MAPA MENTAL.pdf",
        "PORT - AULA 37 - PREPOSIÇÃO - TABELA-RESUMO - OK.pdf",
    ],
    38: [
        "PORT - AULA 38 - INTERJ E PAL DENOTATIVAS - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 38 - INTERJEIÇÃO - MAPA MENTAL.pdf",
        "PORT - AULA 38 - PALAVRAS DENOTATIVAS - MAPA MENTAL.pdf",
    ],
    39: [
        "PORT - AULA 39 - CONCORDÂNCIA NOMINAL - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 39 - CONCORDÂNCIA NOMINAL - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 39 - CONCORDÂNCIA NOMINAL - TABELA-RESUMO - OK.pdf",
    ],
    40: [
        "PORT - AULA 40 - VALORES DO QUE - PARTE 1 - MAPA MENTAL.pdf",
        "PORT - AULA 40 - VALORES DO QUE - PARTE 2 - MAPA MENTAL.pdf",
        "PORT - AULA 40 - VALORES DO QUE - TABELA-RESUMO - OK.pdf",
    ],
    41: [
        "PORT - AULA 41 - FUNÇÕES DA LINGUAGEM - MAPA MENTAL.pdf",
        "PORT - AULA 41 - FUNÇÕES DA LINGUAGEM - TABELA-RESUMO - OK.pdf",
    ],
    42: [
        "PORT - AULA 42 - FIGURAS DE LINGUAGEM - PALAVRA - MAPA MENTAL.pdf",
        "PORT - AULA 42 - FIGURAS DE LINGUAGEM - PENSAMENTO - MAPA MENTAL.pdf",
        "PORT - AULA 42 - FIGURAS DE LINGUAGEM - SINTAXE - MAPA MENTAL.pdf",
        "PORT - AULA 42 - FIGURAS DE LINGUAGEM - SONORAS - MAPA MENTAL.pdf",
        "PORT - AULA 42 - FIGURAS DE LINGUAGEM - TABELA-RESUMO - OK.pdf",
    ],
    43: [
        "PORT - AULA 43 - TIPOS DE DISCURSO - MAPA MENTAL.pdf",
        "PORT - AULA 43 - TIPOS DE DISCURSO - TABELA-RESUMO - OK.pdf",
    ],
    44: [
        "PORT - AULA 44 - COESÃO E COERÊNCIA - MAPA MENTAL.pdf",
        "PORT - AULA 44 - COESÃO E COERÊNCIA - TABELA-RESUMO - OK.pdf",
        "PORT - AULA 44 - FORMAS DE SUBSTITUIÇÃO E REITERAÇÃO - MAPA MENTAL.pdf",
    ],
    45: [
        "PORT - AULA 45 - TIPOLOGIA TEXTUAL - MAPA MENTAL.pdf",
        "PORT - AULA 45 - TIPOLOGIA TEXTUAL - TABELA-RESUMO - OK.pdf",
    ],
}

# ── Leitura Inteligente e Blindada da Planilha ─────────────────────────────────
@st.cache_data
def carregar_questoes():
    arquivo = 'questoes.csv'
    if not os.path.exists(arquivo):
        if os.path.exists('questoes.CSV'):
            arquivo = 'questoes.CSV'
        else:
            st.error("⚠️ O arquivo de questões não foi encontrado no GitHub.")
            return {}

    combinacoes = [
        {'sep': ';', 'enc': 'utf-8'},
        {'sep': ';', 'enc': 'cp1252'},
        {'sep': ';', 'enc': 'latin-1'},
        {'sep': ',', 'enc': 'utf-8'},
        {'sep': ',', 'enc': 'cp1252'},
    ]

    df = None
    for comb in combinacoes:
        try:
            test_df = pd.read_csv(arquivo, sep=comb['sep'], encoding=comb['enc'])
            if len(test_df.columns) >= 5:
                df = test_df
                break
        except Exception:
            continue

    if df is None:
        st.error("❌ Erro crítico: não foi possível decodificar o arquivo CSV.")
        return {}

    try:
        df.columns = df.columns.str.strip().str.lower()
        df['tema'] = df['tema'].astype(str).str.strip().str.lower()

        base = {}
        for tema in df['tema'].unique():
            if pd.isna(tema) or str(tema).strip() == '' or str(tema) == 'nan':
                continue

            questoes_tema = df[df['tema'] == tema].to_dict('records')
            lista_formatada = []

            for q in questoes_tema:
                def limpar_texto(txt):
                    if pd.isna(txt): return ""
                    t = str(txt).strip()
                    if t.startswith('"') and t.endswith('"'):
                        t = t[1:-1]
                    return t.replace('""', '"').replace('\\n', '\n')

                texto_base = limpar_texto(q.get('texto'))
                enunciado  = limpar_texto(q.get('enunciado'))
                op_a = limpar_texto(q.get('op_a'))
                op_b = limpar_texto(q.get('op_b'))
                op_c = limpar_texto(q.get('op_c'))
                op_d = limpar_texto(q.get('op_d'))
                op_e = limpar_texto(q.get('op_e'))

                opcoes_limpas = [op for op in [op_a, op_b, op_c, op_d, op_e] if op != '']

                try:
                    gabarito = int(float(str(q.get('gabarito', 0)).strip()))
                except:
                    gabarito = 0

                lista_formatada.append({
                    "ano":       str(q.get('ano', 'N/A')).split('.')[0],
                    "texto":     texto_base,
                    "enunciado": enunciado if enunciado else "Sem enunciado",
                    "opcoes":    opcoes_limpas,
                    "gabarito":  gabarito,
                    "explicacao": limpar_texto(q.get('explicacao'))
                })
            base[tema] = lista_formatada
        return base
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
        return {}

QUESTOES = carregar_questoes()

# ── Controle de Estado ──────────────────────────────────────────────────────────
for key, val in [
    ('tela', 'menu'),
    ('questoes_atuais', []),
    ('indice', 0),
    ('historico', []),
    ('resposta_enviada', False),
    ('acertos', 0),
    ('tema_nome', ""),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Funções de Navegação ────────────────────────────────────────────────────────
def iniciar_quiz(tipo, nome):
    st.session_state.acertos = 0
    st.session_state.indice = 0
    st.session_state.historico = []
    st.session_state.resposta_enviada = False
    st.session_state.tela = 'quiz'
    st.session_state.tema_nome = nome

    lista = []
    if tipo == 'geral':
        for qs in QUESTOES.values():
            lista.extend(qs)
        random.shuffle(lista)
        st.session_state.questoes_atuais = lista   # TODAS as questões
    else:
        lista = QUESTOES.get(tipo, []).copy()
        random.shuffle(lista)
        st.session_state.questoes_atuais = lista

def voltar_menu():
    st.session_state.tela = 'menu'

# ── ABAS PRINCIPAIS ─────────────────────────────────────────────────────────────
aba_simulador, aba_mapas = st.tabs(["📝 Simulador", "🗺️ Mapas Mentais"])

# ════════════════════════════════════════════════════════════════════════════════
# ABA 1 — SIMULADOR
# ════════════════════════════════════════════════════════════════════════════════
with aba_simulador:

    # TELA 1: MENU
    if st.session_state.tela == 'menu':
        st.title("⚓ Simulador de Português")
        st.subheader("Concurso RM2 - Marinha do Brasil")
        st.divider()

        if not QUESTOES:
            st.warning("⚠️ Nenhuma questão encontrada. Verifique o arquivo de dados.")
        else:
            st.markdown("### Escolha seu modo de estudo:")

            total_q = sum(len(qs) for qs in QUESTOES.values())

            if st.button(f"🌟 Simulado Geral ({total_q} questões aleatórias)", use_container_width=True):
                iniciar_quiz('geral', 'Simulado Geral')
                st.rerun()

            st.write("Ou escolha um tema específico:")
            col1, col2 = st.columns(2)

            for i, (tid, label) in enumerate(TEMAS):
                qtd = len(QUESTOES.get(tid, []))
                if qtd > 0:
                    col = col1 if i % 2 == 0 else col2
                    with col:
                        if st.button(f"📚 {label} ({qtd})", use_container_width=True, key=tid):
                            iniciar_quiz(tid, label)
                            st.rerun()

    # TELA 2: QUIZ
    elif st.session_state.tela == 'quiz':
        q     = st.session_state.questoes_atuais[st.session_state.indice]
        total = len(st.session_state.questoes_atuais)
        atual = st.session_state.indice + 1

        st.caption(f"Tema: {st.session_state.tema_nome} | Ano: {q.get('ano', 'N/A')}")
        st.progress(atual / total, text=f"Questão {atual} de {total}")

        if q["texto"]:
            st.info(q["texto"])

        st.markdown(f"#### {q['enunciado']}")

        resposta_usuario = st.radio(
            "Selecione sua resposta:",
            q["opcoes"],
            index=None,
            key=f"radio_{st.session_state.indice}"
        )

        if not st.session_state.resposta_enviada:
            if st.button("Confirmar Resposta", type="primary"):
                if resposta_usuario:
                    st.session_state.resposta_enviada = True
                    st.rerun()
                else:
                    st.warning("Por favor, selecione uma alternativa.")
        else:
            idx_escolhido = q["opcoes"].index(resposta_usuario)
            correto = (idx_escolhido == q["gabarito"])

            if correto:
                st.success("✅ Resposta Correta!")
                if f"pontuou_{st.session_state.indice}" not in st.session_state:
                    st.session_state.acertos += 1
                    st.session_state[f"pontuou_{st.session_state.indice}"] = True
            else:
                gabarito_texto = q["opcoes"][q["gabarito"]] if q["gabarito"] < len(q["opcoes"]) else "Gabarito inválido"
                st.error("❌ Resposta Incorreta.")
                st.warning(f"O gabarito correto era: **{gabarito_texto}**")

            st.info(f"**Explicação:**\n{q['explicacao']}")

            if len(st.session_state.historico) <= st.session_state.indice:
                st.session_state.historico.append({
                    "questao": q,
                    "escolha": resposta_usuario,
                    "correto": correto
                })

            if atual < total:
                if st.button("Próxima Questão ➔"):
                    st.session_state.indice += 1
                    st.session_state.resposta_enviada = False
                    st.rerun()
            else:
                if st.button("Ver Resultados Finais 🏆", type="primary"):
                    st.session_state.tela = 'resultado'
                    st.rerun()

    # TELA 3: RESULTADOS
    elif st.session_state.tela == 'resultado':
        total   = len(st.session_state.questoes_atuais)
        acertos = st.session_state.acertos
        pct     = int((acertos / total) * 100)

        st.title("Desempenho Final")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Acertos", value=f"{acertos} de {total}")
        with col2:
            st.metric(label="Aproveitamento", value=f"{pct}%")

        st.markdown("### 📝 Revisão do Gabarito")

        for i, h in enumerate(st.session_state.historico):
            q     = h["questao"]
            icone = "✅" if h["correto"] else "❌"

            with st.expander(f"{icone} Questão {i+1} - {q['enunciado'][:50]}..."):
                if q["texto"]:
                    st.caption("Texto base:")
                    st.write(q["texto"])

                st.write(f"**{q['enunciado']}**")
                st.write(f"Sua resposta: {h['escolha']}")
                if not h["correto"]:
                    st.write(f"Gabarito: {q['opcoes'][q['gabarito']]}")

                st.success(f"**Comentário:** {q['explicacao']}")

        st.divider()
        if st.button("Voltar ao Menu Principal"):
            st.session_state.clear()
            voltar_menu()
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# ABA 2 — MAPAS MENTAIS
# ════════════════════════════════════════════════════════════════════════════════
with aba_mapas:
    st.title("🗺️ Mapas Mentais")
    st.subheader("Português - Concurso RM2")
    st.divider()

    opcoes_aulas = [f"Aula {n} - {nome}" for n, nome in AULAS.items()]
    escolha = st.selectbox("Selecione a aula:", opcoes_aulas)

    numero_aula = int(escolha.split(" ")[1])
    arquivos    = ARQUIVOS_POR_AULA.get(numero_aula, [])

    st.markdown(f"### Aula {numero_aula} — {AULAS[numero_aula]}")
    st.caption(f"{len(arquivos)} arquivo(s) disponível(is)")
    st.divider()

    import requests
    from urllib.parse import quote

    for arquivo in arquivos:
        url = GITHUB_RAW + quote(arquivo)

        # Nome amigável
        nome_amigavel = arquivo
        partes = arquivo.split(" - ", 2)
        if len(partes) >= 3:
            nome_amigavel = partes[2].replace(".pdf", "").strip()

        with st.expander(f"📄 {nome_amigavel}", expanded=False):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    st.download_button(
                        label="⬇️ Baixar PDF",
                        data=response.content,
                        file_name=arquivo,
                        mime="application/pdf",
                        key=f"dl_{arquivo}"
                    )
                    # Exibe o PDF inline via iframe com Google Docs Viewer
                    viewer_url = f"https://docs.google.com/viewer?url={url}&embedded=true"
                    st.components.v1.iframe(viewer_url, height=600, scrolling=True)
                else:
                    st.warning(f"⚠️ Arquivo não encontrado no GitHub: {arquivo}")
            except Exception as e:
                st.error(f"Erro ao carregar o PDF: {e}")
