import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Simulador RM2 - Marinha", page_icon="⚓", layout="centered")

# ── Banco de questões ──────────────────────────────────────────────────────────
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

QUESTOES = {
    "interpretacao": [
        {
            "ano": 2023,
            "texto": '"O mar não está para peixe", diz o adágio popular. No Brasil contemporâneo, a expressão\n'
                     'encontra eco numa realidade onde a insegurança alimentar atinge milhões. Segundo dados\n'
                     'recentes, cerca de 33 milhões de pessoas passam fome no país, ao mesmo tempo em que o\n'
                     'Brasil figura entre os maiores exportadores de alimentos do mundo. Esse paradoxo revela\n'
                     'tensões profundas entre o modelo agroexportador e as necessidades da população interna.',
            "enunciado": "Segundo o texto, qual paradoxo é apontado pelo autor?",
            "opcoes": [
                "A) O Brasil exporta peixes, mas sua população não tem acesso ao alimento.",
                "B) O país é grande exportador de alimentos, mas milhões de brasileiros passam fome.",
                "C) A insegurança alimentar é causada exclusivamente pelo modelo agroexportador.",
                "D) O adágio popular reflete com precisão a realidade econômica brasileira.",
                "E) O Brasil importa mais alimentos do que exporta, gerando fome interna."
            ],
            "gabarito": 1,
            "explicacao": "O texto afirma que o Brasil é um dos maiores exportadores de alimentos do mundo e, ao mesmo tempo, cerca de 33 milhões de pessoas passam fome — esse é o paradoxo central apontado."
        },
        {
            "ano": 2022,
            "texto": "A disciplina militar é frequentemente associada à rigidez e à obediência cega. No entanto,\n"
                     "os manuais modernos das Forças Armadas de diversos países enfatizam que a verdadeira\n"
                     "disciplina implica compreensão das ordens, não apenas sua execução mecânica. Um soldado\n"
                     "que entende o porquê de cada procedimento está mais apto a tomar decisões corretas em\n"
                     "situações imprevistas, quando a cadeia de comando pode ser interrompida.",
            "enunciado": "A ideia central do texto é que:",
            "opcoes": [
                "A) A disciplina militar exige obediência irrestrita, sem questionamentos.",
                "B) Os manuais modernos contradizem os princípios fundamentais das Forças Armadas.",
                "C) A verdadeira disciplina envolve compreensão das ordens, não apenas execução mecânica.",
                "D) O soldado deve desobedecer sempre que julgar a ordem inadequada.",
                "E) Situações imprevistas são raras no contexto militar moderno."
            ],
            "gabarito": 2,
            "explicacao": "O texto contrapõe a visão equivocada de disciplina como obediência cega à visão moderna, que enfatiza a compreensão das ordens. A ideia central está explicitamente na segunda frase."
        },
        {
            "ano": 2021,
            "texto": "A Marinha do Brasil tem papel estratégico na defesa das águas jurisdicionais brasileiras,\n"
                     "que compreendem cerca de 3,5 milhões de km², denominados 'Amazônia Azul'. Além da função\n"
                     "de defesa, a instituição contribui para pesquisas oceanográficas, apoio logístico em\n"
                     "regiões remotas e salvaguarda da vida humana no mar. Sua atuação vai muito além do aspecto\n"
                     "bélico, abrangendo dimensões científicas, humanitárias e econômicas.",
            "enunciado": "De acordo com o texto, a atuação da Marinha do Brasil:",
            "opcoes": [
                "A) Limita-se à defesa das fronteiras marítimas do país.",
                "B) Abrange apenas a pesquisa oceanográfica e o apoio logístico.",
                "C) É restrita à 'Amazônia Azul', sem outras funções.",
                "D) Envolve aspectos militares, científicos, humanitários e econômicos.",
                "E) Compete com agências civis no campo da pesquisa oceânica."
            ],
            "gabarito": 3,
            "explicacao": "O último período afirma que a atuação 'vai muito além do aspecto bélico, abrangendo dimensões científicas, humanitárias e econômicas'."
        },
        {
            "ano": 2023,
            "texto": '"Ler é voar sem sair do lugar." Essa metáfora sintetiza a potência transformadora da\n'
                     'leitura. Mais do que decodificar símbolos, ler é construir sentidos, confrontar visões\n'
                     'de mundo e ampliar horizontes cognitivos. Pesquisas indicam que leitores frequentes\n'
                     'desenvolvem maior capacidade empática e pensamento crítico mais apurado.',
            "enunciado": "No texto, a expressão 'voar sem sair do lugar' é utilizada para:",
            "opcoes": [
                "A) Criticar quem lê apenas por obrigação escolar.",
                "B) Indicar que a leitura é uma atividade passiva e contemplativa.",
                "C) Sugerir que livros tratam exclusivamente de viagens e aventuras.",
                "D) Ilustrar o potencial transformador e libertador da leitura.",
                "E) Demonstrar que a leitura substitui viagens reais."
            ],
            "gabarito": 3,
            "explicacao": "A metáfora indica que a leitura tem potencial de transformação e ampliação de horizontes sem necessidade de deslocamento físico — ela ilustra o poder libertador e transformador."
        },
        {
            "ano": 2021,
            "texto": "O relatório apontou falhas graves na manutenção dos equipamentos. Contudo, os responsáveis\n"
                     "alegaram que os recursos destinados ao setor eram insuficientes para cobrir todas as\n"
                     "demandas. A direção, por sua vez, sustentou que os investimentos haviam sido adequados e\n"
                     "que o problema residia na gestão inadequada dos recursos disponíveis.",
            "enunciado": "No texto, a palavra 'contudo' estabelece uma relação de:",
            "opcoes": [
                "A) Adição entre as informações apresentadas.",
                "B) Causa e efeito entre os fatos narrados.",
                "C) Oposição ou contraste entre as ideias.",
                "D) Conclusão com base nas premissas anteriores.",
                "E) Exemplificação do argumento inicial."
            ],
            "gabarito": 2,
            "explicacao": "'Contudo' é conjunção adversativa — introduz uma ideia que se opõe à anterior: a resposta dos responsáveis contrasta com as falhas graves apontadas."
        }
    ],
    "ortografia": [
        {
            "ano": 2023,
            "enunciado": "Assinale a alternativa em que TODAS as palavras estão grafadas corretamente:",
            "opcoes": [
                "A) privilégio, beneficiente, previlégio",
                "B) prerrogativa, beneficência, privilegio",
                "C) prerrogativa, beneficência, privilégio",
                "D) prerogativa, beneficência, privilégio",
                "E) prerrogativa, beneficiência, privilegio"
            ],
            "gabarito": 2,
            "explicacao": "'Prerrogativa' (dois r), 'beneficência' (sem i antes do ê) e 'privilégio' (acento no é) são as grafias corretas conforme o Acordo Ortográfico vigente."
        },
        {
            "ano": 2022,
            "enunciado": "De acordo com a norma ortográfica vigente, assinale a alternativa CORRETA:",
            "opcoes": [
                "A) '...portanto não há porquê reclamar da nota.'",
                "B) '...portanto não há por quê reclamar da nota.'",
                "C) '...portanto não há porque reclamar da nota.'",
                "D) '...portanto não há por que reclamar da nota.'",
                "E) '...portanto não há porquê de reclamar da nota.'"
            ],
            "gabarito": 3,
            "explicacao": "Quando 'por que' equivale a 'para que' ou indica motivo/razão, escreve-se separado e sem acento: 'não há por que reclamar' = não há motivo para reclamar."
        },
        {
            "ano": 2021,
            "enunciado": "Assinale a opção em que o uso do hífen está CORRETO:",
            "opcoes": [
                "A) anti-inflamatório, superinteressante, autoescola",
                "B) antiinflamatório, super-interessante, auto-escola",
                "C) anti-inflamatório, super-interessante, auto-escola",
                "D) antiinflamatório, superinteressante, autoescola",
                "E) anti-inflamatório, superinteressante, auto-escola"
            ],
            "gabarito": 0,
            "explicacao": "Usa-se hífen quando o prefixo termina com letra igual à inicial do segundo elemento: 'anti-inflamatório' (i+i). 'Superinteressante' e 'autoescola' não usam hífen."
        },
        {
            "ano": 2023,
            "enunciado": "Marque a alternativa em que as palavras estão corretamente acentuadas:",
            "opcoes": [
                "A) saúde, juiz, feiúra, paraíso",
                "B) saude, juíz, feiura, paraiso",
                "C) saúde, juíz, feiúra, paraíso",
                "D) saúde, juiz, feiúra, paraíso",
                "E) saúde, juiz, feiura, paraíso"
            ],
            "gabarito": 4,
            "explicacao": "'Saúde' e 'paraíso' têm hiato tônico acentuado; 'juiz' é paroxítona sem acento. 'Feiura' perdeu o acento com o Novo Acordo Ortográfico."
        }
    ],
    "morfologia": [
        {
            "ano": 2023,
            "enunciado": "Na frase 'O candidato foi aprovado com louvor', a palavra 'aprovado' é um:",
            "opcoes": [
                "A) Advérbio de modo",
                "B) Adjetivo predicativo",
                "C) Particípio com função verbal (voz passiva analítica)",
                "D) Substantivo abstrato",
                "E) Verbo no gerúndio"
            ],
            "gabarito": 2,
            "explicacao": "O particípio 'aprovado' + verbo auxiliar 'foi' forma a voz passiva analítica."
        },
        {
            "ano": 2022,
            "enunciado": "Assinale a alternativa em que a palavra destacada é um PRONOME INDEFINIDO:",
            "opcoes": [
                "A) 'Ele mesmo resolveu o problema.'",
                "B) 'Qualquer pessoa pode se inscrever.'",
                "C) 'Este é o oficial responsável.'",
                "D) 'Cujo relatório foi aprovado, o sargento foi promovido.'",
                "E) 'Quem foi convocado deve se apresentar.'"
            ],
            "gabarito": 1,
            "explicacao": "'Qualquer' é pronome indefinido — refere-se a um ser de modo vago e indeterminado."
        }
    ],
    "sintaxe": [
        {
            "ano": 2023,
            "enunciado": "Na frase 'O comandante entregou ao imediato os documentos sigilosos', o termo 'ao imediato' exerce a função de:",
            "opcoes": [
                "A) Objeto direto",
                "B) Objeto indireto",
                "C) Complemento nominal",
                "D) Adjunto adnominal",
                "E) Aposto"
            ],
            "gabarito": 1,
            "explicacao": "'Ao imediato' é objeto indireto — completa o sentido do verbo transitivo indireto 'entregar'."
        },
        {
            "ano": 2022,
            "enunciado": "Assinale a alternativa em que há sujeito indeterminado:",
            "opcoes": [
                "A) 'Chove muito em novembro na região.'",
                "B) 'Precisa-se de voluntários para a missão.'",
                "C) 'É necessário muito esforço para a aprovação.'",
                "D) 'Os candidatos foram convocados pelo edital.'",
                "E) 'Ninguém compareceu à formatura.'"
            ],
            "gabarito": 1,
            "explicacao": "Em 'Precisa-se de voluntários', o verbo transitivo indireto + 'se' indica sujeito indeterminado."
        }
    ],
    "concordancia": [
        {
            "ano": 2023,
            "enunciado": "Assinale a alternativa em que a concordância verbal está CORRETA:",
            "opcoes": [
                "A) 'Fazem dois anos que ele não aparece por aqui.'",
                "B) 'Faz dois anos que ele não aparece por aqui.'",
                "C) Ambas A e B estão corretas.",
                "D) 'Há dois anos que ele não aparece; logo, fazem dois anos.'",
                "E) 'Houveram muitos problemas durante a cerimônia.'"
            ],
            "gabarito": 1,
            "explicacao": "O verbo 'fazer' indicando tempo decorrido é impessoal e fica no singular: 'Faz dois anos'."
        }
    ],
    "regencia": [
        {
            "ano": 2023,
            "enunciado": "Assinale a alternativa em que a regência verbal está CORRETA:",
            "opcoes": [
                "A) 'Aspiramos a uma carreira militar sólida.'",
                "B) 'Aspiramos uma carreira militar sólida.'",
                "C) 'Os alunos preferiram a prova do que o trabalho.'",
                "D) 'Ele visa o cargo de comandante.'",
                "E) 'O candidato implicou com a questão difícil.'"
            ],
            "gabarito": 0,
            "explicacao": "'Aspirar' no sentido de 'almejar' é transitivo indireto: exige preposição 'a'."
        }
    ],
    "pontuacao": [
        {
            "ano": 2023,
            "enunciado": "Assinale a alternativa em que o uso da vírgula está CORRETO:",
            "opcoes": [
                "A) 'O candidato, estudou muito para a prova.'",
                "B) 'Estudou, praticou e, por fim, foi aprovado.'",
                "C) 'Chegou, viu e, venceu.'",
                "D) 'O oficial que chegou, ontem, foi promovido.'",
                "E) 'Os alunos, estavam esgotados após a prova.'"
            ],
            "gabarito": 1,
            "explicacao": "As vírgulas separam termos da enumeração e isolam 'por fim' (expressão parentética)."
        }
    ],
    "semantica": [
        {
            "ano": 2023,
            "enunciado": "'O tempo é dinheiro.' Essa figura de linguagem é um exemplo de:",
            "opcoes": [
                "A) Metonímia",
                "B) Sinestesia",
                "C) Metáfora",
                "D) Hipérbole",
                "E) Eufemismo"
            ],
            "gabarito": 2,
            "explicacao": "Metáfora é a comparação implícita entre dois termos de campos semânticos diferentes."
        }
    ]
}

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
        lista = QUESTOES[tipo].copy()
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
    
    st.markdown("### Escolha seu modo de estudo:")
    
    if st.button("🌟 Simulado Geral (15 questões aleatórias)", use_container_width=True):
        iniciar_quiz('geral', 'Simulado Geral')
        st.rerun()
        
    st.write("Ou escolha um tema específico:")
    col1, col2 = st.columns(2)
    
    for i, (tid, label) in enumerate(TEMAS):
        qtd = len(QUESTOES.get(tid, []))
        if qtd > 0: # Só mostra botão se tiver questão cadastrada
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
    
    if "texto" in q:
        st.info(q["texto"])
        
    st.markdown(f"#### {q['enunciado']}")
    
    # Formulário de resposta
    resposta_usuario = st.radio("Selecione sua resposta:", q["opcoes"], index=None, key=f"radio_{st.session_state.indice}")
    
    if not st.session_state.resposta_enviada:
        if st.button("Confirmar Resposta", type="primary"):
            if resposta_usuario:
                st.session_state.resposta_enviada = True
                st.rerun()
            else:
                st.warning("Por favor, selecione uma alternativa.")
    else:
        # Descobrir o índice da resposta escolhida para comparar com o gabarito
        idx_escolhido = q["opcoes"].index(resposta_usuario)
        correto = (idx_escolhido == q["gabarito"])
        
        if correto:
            st.success("✅ Resposta Correta!")
            if f"pontuou_{st.session_state.indice}" not in st.session_state:
                st.session_state.acertos += 1
                st.session_state[f"pontuou_{st.session_state.indice}"] = True
        else:
            gabarito_texto = q["opcoes"][q["gabarito"]]
            st.error(f"❌ Resposta Incorreta.")
            st.warning(f"O gabarito correto era: **{gabarito_texto}**")
            
        st.info(f"**Explicação:**\n{q['explicacao']}")
        
        # Salva no histórico se for a primeira vez vendo o resultado
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

# TELA 3: RESULTADOS E REVISÃO
elif st.session_state.tela == 'resultado':
    total = len(st.session_state.questoes_atuais)
    acertos = st.session_state.acertos
    pct = int((acertos / total) * 100)
    
    st.title("Desempenho Final")
    st.divider()
    
    # Exibição estilizada da nota
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Acertos", value=f"{acertos} de {total}")
    with col2:
        st.metric(label="Aproveitamento", value=f"{pct}%")
        
    if pct >= 70:
        st.success("Excelente desempenho! Continue assim, o papiro não para!")
    elif pct >= 50:
        st.warning("Você está progredindo. Revise os erros para garantir a farda.")
    else:
        st.error("Precisa focar mais na revisão teórica. Não desista!")
        
    st.markdown("### 📝 Revisão do Gabarito")
    
    # Acordeões para revisão (melhor que a tela do terminal)
    for i, h in enumerate(st.session_state.historico):
        q = h["questao"]
        icone = "✅" if h["correto"] else "❌"
        
        with st.expander(f"{icone} Questão {i+1} - {q['enunciado'][:50]}..."):
            if "texto" in q:
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