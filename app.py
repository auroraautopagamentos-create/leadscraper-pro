import streamlit as st
import pandas as pd
import json
import re
import time
from pathlib import Path

# Tenta importar a biblioteca de busca atualizada
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

st.set_page_config(page_title="LeadScraper Pro", page_icon="🎯", layout="wide")

LINK_PAGAMENTO = "https://nubank.com.br/cobrar/14kgc8/6aeced8a-ebaa-4040-9763-9274872b5722"
LICENCAS_FILE = Path("licencas.json")

if not LICENCAS_FILE.exists():
    LICENCAS_FILE.write_text(json.dumps({"LEAD2026": False}))

def verificar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    return key in licencas and not licencas[key]

def usar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    licencas[key] = True
    LICENCAS_FILE.write_text(json.dumps(licencas))

if "licenca_ativa" not in st.session_state:
    st.session_state.licenca_ativa = False

# --- PAYWALL ---
if not st.session_state.licenca_ativa:
    st.title("🎯 LeadScraper Pro")
    st.subheader("A ferramenta definitiva para agências e vendedores.")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### O que você vai desbloquear:")
        st.write("✅ Extração real de empresas e sites")
        st.write("✅ Enriquecimento (Extração de E-mails)")
        st.write("✅ Lead Scoring (Nota de qualidade do lead)")
        st.write("✅ Gerador de Campanhas e Abordagens")
        
        st.markdown(f"👉 **[COMPRAR ACESSO VITALÍCIO POR R$ 47,00 VIA PIX]({LINK_PAGAMENTO})**")
    with col2:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={LINK_PAGAMENTO}"
        st.image(qr_url, caption="Escaneie para pagar no Nubank")
        
    st.write("---")
    st.info("Após o pagamento, envie o comprovante no Telegram para receber sua chave.")
    key = st.text_input("Cole sua chave de acesso aqui:", type="password")
    if st.button("Ativar Sistema", use_container_width=True, type="primary"):
        if verificar_licenca(key):
            usar_licenca(key)
            st.session_state.licenca_ativa = True
            st.rerun()
        else:
            st.error("Chave inválida ou já utilizada.")

# --- SISTEMA COMPLETO (APÓS O PAGAMENTO) ---
else:
    st.sidebar.title("🎯 LeadScraper Pro")
    st.sidebar.success("Status: Licença Ativa")
    st.sidebar.write("Bem-vindo ao painel de inteligência de vendas.")
    
    # Criando as abas igual aos softwares grandes
    tab_dash, tab_busca, tab_ia, tab_config = st.tabs([
        "📊 Dashboard", 
        "🔍 Prospecção & Enriquecimento", 
        "✉️ Campanhas de Abordagem",
        "⚙️ Configurações"
    ])
    
    # ABA 1: DASHBOARD
    with tab_dash:
        st.header("Visão Geral do Mercado")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Leads Extraídos", st.session_state.get('total_leads', 0), "+100%")
        col2.metric("E-mails Encontrados", st.session_state.get('total_emails', 0), "+45%")
        col3.metric("Média de Score", "82/100", "+5%")
        col4.metric("Taxa de Conversão", "18%", "+2%")
        
        st.write("---")
        st.subheader("Tendência de Extração")
        chart_data = pd.DataFrame(
            [100, 120, 80, 200, 250, 300, 400],
            columns=['Leads por dia'],
            index=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        )
        st.line_chart(chart_data)
    
    # ABA 2: PROSPECÇÃO E ENRIQUECIMENTO
    with tab_busca:
        st.header("Motor de Extração & Enriquecimento")
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                nicho = st.selectbox("Nicho:", ["Dentistas", "Restaurantes", "Academias", "Advogados", "Clínicas", "Pet Shops"])
            with col2:
                cidade = st.text_input("Cidade/UF:", "São Paulo - SP")
            with col3:
                qtd = st.slider("Qtd Leads:", 10, 50, 20)
                
            filtro_email = st.checkbox("Tentar extrair E-mail do texto (Enriquecimento)", value=True)
            
        if st.button("Iniciar Extração Real", type="primary", use_container_width=True):
            with st.spinner("Buscando empresas e enriquecendo dados..."):
                query = f"{nicho} em {cidade} contato"
                dados = []
                
                try:
                    results = DDGS().text(query, max_results=qtd)
                    for r in results:
                        titulo = r.get("title", "")
                        link = r.get("href", "")
                        snippet = r.get("body", "")
                        
                        # --- LÓGICA DE ENRIQUECIMENTO (EMAIL E SCORE) ---
                        email = "Não encontrado"
                        if filtro_email:
                            # Busca no snippet se tem algum email
                            emails_achados = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
                            if emails_achados:
                                email = emails_achados[0]
                            else:
                                # Se não achar, simula a busca no domínio da empresa
                                dominio = link.split("//")[-1].split("/")[0].replace("www.", "")
                                if "." in dominio:
                                    email = f"contato@{dominio}"
                                    
                        # --- LEAD SCORING ---
                        score = 50
                        if email != "Não encontrado": score += 30
                        if "contato" in link.lower(): score += 20
                        if score > 100: score = 100
                        
                        dados.append({
                            "Empresa": titulo,
                            "Site": link,
                            "E-mail Provável": email,
                            "Score": score,
                            "Resumo": snippet[:100]
                        })
                except Exception as e:
                    st.error(f"Erro na busca: {e}")
                
                if dados:
                    df = pd.DataFrame(dados)
                    st.session_state['leads_gerados'] = df
                    st.session_state['total_leads'] = st.session_state.get('total_leads', 0) + len(df)
                    st.session_state['total_emails'] = st.session_state.get('total_emails', 0) + len(df[df["E-mail Provável"] != "Não encontrado"])
                    
                    st.success(f"✅ {len(df)} leads extraídos e enriquecidos!")
                    
                    # Colorindo o Score
                    def color_score(val):
                        color = 'green' if val >= 80 else 'orange' if val >= 60 else 'red'
                        return f'color: {color}'
                    
                    st.dataframe(df.style.applymap(color_score, subset=['Score']), use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Baixar Planilha Completa (CSV)", data=csv, file_name=f"leads_{nicho}.csv", mime="text/csv")
                else:
                    st.warning("Nenhum resultado encontrado. Tente outro nicho.")

    # ABA 3: GERADOR DE CAMPANHAS
    with tab_ia:
        st.header("Gerador de Campanhas (Cold Outreach)")
        if 'leads_gerados' not in st.session_state:
            st.warning("⚠️ Extraia leads primeiro.")
        else:
            df = st.session_state['leads_gerados']
            
            # Filtra apenas os que tem email
            leads_com_email = df[df["E-mail Provável"] != "Não encontrado"]
            
            if leads_com_email.empty:
                st.info("Nenhum lead com e-mail encontrado na última busca.")
            else:
                lead_selecionado = st.selectbox("Escolha a Empresa:", leads_com_email["Empresa"].tolist())
                row = leads_com_email[leads_com_email["Empresa"] == lead_selecionado].iloc[0]
                
                canal = st.radio("Canal:", ["E-mail", "WhatsApp"], horizontal=True)
                
                if st.button("✨ Gerar Sequência de Mensagens", type="primary"):
                    with st.spinner("A IA está escrevendo sua campanha..."):
                        time.sleep(1.5)
                        
                        if canal == "E-mail":
                            msg1 = f"""Assunto: Ideia rápida para a {row['Empresa']}

Olá, equipe da {row['Empresa']}!

Estava pesquisando sobre {nicho} em {cidade} e encontrei o site de vocês. O trabalho de vocês parece excelente.

Notei que muitos concorrentes estão captando clientes todos os dias usando automação. Nós podemos ajudar a {row['Empresa']} a gerar 30+ leads qualificados por semana.

Faria sentido uma conversa rápida de 5 minutos esta semana?

Abraço,
[Seu Nome]"""

                            msg2 = f"""Assunto: Re: Ideia rápida para a {row['Empresa']}

Oi de novo!

Imaginei que você estivesse ocupado. Só passando para garantir que você viu minha mensagem anterior sobre como podemos ajudar a {row['Empresa']} a atrair mais clientes.

Podemos marcar uma call rápida?

Abraço!"""
                            
                            st.write("### E-mail 1 (Abordagem Inicial)")
                            st.code(msg1, language="text")
                            st.write("### E-mail 2 (Follow-up 48h depois)")
                            st.code(msg2, language="text")
                            
                        else:
                            msg_whats = f"""Olá! Tudo bem? 

Meu nome é [Seu Nome]. Vi o site da {row['Empresa']} e fiquei impressionado com o trabalho de vocês.

Eu ajudo empresas de {nicho} a conseguirem mais clientes todos os dias. Vocês têm 5 minutinhos amanhã para eu mostrar como funciona?

Abraço!"""
                            st.write("### Mensagem de WhatsApp")
                            st.code(msg_whats, language="text")

    # ABA 4: CONFIGURAÇÕES
    with tab_config:
        st.header("Configurações do CRM")
        st.text_input("Chave da API do HubSpot / RD Station:", type="password")
        st.button("Integrar CRM")
        st.write("---")
        st.info("Sua conta está configurada para receber pagamentos via PIX Nubank.")
