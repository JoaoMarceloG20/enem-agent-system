# EdTech Agent API

Backend FastAPI para um sistema multi‑agente focado em preparação para o ENEM. Usa Agno + Google Gemini, com PostgreSQL para histórico e Qdrant para vetores.

## Status rápido
- Progresso: 5/6 agents implementados (Orchestrator disponível em modo experimental).
- Última revisão: jan/2025.
- Pendências conhecidas: PDFs de knowledge base não estão no repositório; playground vem desativado por padrão; instalar dependências requer acesso à internet.

## Stack
- Python 3.12, FastAPI, SQLModel.
- Agno 1.4.6 com Google Gemini 2.5 Flash.
- PostgreSQL + Qdrant (docker-compose).
- Gerenciador: `uv` (recomendado) ou `pip` via venv.

## Pré-requisitos
- Python 3.12.
- Docker e Docker Compose (para serviços de infra).
- Chave `GOOGLE_API_KEY` para usar os agentes reais (testes usam mocks).

## Setup local (dev)
```bash
# 1) Ambiente
python3 -m venv .venv
. .venv/bin/activate
# ou: uv venv --python 3.12

# 2) Variáveis de ambiente
cp example.env .env
# edite GOOGLE_API_KEY e credenciais do Postgres/Qdrant conforme necessário

# 3) Dependências
UV_CACHE_DIR=.uv_cache uv sync     # exige internet
# se preferir pip:
# pip install -e .[dev]
```

## Rodar API (Docker)
```bash
docker-compose up -d  # sobe postgres (5433), qdrant (6335) e backend (8000)
curl http://localhost:8000/api/v1/health/
```

## Rodar API local (sem Docker para app)
Suba Postgres e Qdrant (via docker-compose ou externos), depois:
```bash
. .venv/bin/activate
uv run uvicorn app.main:app --reload
```

## Testes
Os testes usam mocks para não depender de serviços externos.
```bash
. .venv/bin/activate
uv run pytest tests/unit tests/integration
```

## Agents e endpoints principais
- `test_enem`: POST `/api/v1/agents/test_enem/runs`
- `tutor`: POST `/api/v1/agents/tutor/runs`
- `quiz`: POST `/api/v1/agents/quiz/runs`
- `essay_grader`: POST `/api/v1/agents/essay_grader/runs`
- `study_plan`: POST `/api/v1/agents/study_plan/runs`
- `orchestrator` (experimental): POST `/api/v1/orchestrator/chat`
- Listagem e metadados: `GET /api/v1/agents`, `/api/v1/agents/info`
- Health: `GET /api/v1/health/`, `/api/v1/health/detailed`

## Playground
- Desativado por padrão para evitar criar agentes que exigem DB/Qdrant/Gemini.
- Para habilitar (assumindo serviços rodando e keys definidas): exporte `ENABLE_PLAYGROUND=true` antes de iniciar a API.

## Notas sobre knowledge base
- `app/agents/knowledge.py` espera PDFs em `app/agents/data/pdfs/` (ex.: `enem-geral.pdf`); os arquivos não acompanham o repo.
- Sem os PDFs, os agentes funcionam, mas sem pesquisa em base vetorial.

## Scripts úteis
- `scripts/dev.sh`: inicialização rápida de dev.
- `scripts/format.sh`: formatação (ruff/black se configurados).
- `scripts/validate.sh`: pipeline de validação.

## Licença
MIT.
