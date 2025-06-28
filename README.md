# ENEM Agent System

Sistema multi-agente inteligente para preparação para o ENEM (Exame Nacional do Ensino Médio), desenvolvido com arquitetura distribuída e IA generativa.

## 🎯 Visão Geral

Este sistema utiliza uma arquitetura de agentes especializados para fornecer uma experiência de estudo personalizada e abrangente para estudantes se preparando para o ENEM. Cada agente é responsável por uma funcionalidade específica, trabalhando em conjunto para oferecer tutoria, planejamento de estudos, questionários e correção de redações.

## 🏗️ Arquitetura

### Componentes Principais

- **Gateway API (FastAPI)**: Interface RESTful para comunicação externa
- **Agente Orquestrador**: Coordena comunicação entre agentes
- **Agentes Especializados**: Funcionalidades específicas de domínio
- **Infraestrutura**: Banco de dados, cache e busca vetorial

### Agentes Especializados

#### 🎓 Tutor Agent
- **Função**: Sistema de Q&A inteligente para dúvidas sobre matérias
- **Tecnologia**: RAG (Retrieval-Augmented Generation) com Qdrant
- **Características**:
  - Busca semântica com embeddings SentenceTransformer
  - Respostas contextualizadas usando Google Gemini Pro
  - Base de conhecimento vetorial para recuperação de informações
  - Suporte completo ao português brasileiro

#### 📅 Study Plan Agent
- **Função**: Geração de planos de estudo personalizados
- **Características**:
  - Planos flexíveis com duração customizável
  - Foco em matérias específicas ou abordagem geral
  - Cronograma diário estruturado em JSON
  - Integração com histórico do estudante

#### 🧠 Quiz Agent
- **Função**: Sistema interativo de questionários e avaliações
- **Características**:
  - Questões no formato ENEM com múltipla escolha
  - Correção automática com feedback explicativo
  - Geração de questões por matéria específica
  - Rastreamento de progresso e desempenho

#### ✍️ Essay Grader Agent
- **Função**: Correção automática de redações seguindo critérios do ENEM
- **Características**:
  - Avaliação baseada nas 5 competências oficiais do ENEM
  - Pontuação de 0-1000 seguindo escala oficial
  - Feedback detalhado por competência
  - Saída estruturada em JSON

## 🛠️ Stack Tecnológico

- **Framework de Agentes**: Agno
- **API**: FastAPI com suporte assíncrono
- **IA**: Google Gemini Pro
- **Banco Vetorial**: Qdrant
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Banco de Dados**: PostgreSQL + SQLAlchemy
- **Cache/Mensageria**: Redis (pub/sub)
- **Containerização**: Docker Compose

## 🚀 Instalação e Execução

### Pré-requisitos

- Docker e Docker Compose
- Python 3.8+
- Chave de API do Google Gemini

### Configuração

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd enem_agent_system
```

2. **Configure as variáveis de ambiente**:
```bash
# Crie um arquivo .env na raiz do projeto
GOOGLE_API_KEY=sua_chave_da_api_gemini
POSTGRES_URL=postgresql://user:password@localhost:5432/enem_db
REDIS_URL=redis://localhost:6379
QDRANT_URL=http://localhost:6333
```

3. **Inicie os serviços**:
```bash
# Suba a infraestrutura
docker-compose up -d

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python -m uvicorn app.main:app --reload
```

4. **Ingestão de dados** (opcional):
```bash
python scripts/ingest.py
```

## 📋 API Endpoints

### Chat Geral
```http
POST /api/v1/chat
Content-Type: application/json

{
  "user_id": "user123",
  "conversation_id": "conv456",
  "text": "Explique a Revolução Francesa"
}
```

### Plano de Estudos
```http
POST /api/v1/study_plan
Content-Type: application/json

{
  "user_id": "user123",
  "conversation_id": "conv456",
  "duration_days": 30,
  "focus_subjects": "matemática"
}
```

### Questionário
```http
POST /api/v1/quiz/request_question
Content-Type: application/json

{
  "user_id": "user123",
  "conversation_id": "conv456",
  "subject": "história"
}
```

### Correção de Redação
```http
POST /api/v1/essay/grade
Content-Type: application/json

{
  "user_id": "user123",
  "conversation_id": "conv456",
  "essay_text": "Texto da redação aqui..."
}
```

## 🔧 Estrutura do Projeto

```
enem_agent_system/
├── app/
│   ├── agents/              # Agentes especializados
│   │   ├── orchestrator_agent.py
│   │   ├── tutor_agent.py
│   │   ├── study_plan_agent.py
│   │   ├── quiz_agent.py
│   │   └── essay_grader_agent.py
│   ├── core/                # Configurações
│   │   └── config.py
│   ├── db/                  # Banco de dados
│   │   ├── database.py
│   │   └── models.py
│   └── main.py              # Gateway FastAPI
├── data/                    # Dados para ingestão
├── scripts/                 # Scripts utilitários
├── docker-compose.yml       # Configuração Docker
└── requirements.txt         # Dependências Python
```

## 🎯 Funcionalidades Principais

### 1. Tutoria Inteligente
- Respostas contextualizadas baseadas em RAG
- Busca semântica em base de conhecimento
- Suporte a todas as matérias do ENEM

### 2. Planejamento Personalizado
- Cronogramas adaptativos
- Foco em áreas específicas
- Progressão baseada em desempenho

### 3. Avaliação Contínua
- Questionários no formato ENEM
- Feedback imediato
- Rastreamento de progresso

### 4. Correção de Redações
- Critérios oficiais do ENEM
- Feedback detalhado por competência
- Sugestões de melhoria

## 🔄 Fluxo de Comunicação

1. **Requisição HTTP** → Gateway FastAPI
2. **Conversão para Mensagem** → Formato Agno
3. **Roteamento** → Agente Orquestrador
4. **Processamento** → Agente Especializado
5. **Resposta** → Canal Redis pub/sub
6. **Retorno** → Cliente via HTTP

## 🛡️ Segurança e Configuração

- Autenticação por chaves de API
- Validação de dados com Pydantic
- Timeouts configuráveis para operações
- Logs estruturados para monitoramento

## 📊 Monitoramento

O sistema inclui logging detalhado para:
- Rastreamento de mensagens entre agentes
- Métricas de tempo de resposta
- Erros e timeouts
- Uso de recursos

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Faça um pull request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação do Agno Framework
- Verifique os logs do sistema

---

**Desenvolvido com ❤️ para estudantes brasileiros se preparando para o ENEM**