# 🏗️ Padrões de Arquitetura - Baseados no dr_ubyfol

## 📋 Estrutura do Agent dr_ubyfol (Padrão Ouro)

### Tecnologias Utilizadas
- **Framework**: Agno (agno.agent.Agent)  
- **Modelo IA**: Google Gemini 2.5 Flash
- **Vector DB**: Qdrant com FastEmbedEmbedder
- **Memory**: PostgresMemoryDb (personalização)
- **Storage**: PostgresAgentStorage (chat history)
- **Knowledge**: PDFKnowledgeBase com AgenticChunking

### Estrutura do Código
```python
# Padrão de imports
from agno.agent import Agent, AgentKnowledge
from agno.models.google import Gemini
from agno.vectordb.qdrant import Qdrant
from agno.memory.v2.memory import Memory
from agno.storage.agent.postgres import PostgresAgentStorage

# Padrão de configuração
def get_vector_db(collection_name: str):
    return Qdrant(
        collection=collection_name,
        url=f'http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}',
        embedder=FastEmbedEmbedder(),
    )

def get_knowledge() -> AgentKnowledge:
    knowledge_base = PDFKnowledgeBase(
        path=Path(__file__).parent / 'data/pdfs/documento.pdf',
        vector_db=get_vector_db(),
        reader=PDFReader(),
        chunking_strategy=AgenticChunking(model=Gemini(...))
    )
    return knowledge_base

def get_agent(model_id, user_id, session_id, debug_mode) -> Agent:
    return Agent(
        name='Agent Name',
        agent_id='agent_id',
        user_id=user_id,
        session_id=session_id,
        model=Gemini(id=model_id, api_key=settings.GOOGLE_API_KEY),
        tools=[ReasoningTools(add_instructions=True)],
        description=dedent("Description..."),
        instructions=dedent("Instructions..."),
        # Configurações importantes
        add_state_in_messages=True,
        knowledge=get_knowledge(),
        search_knowledge=True,
        storage=PostgresAgentStorage(...),
        add_history_to_messages=True,
        num_history_runs=3,
        read_chat_history=True,
        memory=Memory(...),
        enable_agentic_memory=True,
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
```

## 🔧 Configurações do Sistema (config.py)

### Padrões de Settings
```python
class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Agent API'
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Environment
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'
    
    # Database PostgreSQL
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'agent_api'
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = 'agent_api'
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))
    
    # Qdrant Vector Database
    QDRANT_HOST: str = 'localhost'
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str | None = None
    
    # Google API
    GOOGLE_API_KEY: str | None = None
```

## 🐳 Docker-compose Pattern

### Serviços Padrão
```yaml
services:
  db:
    image: postgres:17
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
    volumes:
      - app-db-data:/var/lib/postgresql/data/pgdata
    env_file: .env
    
  qdrant:
    image: qdrant/qdrant:latest
    restart: always
    volumes:
      - qdrant-data:/qdrant/storage
    ports:
      - "6333:6333"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      
  backend:
    build:
      context: .
    restart: always
    depends_on:
      db:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    env_file: .env
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/"]
```

## 📁 Estrutura de Diretórios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agents/                 # Todos os agentes
│   │   ├── __init__.py
│   │   ├── dr_ubyfol.py       # Padrão ouro
│   │   ├── base_agent.py      # Base para ENEM agents
│   │   └── data/              # PDFs e recursos
│   ├── api/                   # APIs RESTful
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── agents.py
│   │       ├── health.py
│   │       └── playground.py
│   └── core/                  # Configurações centrais
│       ├── __init__.py
│       ├── config.py
│       ├── db.py
│       └── qdrant.py
├── docker-compose.yml
├── pyproject.toml
├── example.env
└── scripts/                   # Scripts utilitários
    ├── dev.sh
    ├── format.sh
    └── entrypoint.sh
```

## 🎯 Padrões para Agentes ENEM

### Baseados no dr_ubyfol, adaptar para:

1. **BaseENEMAgent**: Classe abstrata similar ao Agent do Agno
2. **Cada Agente ENEM**: Seguir padrão get_agent() function
3. **Knowledge Base**: PDFs educacionais ENEM em data/pdfs/
4. **Prompts**: Usar dedent() para formatação
5. **Configurações**: Diferentes temperatures por agente
6. **Storage**: Mesmo padrão PostgresAgentStorage
7. **Memory**: Sistema de personalização por usuário
8. **Tools**: ReasoningTools + tools específicos por agente

### Diferenças Principais para ENEM:
- **Múltiplos Agentes**: 6 agentes vs 1 agent
- **Orquestração**: Sistema central de roteamento
- **Knowledge**: Conteúdos ENEM vs nutrição foliar
- **Tools**: Tools educacionais vs técnicas
- **Prompts**: Foco educacional vs consultoria técnica

## 🔍 Próximos Passos

1. **Reproduzir exatamente** a estrutura do dr_ubyfol
2. **Adaptar** para múltiplos agentes ENEM
3. **Manter** todas as tecnologias e padrões
4. **Adicionar** sistema de orquestração central
5. **Integrar** conhecimento educacional ENEM