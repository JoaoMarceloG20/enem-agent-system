# 📋 Mapeamento de Agentes - Sistema ENEM Tutor

## 🔍 Visão Geral do Sistema

O projeto **ENEM Tutor System** na branch **MVP** implementa um sistema multi-agente usando o **framework Agno** para preparação ao ENEM. O sistema é baseado em uma arquitetura modular onde cada agente tem responsabilidades específicas e utiliza o Google Gemini como modelo de IA principal.

### 📊 Arquitetura Geral
- **Framework**: Agno (Sistema multi-agente)
- **Modelo IA**: Google Gemini 1.5 Flash
- **Linguagem**: Python
- **Estrutura**: Baseada em classe `BaseENEMAgent` com especialização para diferentes domínios

---

## 🤖 Agentes Identificados

### 1. **BaseENEMAgent** (Classe Base)
📂 **Arquivo**: `app/agents/base_agent.py`

**Funcionalidade**: Classe abstrata que serve como base para todos os agentes do sistema.

**Características**:
- Integração nativa com framework Agno
- Sistema de logs e métricas
- Gerenciamento de sessões e contexto
- Health checks automatizados
- Sistema de tools integrado

**Configurações**:
```python
# Modelo IA padrão
model = settings.gemini_model  # "gemini-1.5-flash"

# Sistema de logging
logger = get_agent_logger(agent_name)

# Context management
session_context = {}
```

**Tools Disponíveis**:
- `get_session_context()` - Obter contexto da sessão
- `update_session_context()` - Atualizar contexto
- `create_session_id()` - Gerar ID único de sessão

**Métodos Abstratos**:
```python
@abstractmethod
def get_agent_type(self) -> str:
    pass

@abstractmethod
async def process_enem_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    pass
```

---

### 2. **TutorAgent** (Tutor Educacional)
📂 **Arquivo**: `app/agents/tutor_agent.py`

**Funcionalidade**: Tutor IA especializado em preparação para ENEM com capacidades de ensino adaptativo.

**Modelo Utilizado**:
- **Google Gemini 1.5 Flash**
- **Temperature**: 0.7 (balanceado para criatividade educacional)
- **Max Output Tokens**: 2048

**Matérias Suportadas**:
```python
enem_subjects = {
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

**Prompts Principais**:
```python
system_prompt = f"""
Você é um tutor especializado em preparação para o ENEM (Exame Nacional do Ensino Médio) usando o framework Agno.

**Contexto da Conversa:**
- Matéria atual: {subject_name}
- Histórico da conversa: {conversation_context}

**Suas responsabilidades:**
1. Fornecer explicações claras e didáticas sobre conteúdos do ENEM
2. Adaptar a linguagem ao nível do estudante
3. Usar exemplos práticos e contextualizados
4. Incentivar o pensamento crítico
5. Conectar conceitos entre diferentes matérias quando relevante
6. Sugerir métodos de estudo eficazes
7. Fornecer dicas específicas para o ENEM

**Diretrizes importantes:**
- Seja sempre encorajador e positivo
- Use linguagem acessível, mas precisa
- Inclua exemplos do cotidiano quando possível
- Sugira exercícios ou atividades práticas
- Conecte o conteúdo com questões reais do ENEM
- Se não souber algo, seja honesto e sugira fontes confiáveis

Pergunta do estudante: {message}
"""
```

**Tools Específicas**:
- `get_conversation_history()` - Histórico de conversas
- `get_subject_statistics()` - Estatísticas por matéria
- `suggest_study_topics()` - Sugestões de tópicos
- `explain_concept()` - Explicar conceitos específicos
- `solve_problem()` - Resolver problemas passo a passo
- `get_enem_subjects()` - Lista de matérias disponíveis
- `switch_subject_context()` - Trocar contexto de matéria
- `get_study_recommendations()` - Recomendações personalizadas

**Funcionalidades Avançadas**:
- Gerenciamento de histórico de conversas (máximo 20 mensagens)
- Análise de contexto por matéria
- Adaptação da linguagem conforme nível do estudante
- Safety settings para conteúdo educacional

---

### 3. **QuizAgent** (Gerador de Quiz)
📂 **Arquivo**: `app/agents/quiz_agent.py`

**Funcionalidade**: Geração e avaliação de quizzes estilo ENEM com análise de desempenho.

**Modelo Utilizado**:
- **Google Gemini 1.5 Flash**
- **Temperature**: 0.4 (mais determinístico para questões)
- **Max Output Tokens**: 3000

**Matérias e Tópicos**:
```python
enem_topics = {
    "matematica": [
        "Aritmética", "Álgebra", "Geometria Plana", "Geometria Espacial",
        "Trigonometria", "Estatística", "Probabilidade", "Funções",
        "Progressões", "Análise Combinatória", "Matrizes", "Logaritmos"
    ],
    "portugues": [
        "Interpretação de Texto", "Gramática", "Literatura Brasileira",
        "Figuras de Linguagem", "Sintaxe", "Semântica", "Fonética",
        "Morfologia", "Gêneros Textuais", "Variações Linguísticas"
    ],
    # ... outros tópicos
}
```

**Níveis de Dificuldade**:
```python
difficulty_levels = {
    "facil": {"description": "Fácil - Conceitos básicos", "weight": 0.3},
    "medio": {"description": "Médio - Aplicação de conceitos", "weight": 0.5},
    "dificil": {"description": "Difícil - Análise e síntese", "weight": 0.2}
}
```

**Prompt de Geração de Questões**:
```python
prompt = f"""
Você é um especialista em criar questões para o ENEM usando o framework Agno. Gere {num_questions} questões de múltipla escolha sobre {subject_name}.

**Especificações:**
- Matéria: {subject_name}
- Tópico: {topic}
- Dificuldade: {difficulty_desc}
- Número de questões: {num_questions}

**Critérios para as questões:**
1. Seguir o padrão ENEM (contextualizada, interdisciplinar quando possível)
2. Ter 5 alternativas (A, B, C, D, E)
3. Apenas uma alternativa correta
4. Incluir explicação detalhada da resposta
5. Ser adequada ao nível de dificuldade especificado
6. Abordar competências e habilidades do ENEM
"""
```

**Tools Específicas**:
- `submit_quiz_answers()` - Submeter respostas do quiz
- `get_quiz_statistics()` - Estatísticas de performance
- `get_quiz_history()` - Histórico de quizzes
- `get_enem_topics()` - Tópicos disponíveis por matéria
- `generate_custom_quiz()` - Criar quiz personalizado

**Funcionalidades**:
- Sistema de correção automática
- Análise detalhada de performance por tópico
- Recomendações de estudo baseadas em fraquezas
- Geração de questões contextualizadas
- Sistema de fallback para questões

---

### 4. **EssayGraderAgent** (Corretor de Redação)
📂 **Arquivo**: `app/agents/essay_grader_agent.py`

**Funcionalidade**: Correção automática de redações baseada nos critérios oficiais do ENEM.

**Modelo Utilizado**:
- **Google Gemini 1.5 Flash**
- **Temperature**: 0.2 (baixa para correção consistente)
- **Max Output Tokens**: 4000

**Competências ENEM**:
```python
enem_competencies = {
    "competencia_1": {
        "name": "Domínio da norma padrão da língua escrita",
        "description": "Avalia conhecimento dos mecanismos linguísticos necessários para a construção da argumentação",
        "max_score": 200,
        "criteria": [
            "Desvios de convenções da escrita",
            "Grafia, acentuação, uso de hífen, emprego de letras maiúsculas e minúsculas",
            "Separação silábica, pontuação, concordância, regência, emprego de pronomes e crase"
        ]
    },
    # ... outras competências
}
```

**Escalas de Pontuação**:
```python
score_ranges = {
    200: "Excelente - Domina plenamente a competência",
    160: "Bom - Domina bem a competência",
    120: "Regular - Domina parcialmente a competência",
    80: "Insuficiente - Domina minimamente a competência", 
    40: "Deficitário - Não domina a competência",
    0: "Nulo - Foge ao tema ou não atende ao tipo textual"
}
```

**Prompt de Correção**:
```python
prompt = f"""
Você é um avaliador especialista em redações do ENEM. Avalie a redação a seguir de acordo com as 5 competências do ENEM.

**TEMA DA REDAÇÃO:** {theme}

**REDAÇÃO A SER AVALIADA:**
{essay_text}

**CRITÉRIOS DE AVALIAÇÃO (5 Competências do ENEM):**

**COMPETÊNCIA 1 - Domínio da norma padrão da língua escrita (0-200 pontos)**
Avalie: ortografia, acentuação, pontuação, concordância, regência, emprego de pronomes, crase.

**COMPETÊNCIA 2 - Compreender a proposta e aplicar conceitos (0-200 pontos)**
Avalie: desenvolvimento do tema, aplicação de conhecimentos, tipo textual dissertativo-argumentativo.

[...continua com todas as competências...]

**INSTRUÇÕES PARA AVALIAÇÃO:**
1. Atribua uma nota de 0 a 200 para cada competência (apenas valores: 0, 40, 80, 120, 160, 200)
2. Justifique cada nota com comentários específicos
3. Identifique pontos fortes e fracos
4. Forneça sugestões de melhoria
5. Seja detalhado e construtivo no feedback
"""
```

**Temas de Exemplo**:
```python
essay_themes = [
    "Desafios da educação no Brasil",
    "Violência contra a mulher", 
    "Intolerância religiosa",
    "Democratização do acesso ao cinema",
    "Manipulação do comportamento do usuário pelo controle de dados",
    # ... outros temas
]
```

**Tools Específicas**:
- `grade_essay()` - Corrigir redação
- `get_essay_history_tool()` - Histórico de redações
- `get_essay_statistics_tool()` - Estatísticas de performance
- `suggest_essay_theme()` - Sugerir tema aleatório
- `get_writing_tips()` - Dicas de escrita
- `get_enem_competencies_tool()` - Explicar competências
- `get_essay_by_id_tool()` - Buscar redação específica

**Funcionalidades**:
- Análise completa das 5 competências ENEM
- Validação de comprimento (150-600 palavras)
- Parsing inteligente de análise IA
- Sistema de fallback para correção básica
- Análise estatística de texto (contagem de palavras, frases, parágrafos)
- Tracking de progresso histórico

---

### 5. **StudyPlanAgent** (Planos de Estudo)
📂 **Arquivo**: `app/agents/study_plan_agent.py`

**Funcionalidade**: Criação de planos de estudo personalizados e adaptativos para o ENEM.

**Modelo Utilizado**:
- **Google Gemini 1.5 Flash**
- **Temperature**: 0.3 (estruturado para planos)
- **Max Output Tokens**: 3000

**Pesos das Matérias**:
```python
subject_weights = {
    "matematica": {"hours_per_week": 8, "difficulty": "high", "weight": 0.20},
    "portugues": {"hours_per_week": 6, "difficulty": "medium", "weight": 0.15},
    "fisica": {"hours_per_week": 6, "difficulty": "high", "weight": 0.15},
    "quimica": {"hours_per_week": 6, "difficulty": "high", "weight": 0.15},
    "biologia": {"hours_per_week": 5, "difficulty": "medium", "weight": 0.10},
    "redacao": {"hours_per_week": 4, "difficulty": "medium", "weight": 0.10},
    # ... outras matérias
}
```

**Níveis de Intensidade**:
```python
intensity_levels = {
    "light": {"hours_per_day": 2, "days_per_week": 5, "description": "Ritmo leve - 2h/dia, 5 dias/semana"},
    "moderate": {"hours_per_day": 4, "days_per_week": 6, "description": "Ritmo moderado - 4h/dia, 6 dias/semana"},
    "intensive": {"hours_per_day": 6, "days_per_week": 6, "description": "Ritmo intensivo - 6h/dia, 6 dias/semana"},
    "extreme": {"hours_per_day": 8, "days_per_week": 7, "description": "Ritmo extremo - 8h/dia, 7 dias/semana"}
}
```

**Prompt de Criação de Planos**:
```python
prompt = f"""
Crie um plano de estudos personalizado para o ENEM usando o framework Agno com as seguintes especificações:

**Dados do Plano:**
- Matérias: {subjects_list}
- Duração: {duration_weeks} semanas
- Intensidade: {intensity} ({hours_per_day}h/dia, {days_per_week} dias/semana)
- Total de horas: {total_hours}h
- Data objetivo: {target_date}

**Instruções:**
1. Distribua as horas entre as matérias baseado na importância no ENEM
2. Crie uma progressão lógica de estudos (do básico ao avançado)
3. Inclua momentos para revisão e simulados
4. Sugira recursos de estudo específicos
5. Defina marcos e metas semanais
6. Considere a curva de aprendizagem de cada matéria
"""
```

**Tools Específicas**:
- `get_study_plan()` - Obter plano por ID
- `list_user_plans()` - Listar planos do usuário
- `update_plan_progress()` - Atualizar progresso
- `adapt_study_plan()` - Adaptar plano baseado em performance
- `get_weekly_schedule()` - Cronograma semanal
- `create_custom_plan()` - Criar plano personalizado
- `get_plan_analytics()` - Análises e estatísticas

**Funcionalidades**:
- Cálculo automático de distribuição de horas
- Cronogramas semanais detalhados
- Sistema de marcos e milestones
- Adaptação baseada em performance
- Analytics completos de progresso
- Múltiplos níveis de intensidade

---

### 6. **OrchestratorAgent** (Orquestrador Central)
📂 **Arquivo**: `app/agents/orchestrator_agent.py`

**Funcionalidade**: Coordenação central de todos os agentes, roteamento de mensagens e gerenciamento de sessões.

**Não usa IA diretamente** - Funciona como roteador e coordenador.

**Comandos Suportados**:
```python
commands = {
    "/help": "Show help message",
    "/status": "Show system status", 
    "/agents": "List available agents",
    "/sessions": "Show active sessions",
    "/health": "Check system health",
    "/switch <agent>": "Switch to specific agent",
    "/session new": "Create new session",
    "/session end": "End current session"
}
```

**Agentes Gerenciados**:
- tutor - Chat with AI tutor
- quiz - Generate and take quizzes  
- essay - Essay grading and feedback
- study_plan - Create study plans

**Funcionalidades**:
- Roteamento inteligente de mensagens
- Gerenciamento de sessões ativas
- Health checks de todos os agentes
- Broadcasting de mensagens
- Cleanup automático de sessões inativas
- Sistema de comandos integrado

---

## 🎯 AgentOrchestrator (Classe Utilitária)
📂 **Arquivo**: `app/agents/base_agent.py` (linhas 236-381)

**Funcionalidade**: Sistema de orquestração usando Agno MessageBus e AgentPipes.

**Características**:
```python
class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.message_bus = MessageBus()
        self.agent_pipes = {}
        self.active_sessions = {}
```

**Funcionalidades**:
- Registro/desregistro dinâmico de agentes
- Roteamento via AgentPipes
- Broadcast para múltiplos agentes
- Gerenciamento de sessões
- Health checks distribuídos
- Cleanup automático

---

## ⚙️ Configurações Globais

### 📋 Configurações do Sistema
📂 **Arquivo**: `app/core/config.py`

```python
class Settings(BaseSettings):
    # AI Configuration
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    
    # Database
    database_url: str = "sqlite:///./enem_tutor.db"
    
    # Vector Database (Qdrant)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "enem_documents"
    
    # Redis
    redis_host: str = "localhost" 
    redis_port: int = 6379
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

---

## 🔧 Framework e Dependências

### Principais Tecnologias:
- **Agno**: Framework multi-agente principal
- **Google Gemini**: Modelo de IA utilizado
- **FastAPI**: Backend API
- **SQLite**: Banco de dados principal  
- **Qdrant**: Vector database (preparado)
- **Redis**: Cache e sessões (preparado)
- **Pydantic**: Validação de dados

### Estrutura de Tools Agno:
Todos os agentes implementam tools usando o decorador `@tool()` do framework Agno:

```python
from agno.tools import tool

@tool(description="Description of the tool")
def tool_function(self, param: str) -> ReturnType:
    """Tool implementation"""
    pass
```

---

## 📊 Métricas e Logs

### Sistema de Logging:
- Logs estruturados por agente
- Métricas de performance automáticas
- Health checks periódicos
- Tracking de ações e erros

### Métricas Coletadas:
- Número de mensagens processadas
- Tempo de resposta por agente
- Erros e exceções
- Uso por matéria/tópico
- Performance de IA (tokens, tempo)

---

## 🚀 Próximos Passos para Migração

### Pontos de Atenção:
1. **Dependência do Framework Agno** - Todo o sistema está integrado com Agno
2. **Google Gemini** - Modelo IA específico usado em todos os agentes
3. **Estrutura de Tools** - Sistema de ferramentas específico do Agno
4. **Orquestração** - MessageBus e AgentPipes são específicos do framework

### Componentes para Extração:
1. **Prompts e Templates** - Todos os prompts estão bem estruturados
2. **Lógica de Negócio** - Algoritmos de correção, geração de planos, etc.
3. **Configurações de IA** - Parâmetros de temperatura, tokens, etc.
4. **Estruturas de Dados** - Matérias, tópicos, competências ENEM
5. **Tools e Funcionalidades** - Lógica específica de cada ferramenta

### Dados Estruturados Reutilizáveis:
- Matérias e tópicos do ENEM
- Competências de redação
- Escalas de pontuação
- Templates de cronogramas
- Pesos de matérias para planos de estudo
- Níveis de dificuldade e intensidade

---

**Total de Agentes Mapeados: 6 agentes principais + 1 orquestrador**
**Framework: Agno**
**Modelo IA: Google Gemini 1.5 Flash**
**Arquitetura: Multi-agente com orquestração central**