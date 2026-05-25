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
]

# ── Leitura Inteligente e Blindada da Planilha ─────────────────────────────────
@st.cache_data
def carregar_questoes():
    # 1. Detecta o arquivo independente de estar em minúsculo (.csv) ou maiúsculo (.CSV)
    arquivo = 'questoes.csv'
    if not os.path.exists(arquivo):
        if os.path.exists('questoes.CSV'):
            arquivo = 'questoes.CSV'
        else:
            st.error("⚠️ O arquivo de questões não foi encontrado no GitHub. Certifique-se de que ele se chama 'questoes.csv'.")
            return {}

    # 2. Testa automaticamente combinações de separadores e encodings do Excel brasileiro
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
            # Se conseguiu ler pelo menos 5 colunas estruturadas, achou o padrão correto
            if len(test_df.columns) >= 5:
                df = test_df
                break
        except Exception:
            continue

    if df is None:
        st.error("❌ Erro crítico: O Excel gerou um formato de arquivo que o sistema não conseguiu decodificar. Tente salvar novamente como CSV.")
        return {}

    try:
        # Padroniza os nomes das colunas para evitar erros de digitação (remove espaços e deixa minúsculo)
        df.columns = df.columns.str.strip().str.lower()
        df['tema'] = df['tema'].astype(str).str.strip().str.lower()
        
        base = {}
        for tema in df['tema'].unique():
            if pd.isna(tema) or str(tema).strip() == '' or str(tema) == 'nan':
                continue
                
            questoes_tema = df[df['tema'] == tema].to_dict('records')
            lista_formatada = []
            
            for q in questoes_tema:
                # Função interna para limpar as aspas extras que o Excel coloca automaticamente
                def limpar_texto(txt):
                    if pd.isna(txt): return ""
                    t = str(txt).strip()
                    if t.startswith('"') and t.endswith('"'):
                        t = t[1:-1]
                    return t.replace('""', '"').replace('\\n', '\n')

                texto_base = limpar_texto(q.get('texto'))
                enunciado = limpar_texto(q.get('enunciado'))
                
                op_a = limpar_texto(q.get('op_a'))
                op_b = limpar_texto(q.get('op_b'))
                op_c = limpar_texto(q.get('op_c'))
                op_d = limpar_texto(q.get('op_d'))
                op_e = limpar_texto(q.get('op_e'))
                
                opcoes_brutas = [op_a, op_b, op_c, op_d, op_e]
                opcoes_limpas = [op for op in opcoes_brutas if op != '']
                
                # Garante que o gabarito vai ser lido como número inteiro puro
                try:
                    gabarito = int(float(str(q.get('gabarito', 0)).strip()))
                except:
                    gabarito = 0

                lista_formatada.append({
                    "ano": str(q.get('ano', 'N/A')).split('.')[0],
                    "texto": texto_base,
                    "enunciado": enunciado if enunciado else "Sem enunciado",
                    "opcoes": opcoes_limpas,
                    "gabarito": gabarito,
                    "explicacao": limpar_texto(q.get('explicacao'))
                })
            base[tema] = lista_formatada
        return base
    except Exception as e:
        st.error(f"❌ Erro ao processar as linhas do arquivo: {e}")
        return {}

# Executa o carregamento blindado
QUESTOES = carregar_questoes()

# ── Controle de Estado ──────────────────────────────────────────────────────────
if 'tela' not in st.session_state:
    st.session_state.tela = 'menu'
if 'questoes_atuais' not in st.session_state:
    st.session_state.questoes_atuais = []
if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'resposta_enviada' not in st.session_state:
    st.session_state.resposta_enviada = False
if 'acertos' not in st.session_state:
    st.session_state.acertos = 0
if 'tema_nome' not in st.session_state:
    st.session_state.tema_nome = ""

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
        st.session_state.questoes_atuais = lista[:15]
    else:
        lista = QUESTOES.get(tipo, []).copy()
        random.shuffle(lista)
        st.session_state.questoes_atuais = lista

def voltar_menu():
    st.session_state.tela = 'menu'

# ── Renderização das Telas ──────────────────────────────────────────────────────

# TELA 1: MENU
if st.session_state.tela == 'menu':
    st.title("⚓ Simulador de Português")
    st.subheader("Concurso RM2 - Marinha do Brasil")
    st.divider()
    
    if not QUESTOES:
        st.warning("⚠️ Nenhuma questão ativa encontrada. Verifique o arquivo de dados.")
    else:
        st.markdown("### Escolha seu modo de estudo:")
        
        total_q = sum(len(qs) for qs in QUESTOES.values())
        limite = min(15, total_q)
        
        if st.button(f"🌟 Simulado Geral ({limite} questões aleatórias)", use_container_width=True):
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
    q = st.session_state.questoes_atuais[st.session_state.indice]
    total = len(st.session_state.questoes_atuais)
    atual = st.session_state.indice + 1
    
    st.caption(f"Tema: {st.session_state.tema_nome} | Ano: {q.get('ano', 'N/A')}")
    st.progress(atual / total, text=f"Questão {atual} de {total}")
    
    if q["texto"]:
        st.info(q["texto"])
        
    st.markdown(f"#### {q['enunciado']}")
    
    resposta_usuario = st.radio("Selecione sua resposta:", q["opcoes"], index=None, key=f"radio_{st.session_state.indice}")
    
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
            st.error(f"❌ Resposta Incorreta.")
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
                st.session_state.shadow_enviada = False
                st.session_state.resposta_enviada = False
                st.rerun()
        else:
            if st.button("Ver Resultados Finais 🏆", type="primary"):
                st.session_state.tela = 'resultado'
                st.rerun()

# TELA 3: RESULTADOS
elif st.session_state.tela == 'resultado':
    total = len(st.session_state.questoes_atuais)
    acertos = st.session_state.acertos
    pct = int((acertos / total) * 100)
    
    st.title("Desempenho Final")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Acertos", value=f"{acertos} de {total}")
    with col2:
        st.metric(label="Aproveitamento", value=f"{pct}%")
        
    st.markdown("### 📝 Revisão do Gabarito")
    
    for i, h in enumerate(st.session_state.historico):
        q = h["questao"]
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
