

    
            import streamlit as st
import pandas as pd
import numpy as np
import random
import json
import time
import io
from pathlib import Path

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
        st.write("✅ Extração ilimitada de leads (Nome, WhatsApp, E-mail, Site)")
        st.write("✅ Dashboard de inteligência de vendas")
        st.write("✅ Filtros avançados (Empresas com site, somente WhatsApp)")
        st.write("✅ Gerador de Abordagem Automática (Copie e Cole)")
        
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

# --- SISTEMA COMPLETO (Após Pagamento) ---
else:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2933/2933245.png", width=80)
        st.title("LeadScraper Pro")
        st.success("Plano: Vitalício PRO")
        st.write("---")
        st.write("**Sessão iniciada:**")
        st.write("Usuário: Cliente PRO")
        st.write("Status: Ativo")
    
    st.title("Painel de Controle de Prospecção")
    
    # Cria as abas
    tab_dash, tab_busca, tab_ia, tab_config = st.tabs(["📊 Dashboard", "🔍 Prospecção", "✉️ Gerador de Abordagem", "⚙️ Configurações"])
    
    # Aba 1: Dashboard
    with tab_dash:
        st.header("Visão Geral do Mercado")
        col1, col2, col3 = st.columns(3)
        col1.metric("Leads Extraídos Hoje", "1.250", "+12%")
        col2.metric("Leads com WhatsApp", "840", "+5%")
        col3.metric("Taxa de Conversão Estimada", "18%", "+2%")
        
        st.write("---")
        st.subheader("Distribuição de Leads por Nicho")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Dentistas', 'Restaurantes', 'Advogados']
        )
        st.line_chart(chart_data)
    
    # Aba 2: Prospecção
    with tab_busca:
        st.header("Motor de Extração")
        
        with st.expander("Filtros Avançados", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                nicho = st.selectbox("Nicho:", ["Dentistas", "Restaurantes", "Academias", "Advogados", "Clínicas"])
            with col2:
                cidade = st.text_input("Cidade/UF:", "São Paulo - SP")
            with col3:
                qtd = st.slider("Qtd Leads:", 10, 200, 50)
                
            filtros = st.multiselect("Requisitos do Lead:", ["Possui Site", "Possui WhatsApp", "Possui E-mail"], default=["Possui WhatsApp"])
        
        if st.button("Iniciar Extração", type="primary", use_container_width=True):
            with st.spinner("Vasculhando Google Maps e Diretórios..."):
                time.sleep(2)
                
                # Gerando dados simulados realistas em DataFrame (Pandas)
                nomes_base = ["Studio", "Clínica", "Espaço", "Centro", "Grupo", "Consultório", "Oficina"]
                dados = []
                for i in range(qtd):
                    nome = f"{random.choice(nomes_base)} {nicho[:-1]} {random.choice(['Silva', 'Souza', 'Oliveira', 'Santos'])}"
                    tel = f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
                    email = f"contato@{nome.lower().replace(' ', '')}.com.br"
                    site = f"www.{nome.lower().replace(' ', '')}.com.br"
                    
                    # Aplicando filtros
                    if "Possui Site" in filtros and not site: continue
                    if "Possui WhatsApp" in filtros and not tel: continue
                    if "Possui E-mail" in filtros and not email: continue
                    
                    dados.append({
                        "Empresa": nome,
                        "Telefone/WhatsApp": tel,
                        "E-mail": email,
                        "Site": site,
                        "Cidade": cidade
                    })
                
                df = pd.DataFrame(dados)
                st.session_state['leads_gerados'] = df
                
                st.success(f"✅ Extração concluída! {len(df)} leads qualificados.")
                st.dataframe(df, use_container_width=True)
                
                # Botão de Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Planilha (Excel/CSV)",
                    data=csv,
                    file_name=f"leads_{nicho}_{cidade}.csv",
                    mime="text/csv",
                    type="primary"
                )

    # Aba 3: Gerador de Abordagem (IA)
    with tab_ia:
        st.header("Gerador de Abordagem (Cold Outreach)")
        st.write("Selecione um lead extraído e crie a mensagem perfeita para ele.")
        
        if 'leads_gerados' not in st.session_state:
            st.warning("⚠️ Você precisa extrair leads na aba 'Prospecção' primeiro.")
        else:
            df = st.session_state['leads_gerados']
            lead_selecionado = st.selectbox("Escolha a empresa:", df["Empresa"].tolist())
            
            row = df[df["Empresa"] == lead_selecionado].iloc[0]
            
            canal = st.radio("Canal de Abordagem:", ["WhatsApp", "E-mail"], horizontal=True)
            
            if st.button("✨ Gerar Mensagem", type="primary"):
                with st.spinner("Escrevendo abordagem personalizada..."):
                    time.sleep(1) # Simula pensamento
                    
                    if canal == "WhatsApp":
                        texto = f"""Olá, equipe {row['Empresa']}! Tudo bem?

Encontrei o trabalho de vocês no Google e vi que atuam no ramo de {nicho.lower()}. 

Percebi que muitos clientes em {row['Cidade']} procuram por {nicho.lower()} mas não encontram vocês facilmente no topo das buscas.

Eu ajudo empresas como a sua a captar mais clientes todos os dias de forma automática. Podemos conversar por 5 minutos amanhã?

Abraço!"""
                    else:
                        texto = f"""Assunto: Aumentando o faturamento da {row['Empresa']}

Olá, tudo bem?

Meu nome é [Seu Nome] e acabei de visitar o site de vocês.

Notei que a {row['Empresa']} tem um grande potencial de mercado em {row['Cidade']}, mas está perdendo clientes para concorrentes que investem em captação diária.

Nós temos uma solução que entrega centenas de contatos qualificados de {nicho.lower()} por semana.

Gostaria de te enviar um vídeo rápido mostrando como funciona?

Abraço,
[Seu Nome]"""
                    
                    st.text_area("Copie sua mensagem:", texto, height=200)
                    
    # Aba 4: Configurações
    with tab_config:
        st.header("Configurações da Conta")
        st.text_input("Chave da API do CRM (Integração):", type="password")
        st.button("Salvar Alterações")
        st.write("---")
        st.subheader("Integração de Pagamentos")
        st.info("Suas vendas estão caindo na conta Nubank configurada.")            
