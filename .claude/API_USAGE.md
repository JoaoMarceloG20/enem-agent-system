# 🚀 API Usage Guide - ENEM Agents

## Visão Geral

A API do **ENEM Tutor System** oferece acesso a 3 agentes especializados para preparação ao ENEM via endpoints REST.

**Base URL**: `http://localhost:8000/api/v1`

---

## 🤖 Agents Disponíveis

### 1. **TestAgent** (`test_enem`)
- **Propósito**: Validação e teste do sistema
- **Temperature**: 0.5
- **Max Tokens**: 1024
- **Parâmetros especiais**: Nenhum

### 2. **TutorAgent** (`tutor`)
- **Propósito**: Tutor educacional para preparação ENEM
- **Temperature**: 0.7 (balanceada para ensino)
- **Max Tokens**: 2048
- **Parâmetros especiais**: `subject` (opcional)

### 3. **QuizAgent** (`quiz`)
- **Propósito**: Geração e avaliação de quizzes ENEM
- **Temperature**: 0.4 (determinística para questões)
- **Max Tokens**: 3000
- **Parâmetros especiais**: `subject`, `difficulty`

---

## 📊 Endpoints Informativos

### Listar Agents Disponíveis
```http
GET /agents
```

**Response:**
```json
["test_enem", "tutor", "quiz"]
```

### Informações Detalhadas dos Agents
```http
GET /agents/info
```

**Response:**
```json
{
  "test_enem": {
    "name": "Test ENEM Agent",
    "description": "Agent de teste para validação do sistema ENEM",
    "supports_subject": false,
    "supports_difficulty": false,
    "temperature": 0.5,
    "max_tokens": 1024
  },
  "tutor": {
    "name": "Tutor ENEM",
    "description": "Tutor educacional especializado em preparação para ENEM",
    "supports_subject": true,
    "supports_difficulty": false,
    "temperature": 0.7,
    "max_tokens": 2048,
    "subjects": ["matematica", "portugues", "literatura", ...]
  },
  "quiz": {
    "name": "Quiz ENEM",
    "description": "Gerador e avaliador de quizzes estilo ENEM",
    "supports_subject": true,
    "supports_difficulty": true,
    "temperature": 0.4,
    "max_tokens": 3000,
    "subjects": ["matematica", "portugues", "literatura", ...],
    "difficulties": ["facil", "medio", "dificil"]
  }
}
```

### Matérias ENEM Suportadas
```http
GET /agents/subjects
```

**Response:**
```json
{
  "matematica": "Matemática e suas Tecnologias",
  "portugues": "Linguagens, Códigos e suas Tecnologias - Português",
  "literatura": "Linguagens, Códigos e suas Tecnologias - Literatura",
  "ingles": "Linguagens, Códigos e suas Tecnologias - Inglês",
  "espanhol": "Linguagens, Códigos e suas Tecnologias - Espanhol",
  "fisica": "Ciências da Natureza e suas Tecnologias - Física",
  "quimica": "Ciências da Natureza e suas Tecnologias - Química",
  "biologia": "Ciências da Natureza e suas Tecnologias - Biologia",
  "historia": "Ciências Humanas e suas Tecnologias - História",
  "geografia": "Ciências Humanas e suas Tecnologias - Geografia",
  "filosofia": "Ciências Humanas e suas Tecnologias - Filosofia",
  "sociologia": "Ciências Humanas e suas Tecnologias - Sociologia",
  "redacao": "Redação"
}
```

### Tópicos de Quiz por Matéria
```http
GET /agents/quiz/topics
```

**Response:**
```json
{
  "matematica": [
    "Aritmética", "Álgebra", "Geometria Plana", "Geometria Espacial",
    "Trigonometria", "Estatística", "Probabilidade", "Funções",
    "Progressões", "Análise Combinatória", "Matrizes", "Logaritmos"
  ],
  "fisica": [
    "Mecânica", "Termologia", "Ondulatória", "Óptica",
    "Eletricidade", "Magnetismo", "Física Moderna"
  ]
  // ... outras matérias
}
```

### Níveis de Dificuldade do Quiz
```http
GET /agents/quiz/difficulties
```

**Response:**
```json
{
  "facil": {
    "description": "Fácil - Conceitos básicos",
    "weight": 0.3
  },
  "medio": {
    "description": "Médio - Aplicação de conceitos",
    "weight": 0.5
  },
  "dificil": {
    "description": "Difícil - Análise e síntese",
    "weight": 0.2
  }
}
```

---

## 🏭 Criação de Agent Instances

### Criar Agent Instance
```http
POST /agents/create
Content-Type: application/json
```

**Body:**
```json
{
  "agent_id": "tutor",
  "model": "gemini-2.5-flash",
  "user_id": "student123",
  "session_id": "session456",
  "subject": "matematica"
}
```

**Response:**
```json
{
  "agent_id": "tutor",
  "name": "Tutor ENEM - Matemática e suas Tecnologias",
  "agent_name": "tutor_matematica",
  "model": "gemini-2.5-flash",
  "user_id": "student123",
  "session_id": "session456",
  "subject": "matematica",
  "difficulty": null,
  "created": true
}
```

### Exemplos de Criação

#### TestAgent (Validação)
```json
{
  "agent_id": "test_enem",
  "user_id": "test_user",
  "session_id": "test_session"
}
```

#### TutorAgent Geral
```json
{
  "agent_id": "tutor",
  "user_id": "student123",
  "session_id": "math_session"
}
```

#### TutorAgent para Física
```json
{
  "agent_id": "tutor", 
  "subject": "fisica",
  "user_id": "student123",
  "session_id": "physics_session"
}
```

#### QuizAgent Médio (Geral)
```json
{
  "agent_id": "quiz",
  "difficulty": "medio",
  "user_id": "student123",
  "session_id": "quiz_session"
}
```

#### QuizAgent Matemática Difícil
```json
{
  "agent_id": "quiz",
  "subject": "matematica",
  "difficulty": "dificil", 
  "user_id": "student123",
  "session_id": "math_hard_quiz"
}
```

---

## 💬 Interação com Agents

### Enviar Mensagem para Agent
```http
POST /agents/{agent_id}/runs
Content-Type: application/json
```

**Body:**
```json
{
  "message": "Explique o teorema de Pitágoras",
  "stream": false,
  "model": "gemini-2.5-flash",
  "user_id": "student123",
  "session_id": "math_session",
  "subject": "matematica"
}
```

**Response (stream=false):**
```
Texto da resposta do agent...
```

**Response (stream=true):**
```
Content-Type: text/event-stream
[Chunks de texto em streaming]
```

### Exemplos de Interação

#### TutorAgent - Explicação de Conceito
```bash
curl -X POST "http://localhost:8000/api/v1/agents/tutor/runs" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Como resolver uma equação do segundo grau?",
    "stream": false,
    "user_id": "student123", 
    "session_id": "math_session",
    "subject": "matematica"
  }'
```

#### QuizAgent - Gerar Quiz
```bash
curl -X POST "http://localhost:8000/api/v1/agents/quiz/runs" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Crie um quiz de 3 questões sobre cinemática",
    "stream": false,
    "user_id": "student123",
    "session_id": "physics_quiz",
    "subject": "fisica",
    "difficulty": "medio"
  }'
```

#### TestAgent - Verificação do Sistema
```bash
curl -X POST "http://localhost:8000/api/v1/agents/test_enem/runs" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "O sistema está funcionando?",
    "stream": false,
    "user_id": "test_user",
    "session_id": "test_session"
  }'
```

---

## 🏥 Health Checks

### Health Check Básico
```http
GET /health/
```

### Health Check Detalhado
```http
GET /health/detailed
```

### Health Check do Sistema
```http
GET /health/system
```

### Health Check dos Agents
```http
GET /health/agents
```

**Response:**
```json
{
  "total_agents": 3,
  "healthy_agents": 3,
  "health_percentage": 100.0,
  "agents": {
    "test_enem": {
      "agent_type": "test_enem",
      "agent_name": "Test ENEM Agent",
      "google_api_key": true,
      "database": true,
      "qdrant": true,
      "healthy": true
    },
    "tutor": {
      "agent_type": "tutor",
      "agent_name": "Tutor ENEM - Todas as Matérias", 
      "healthy": true
    },
    "quiz": {
      "agent_type": "quiz_medio",
      "agent_name": "Quiz ENEM - Todas as Matérias (Médio)",
      "healthy": true
    }
  }
}
```

---

## 🎮 Playground

### Acesso ao Playground Agno
```http
GET /
```

Interface visual para testar agents interativamente.

---

## ⚠️ Configuração Necessária

### Google API Key
Para funcionamento completo, configure uma chave válida do Google Gemini:

```bash
# .env
GOOGLE_API_KEY="your_actual_google_gemini_api_key_here"
```

### Docker Services
Para funcionalidade completa (storage e knowledge):

```bash
# Subir PostgreSQL e Qdrant
docker-compose up -d db qdrant
```

---

## 📝 Exemplos de Uso Completo

### 1. Sistema de Tutoria Personalizada

```javascript
// 1. Criar tutor para matemática
const tutorResponse = await fetch('/api/v1/agents/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    agent_id: 'tutor',
    subject: 'matematica',
    user_id: 'student_123',
    session_id: 'math_study_session'
  })
});

// 2. Interagir com o tutor
const interactionResponse = await fetch('/api/v1/agents/tutor/runs', {
  method: 'POST', 
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Não entendo logaritmos, pode me explicar?',
    stream: false,
    user_id: 'student_123',
    session_id: 'math_study_session',
    subject: 'matematica'
  })
});
```

### 2. Sistema de Quiz Adaptativo

```python
import requests

# 1. Descobrir tópicos disponíveis
topics_response = requests.get('http://localhost:8000/api/v1/agents/quiz/topics')
physics_topics = topics_response.json()['fisica']

# 2. Criar quiz de física difícil
quiz_agent = requests.post('http://localhost:8000/api/v1/agents/create', json={
    'agent_id': 'quiz',
    'subject': 'fisica', 
    'difficulty': 'dificil',
    'user_id': 'student_123',
    'session_id': 'physics_challenge'
})

# 3. Gerar questões
quiz_response = requests.post('http://localhost:8000/api/v1/agents/quiz/runs', json={
    'message': f'Crie 5 questões sobre {physics_topics[0]}',
    'stream': False,
    'user_id': 'student_123',
    'session_id': 'physics_challenge',
    'subject': 'fisica',
    'difficulty': 'dificil'
})
```

### 3. Monitoramento do Sistema

```bash
# Verificar status geral
curl http://localhost:8000/api/v1/health/detailed

# Verificar agents específicos  
curl http://localhost:8000/api/v1/health/agents

# Listar capacidades
curl http://localhost:8000/api/v1/agents/info
```

---

## 🚀 Resumo das Capacidades

- ✅ **3 Agents especializados** (Test, Tutor, Quiz)
- ✅ **13 matérias ENEM** suportadas
- ✅ **99 tópicos mapeados** para quiz
- ✅ **3 níveis de dificuldade** (fácil, médio, difícil)
- ✅ **Context switching** por matéria e dificuldade
- ✅ **Streaming e não-streaming** suportado
- ✅ **Health monitoring** completo
- ✅ **Playground interativo** disponível
- ✅ **APIs REST** totalmente funcionais