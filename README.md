# EdTech Agent API

Backend API multi-agent especializado em preparação para o ENEM (Exame Nacional do Ensino Médio). Sistema baseado no framework Agno com Google Gemini 2.5 Flash.

## Status do Projeto

**Progresso**: 83% concluído (5 de 6 agents implementados)  
**Status**: Pronto para produção  
**Última atualização**: Janeiro 2025

## Agents Disponíveis

### Operacionais (5/6)

1. **TestAgent** - Validação do sistema
   - Endpoint: `POST /api/v1/agents/test_enem/runs`
   - Função: Testes de infraestrutura

2. **TutorAgent** - Tutor educacional especializado  
   - Endpoint: `POST /api/v1/agents/tutor/runs`
   - Função: Ensino personalizado em 13 matérias ENEM
   - Parâmetros: `subject` (matematica, portugues, fisica, etc.)

3. **QuizAgent** - Gerador de quizzes ENEM
   - Endpoint: `POST /api/v1/agents/quiz/runs`  
   - Função: Geração e avaliação de questões estilo ENEM
   - Parâmetros: `subject`, `difficulty` (facil, medio, dificil)

4. **EssayGraderAgent** - Corretor de redações
   - Endpoint: `POST /api/v1/agents/essay_grader/runs`
   - Função: Correção baseada nas 5 competências ENEM
   - Features: Notas 0-200, feedback detalhado

5. **StudyPlanAgent** - Criador de planos de estudo
   - Endpoint: `POST /api/v1/agents/study_plan/runs`
   - Função: Planos personalizados com múltiplos níveis
   - Parâmetros: `intensity` (light, moderate, intensive, extreme)

### Pendente (1/6)

6. **OrchestratorAgent** - Coordenador central (opcional)

## Quick Start

### Pré-requisitos
- Docker e Docker Compose
- UV package manager
- Google API Key (Gemini)

### Instalação

```bash
# 1. Clone o repositório
git clone <repository-url>
cd edtech-agent-api

# 2. Configure as variáveis de ambiente
cp example.env .env
# Edite .env com sua GOOGLE_API_KEY

# 3. Inicie os serviços
docker-compose up -d

# 4. Verifique o status
curl http://localhost:8000/api/v1/health/
```

### Uso Básico

```bash
# Listar agents disponíveis
curl http://localhost:8000/api/v1/agents/info

# Criar um tutor de matemática
curl -X POST "http://localhost:8000/api/v1/agents/create" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "tutor", "subject": "matematica"}'

# Fazer uma pergunta ao tutor
curl -X POST "http://localhost:8000/api/v1/agents/tutor/runs" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explique funções quadráticas", "stream": false}'
```

## Arquitetura

### Stack Tecnológica
- **Framework IA**: Agno 1.4.6
- **Modelo**: Google Gemini 2.5 Flash  
- **API**: FastAPI + SQLModel
- **Banco**: PostgreSQL + Qdrant (vector database)
- **Container**: Docker + UV package manager

### Estrutura do Projeto
```
app/
├── agents/           # Agents implementados
│   ├── base_enem_agent.py    # Classe base abstrata
│   ├── tutor_agent.py        # Tutor educacional
│   ├── quiz_agent.py         # Gerador de quizzes
│   ├── essay_grader_agent.py # Corretor de redações
│   ├── study_plan_agent.py   # Planos de estudo
│   └── selector.py           # Sistema de seleção
├── api/              # Endpoints FastAPI
├── core/             # Configurações
└── main.py           # App principal
```

## API Endpoints

### Principais
- `GET /api/v1/agents/` - Listar agents
- `GET /api/v1/agents/info` - Informações detalhadas
- `POST /api/v1/agents/create` - Criar agent
- `POST /api/v1/agents/{agent_id}/runs` - Executar agent
- `GET /api/v1/health/` - Health check

### Documentação
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuração

### Variáveis de Ambiente (.env)
```bash
# API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# Database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=edtech_agents

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# API
API_PORT=8000
DEBUG=true
```

### Portas dos Serviços
- **Backend API**: 8000
- **PostgreSQL**: 5433 (local) / 5432 (container)
- **Qdrant**: 6335 (local) / 6333 (container)

## Testes

### Health Check
```bash
curl http://localhost:8000/api/v1/health/
```

### Teste de Agent
```bash
# Test Agent (sempre funcional)
curl -X POST "http://localhost:8000/api/v1/agents/test_enem/runs" \
  -H "Content-Type: application/json" \
  -d '{"message": "teste", "stream": false}'
```

## Desenvolvimento

### Comandos UV
```bash
# Instalar dependências
uv sync

# Adicionar nova dependência
uv add <package>

# Executar aplicação localmente
uv run uvicorn app.main:app --reload
```

### Docker Development
```bash
# Rebuild containers
docker-compose build --no-cache

# Ver logs
docker-compose logs backend --tail=50

# Executar comandos no container
docker-compose exec backend python -c "import app.agents.selector"
```

## Documentação Detalhada

- **Status Completo**: [`tasks/PROJECT_STATUS.md`](tasks/PROJECT_STATUS.md)
- **Roadmap Original**: [`tasks/ROADMAP_EDTECH_AGENT_API.md`](tasks/ROADMAP_EDTECH_AGENT_API.md)
- **Especificações**: [`AGENTES_MAPEAMENTO.md`](AGENTES_MAPEAMENTO.md)

## Issues Conhecidas

1. **DateTime Formatting** (Resolvido)
   - Status: Corrigido nas tools
   - Impacto: Todos os agents funcionais

2. **Docker Build Cache**
   - Workaround: Usar `docker cp` para mudanças rápidas
   - Impacto: Apenas durante desenvolvimento

## Roadmap Futuro

### Opcional/Melhorias
- [ ] OrchestratorAgent (coordenador central)
- [ ] Knowledge base com PDFs
- [ ] Authentication e autorização
- [ ] Monitoring e métricas avançadas

## Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença [MIT](LICENSE).

## Reconhecimentos

- Framework [Agno](https://github.com/agno-ai/agno) para arquitetura multi-agent
- Google Gemini 2.5 Flash para processamento de linguagem natural
- Baseado no padrão dr_ubyfol como referência de qualidade

---

**Status**: Projeto em produção com 5 agents funcionais  
**Contato**: [Seu contato aqui]