# 🧪 Guia de Testes - Edtech Agent API

Este documento descreve a estrutura de testes do projeto e como executá-los.

## 📋 Visão Geral

O projeto utiliza `pytest` como framework de testes. A suíte de testes cobre:
- **Testes Unitários**: Inicialização de agentes e funcionamento de tools.
- **Testes de Integração**: Endpoints da API e fluxo do Orchestrator.
- **Scripts de Verificação**: Scripts isolados para validação rápida.

## 📂 Estrutura de Testes

Os testes estão organizados na pasta `tests/`:

```
tests/
├── unit/                  # Testes unitários
│   ├── test_agents.py     # Inicialização e roteamento de agentes
│   ├── test_tools.py      # Funcionamento das ferramentas (mockado)
│   ├── test_quiz_agent.py # Testes legados do QuizAgent
│   └── test_tutor_agent.py# Testes legados do TutorAgent
│
├── integration/           # Testes de integração
│   ├── test_api.py        # Endpoints FastAPI (Client Test)
│   ├── test_api_integration.py      # Testes legados de integração
│   ├── test_selector_integration.py # Testes legados de seletor
│   └── test_swagger_endpoints.py    # Validação de endpoints Swagger
│
├── scripts/               # Scripts utilitários
│   ├── verify_orchestrator_mock.py  # Mock do fluxo do orquestrador
│   └── verify_tools.py              # Verificação de carregamento de tools
│
└── conftest.py            # Configurações globais e Mocks
```

## 🚀 Como Executar os Testes

Certifique-se de ter o `uv` instalado e as dependências sincronizadas (`uv sync`).

### 1. Executar Todos os Testes
Para rodar a suíte completa:
```bash
uv run pytest tests/
```

### 2. Executar por Categoria
Apenas testes unitários:
```bash
uv run pytest tests/unit/
```

Apenas testes de integração:
```bash
uv run pytest tests/integration/
```

### 3. Executar com Logs Detalhados
Para ver o output (print) durante os testes:
```bash
uv run pytest tests/ -s -v
```

## 🛠️ Mocks e Configurações (`conftest.py`)

O arquivo `tests/conftest.py` é crucial para o funcionamento dos testes. Ele realiza:
- **Mock do Banco de Dados**: Impede que os testes tentem conectar a um banco real (PostgreSQL), simulando a conexão e o driver `psycopg2`.
- **Mock do Google Gemini**: Simula as respostas da IA para evitar custos e latência.
- **Mock do Agno Storage**: Impede que o framework Agno tente criar tabelas no banco durante a inicialização dos agentes.

> **Nota**: Se você adicionar novas dependências que conectam a serviços externos, lembre-se de adicionar os mocks correspondentes no `conftest.py`.
