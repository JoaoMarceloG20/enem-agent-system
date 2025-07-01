"""
ENEM Tutor Frontend - Interface Streamlit Simplificada
"""
import streamlit as st
import requests
import uuid

# Configuração
st.set_page_config(page_title="ENEM Tutor", page_icon="📚", layout="wide")
API_URL = "http://localhost:8000"

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Função para fazer requisições
def call_api(endpoint, data):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=data, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ API não disponível. Execute: python api.py")
        return None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# Interface principal
st.title("📚 ENEM Tutor System")
st.markdown("Sistema de tutoria inteligente para o ENEM")

# Verificar API
try:
    health = requests.get(f"{API_URL}/", timeout=5)
    if health.status_code == 200:
        st.success("✅ Conectado à API")
    else:
        st.error("❌ API com problemas")
except:
    st.error("❌ Execute: `python api.py` primeiro")
    st.stop()

# Menu lateral
st.sidebar.title("Menu")
option = st.sidebar.radio("Escolha:", [
    "💬 Chat",
    "📋 Plano de Estudos", 
    "🎯 Quiz",
    "📝 Correção de Redação"
])

# Chat
if option == "💬 Chat":
    st.header("💬 Chat com Tutor")
    
    message = st.text_input("Sua pergunta:")
    
    if st.button("Enviar") and message:
        with st.spinner("Pensando..."):
            result = call_api("chat", {"message": message})
        
        if result:
            st.markdown("### 🤖 Resposta:")
            st.write(result["response"])

# Plano de Estudos
elif option == "📋 Plano de Estudos":
    st.header("📋 Plano de Estudos")
    
    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Dias:", 1, 365, 30)
    with col2:
        subject = st.selectbox("Foco:", [
            "geral", "matemática", "português", 
            "ciências naturais", "ciências humanas", "redação"
        ])
    
    if st.button("Gerar Plano"):
        with st.spinner("Criando plano..."):
            result = call_api("study-plan", {
                "duration_days": days,
                "focus_subjects": subject
            })
        
        if result:
            st.markdown("### 📋 Seu Plano:")
            st.write(result["plan"])

# Quiz
elif option == "🎯 Quiz":
    st.header("🎯 Quiz ENEM")
    
    subject = st.selectbox("Matéria:", [
        "geral", "matemática", "português", "história", 
        "geografia", "física", "química", "biologia"
    ])
    
    if st.button("Gerar Questão"):
        with st.spinner("Criando questão..."):
            result = call_api("quiz", {"subject": subject})
        
        if result:
            st.markdown("### 📝 Questão:")
            st.write(result["quiz"])

# Redação
elif option == "📝 Correção de Redação":
    st.header("📝 Correção de Redação")
    
    essay = st.text_area("Sua redação:", height=300)
    
    if st.button("Corrigir") and essay:
        with st.spinner("Corrigindo..."):
            result = call_api("essay", {"essay_text": essay})
        
        if result:
            st.markdown("### 📊 Correção:")
            st.write(result["grade"])

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown(f"**API:** {API_URL}")
st.sidebar.markdown(f"**User:** {st.session_state.user_id[:8]}...")

if __name__ == "__main__":
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__, "--server.port=8501"])