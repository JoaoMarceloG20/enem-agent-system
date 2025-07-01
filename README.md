# 📚 ENEM Tutor System

Sistema simplificado de tutoria para o ENEM com IA.

## 🚀 Instalação e Execução

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar API
Edite o arquivo `config/.env` e adicione sua chave do Gemini:
```
GEMINI_API_KEY=sua_chave_aqui
```
Obtenha em: https://makersuite.google.com/app/apikey

### 3. Executar
```bash
python start.py
```

Ou manualmente:
```bash
# Terminal 1
cd src && python api.py

# Terminal 2  
cd src && streamlit run frontend.py
```

## 🌐 Acesso
- **Interface**: http://localhost:8501
- **API**: http://localhost:8000

## 🎯 Funcionalidades
- 💬 **Chat**: Tire dúvidas com IA
- 📋 **Plano de Estudos**: Cronogramas personalizados  
- 🎯 **Quiz**: Questões do ENEM
- 📝 **Redação**: Correção automática

## 📁 Estrutura
```
enem_agent_system/
├── src/
│   ├── api.py          # Backend FastAPI
│   ├── frontend.py     # Interface Streamlit
│   └── __init__.py     # Pacote Python
├── config/
│   └── .env            # Configurações
├── start.py            # Script de inicialização
├── requirements.txt    # Dependências
└── README.md          # Documentação
```

## 🔧 Desenvolvimento
- **Backend**: FastAPI + Google Gemini
- **Frontend**: Streamlit
- **IA**: Google Gemini 1.5 Flash