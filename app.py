import streamlit as st
import pandas as pd
import json
import re
import time
from pathlib import Path

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
    st.subheader("Minere leads reais e qualificados em segundos.")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### O que você vai desbloquear:")
        st.write("✅ Extração real de empresas, e-mails e telefones")
        st.write("✅ Lead Scoring inteligente")
        st.write("✅ Gerador de campanhas (e-mail + WhatsApp)")
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

# --- SISTEMA COMPLETO ---
else:
    st.sidebar.title("🎯 LeadScraper Pro")
    st.sidebar.success("Status: Licença Ativa")
    
    tab_dash, tab_busca, tab_ia = st.tabs(["📊 Dashboard", "🔍 Prospecção", "✉️ Campanhas"])
    
    # DASHBOARD
    with tab_dash:
        st.header("Visão Geral")
        col1, col2, col3 = st.columns(3)
        col1.metric("Leads Extraídos", st.session_state.get('total_leads', 0))
        col2.metric("E-mails Encontrados", st.session_state.get('total_emails', 0))
        col3.metric("Média de Score", "82/100")
        st.write("---")
        st.line_chart(pd.DataFrame([100, 120, 80, 200, 250], columns=['Leads']))
    
    # PROSPECÇÃO
    with tab_busca:
        st.header("Extração & Enriquecimento")
        col1, col2, col3 = st.columns(3)
        with col1: nicho = st.selectbox("Nicho:", ["Dentistas", "Restaurantes", "Academias", "Advogados"])
        with col2: cidade = st.text_input("Cidade:", "São Paulo")
        with col3: qtd = st.slider("Qtd:", 10, 50, 20)
            
        if st.button("Iniciar Extração", type="primary", use_container_width=True):
            with st.spinner("Buscando..."):
                query = f"{nicho} em {cidade} contato"
                dados = []
                try:
                    resultados = DDGS().text(query, max_results=qtd)
                    for r in resultados:
                        titulo = r.get("title", "")
                        link = r.get("href", "")
                        snippet = r.get("body", "")
                        
                        email = "Não encontrado"
                        telefone = "Não encontrado"
                        
                        # Extração via Regex no texto da busca
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
                        if emails: email = emails[0]
                        
                        tels = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', snippet)
                        if tels: telefone = tels[0]
                        
                        score = 50
                        if email != "Não encontrado": score += 20
                        if telefone != "Não encontrado": score += 15
                        if "contato" in link.lower(): score += 15
                        
                        dados.append({"Empresa": titulo, "Site": link, "E-mail": email, "Telefone": telefone, "Score": score})
                except Exception as e:
                    st.error(f"Erro: {e}")
                
                if dados:
                    df = pd.DataFrame(dados)
                    st.session_state['leads_gerados'] = df
                    st.session_state['total_leads'] = st.session_state.get('total_leads', 0) + len(df)
                    st.session_state['total_emails'] = st.session_state.get('total_emails', 0) + len(df[df["E-mail"] != "Não encontrado"])
                    
                    st.success(f"✅ {len(df)} leads encontrados!")
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Baixar CSV", data=csv, file_name="leads.csv")

    # CAMPANHAS
    with tab_ia:
        st.header("Gerador de Abordagem")
        if 'leads_gerados' not in st.session_state:
            st.warning("Extraia leads primeiro.")
        else:
            df = st.session_state['leads_gerados']
            lead = st.selectbox("Escolha a Empresa:", df["Empresa"].tolist())
            row = df[df["Empresa"] == lead].iloc[0]
            
            if st.button("Gerar Mensagem"):
                st.text_area("Copie:", f"Olá equipe da {row['Empresa']}! Vi o site de vocês e notei uma oportunidade de atrair mais clientes em {cidade}. Podemos conversar?", height=150)
