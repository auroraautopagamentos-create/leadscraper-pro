import streamlit as st
import pandas as pd
import json
from pathlib import Path
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
        st.write("✅ Extração real de sites e contatos de empresas")
        st.write("✅ Exportação para Excel/CSV")
        st.write("✅ Gerador de Abordagem Automática")
        
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
    st.title("Painel de Extração Real")
    
    tab_busca, tab_ia = st.tabs(["🔍 Prospecção", "✉️ Gerador de Abordagem"])
    
    with tab_busca:
        col1, col2, col3 = st.columns(3)
        with col1:
            nicho = st.selectbox("Nicho:", ["Dentistas", "Restaurantes", "Academias", "Advogados", "Clínicas", "Pet Shops"])
        with col2:
            cidade = st.text_input("Cidade/UF:", "São Paulo - SP")
        with col3:
            qtd = st.slider("Qtd Leads:", 10, 50, 20)
            
        if st.button("Iniciar Extração Real", type="primary", use_container_width=True):
            with st.spinner("Buscando empresas reais na internet..."):
                query = f"{nicho} em {cidade}"
                dados = []
                
                try:
                    # BUSCA REAL NA INTERNET
                    results = DDGS().text(query, max_results=qtd)
                    for r in results:
                        dados.append({
                            "Empresa / Site": r.get("title"),
                            "Link Real": r.get("href"),
                            "Resumo (Snippet)": r.get("body")
                        })
                except Exception as e:
                    st.error(f"Erro na busca: {e}")
                
                if dados:
                    df = pd.DataFrame(dados)
                    st.session_state['leads_gerados'] = df
                    st.success(f"✅ {len(df)} resultados REAIS encontrados!")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Baixar Planilha (Excel/CSV)", data=csv, file_name=f"leads_reais.csv", mime="text/csv")
                else:
                    st.warning("Nenhum resultado encontrado. Tente outro nicho ou cidade.")

    with tab_ia:
        st.header("Gerador de Abordagem")
        if 'leads_gerados' not in st.session_state:
            st.warning("⚠️ Extraia leads primeiro.")
        else:
            df = st.session_state['leads_gerados']
            lead_selecionado = st.selectbox("Escolha o Site:", df["Empresa / Site"].tolist())
            
            if st.button("✨ Gerar Mensagem"):
                st.text_area("Copie sua mensagem:", f"Olá, tudo bem?\n\nVi o site de vocês e percebi uma grande oportunidade de atrair mais clientes...\n\nPodemos conversar?", height=150)
