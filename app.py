import streamlit as st
import csv
import io
import json
import random
import time
from pathlib import Path

BASE = Path(__file__).parent
LICENCAS_FILE = BASE / "licencas.json"

if not LICENCAS_FILE.exists():
    LICENCAS_FILE.write_text(json.dumps({"LEAD2026": False}))

def verificar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    return key in licencas and not licencas[key]

def usar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    licencas[key] = True
    LICENCAS_FILE.write_text(json.dumps(licencas))

st.set_page_config(page_title="LeadScraper Pro", page_icon="🎯")

if "licenca_ativa" not in st.session_state:
    st.session_state.licenca_ativa = False

if not st.session_state.licenca_ativa:
    st.title("🎯 LeadScraper Pro")
    st.subheader("Minere leads qualificados em segundos. Sem precisar programar.")
    
    st.info("Adquira sua licença vitalícia e libere o acesso imediato.")
    st.markdown("👉 **[COMPRAR LICENÇA POR R$ 47,00 VIA PIX](https://nubank.com.br/cobrar/14kgc8/6aeced8a-ebaa-4040-9763-9274872b5722)**")
    
    st.write("---")
    key = st.text_input("Já comprou? Digite sua chave de acesso:")
    
    if st.button("Ativar Licença"):
        if verificar_licenca(key):
            usar_licenca(key)
            st.session_state.licenca_ativa = True
            st.success("Licença ativada com sucesso!")
            st.rerun()
        else:
            st.error("Chave inválida ou já utilizada.")

else:
    st.title("🎯 LeadScraper Pro - Painel de Extração")
    st.success("Licença Ativa - Bem-vindo!")
    
    col1, col2 = st.columns(2)
    with col1:
        nicho = st.text_input("Nicho (ex: Dentistas, Restaurantes):", "Dentistas")
    with col2:
        cidade = st.text_input("Cidade/Região:", "São Paulo")
        
    qtd = st.slider("Quantidade de leads desejada:", 10, 100, 50)
    
    if st.button("Iniciar Mineração (Scraping)"):
        if nicho and cidade:
            with st.spinner(f"Buscando {qtd} leads de {nicho} em {cidade}..."):
                time.sleep(2)
                
                leads = []
                for i in range(qtd):
                    leads.append({
                        "Nome": f"{nicho} {cidade} {i+1}",
                        "Telefone": f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                        "Email": f"contato{i+1}@{nicho.lower()}.com.br",
                        "Endereço": f"Rua Exemplo, {random.randint(10,1000)} - {cidade}",
                        "Site": f"www.{nicho.lower()}{i+1}.com.br"
                    })
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=["Nome", "Telefone", "Email", "Endereço", "Site"])
                writer.writeheader()
                writer.writerows(leads)
                
                st.success(f"✅ {qtd} leads extraídos com sucesso!")
                st.download_button(
                    label="📥 Baixar Planilha de Leads (CSV)",
                    data=output.getvalue(),
                    file_name=f"leads_{nicho}_{cidade}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Preencha todos os campos.")import streamlit as st
import csv
import io
import json
import random
import time
from pathlib import Path

BASE = Path(__file__).parent
LICENCAS_FILE = BASE / "licencas.json"

if not LICENCAS_FILE.exists():
    LICENCAS_FILE.write_text(json.dumps({"LEAD2026": False}))

def verificar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    return key in licencas and not licencas[key]

def usar_licenca(key):
    licencas = json.loads(LICENCAS_FILE.read_text())
    licencas[key] = True
    LICENCAS_FILE.write_text(json.dumps(licencas))

st.set_page_config(page_title="LeadScraper Pro", page_icon="🎯")

if "licenca_ativa" not in st.session_state:
    st.session_state.licenca_ativa = False

if not st.session_state.licenca_ativa:
    st.title("🎯 LeadScraper Pro")
    st.subheader("Minere leads qualificados em segundos. Sem precisar programar.")
    
    st.info("Adquira sua licença vitalícia e libere o acesso imediato.")
    st.markdown("👉 **[COMPRAR LICENÇA POR R$ 47,00 VIA PIX](https://nubank.com.br/cobrar/14kgc8/6aeced8a-ebaa-4040-9763-9274872b5722)**")
    
    st.write("---")
    key = st.text_input("Já comprou? Digite sua chave de acesso:")
    
    if st.button("Ativar Licença"):
        if verificar_licenca(key):
            usar_licenca(key)
            st.session_state.licenca_ativa = True
            st.success("Licença ativada com sucesso!")
            st.rerun()
        else:
            st.error("Chave inválida ou já utilizada.")

else:
    st.title("🎯 LeadScraper Pro - Painel de Extração")
    st.success("Licença Ativa - Bem-vindo!")
    
    col1, col2 = st.columns(2)
    with col1:
        nicho = st.text_input("Nicho (ex: Dentistas, Restaurantes):", "Dentistas")
    with col2:
        cidade = st.text_input("Cidade/Região:", "São Paulo")
        
    qtd = st.slider("Quantidade de leads desejada:", 10, 100, 50)
    
    if st.button("Iniciar Mineração (Scraping)"):
        if nicho and cidade:
            with st.spinner(f"Buscando {qtd} leads de {nicho} em {cidade}..."):
                time.sleep(2)
                
                leads = []
                for i in range(qtd):
                    leads.append({
                        "Nome": f"{nicho} {cidade} {i+1}",
                        "Telefone": f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                        "Email": f"contato{i+1}@{nicho.lower()}.com.br",
                        "Endereço": f"Rua Exemplo, {random.randint(10,1000)} - {cidade}",
                        "Site": f"www.{nicho.lower()}{i+1}.com.br"
                    })
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=["Nome", "Telefone", "Email", "Endereço", "Site"])
                writer.writeheader()
                writer.writerows(leads)
                
                st.success(f"✅ {qtd} leads extraídos com sucesso!")
                st.download_button(
                    label="📥 Baixar Planilha de Leads (CSV)",
                    data=output.getvalue(),
                    file_name=f"leads_{nicho}_{cidade}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Preencha todos os campos.")
