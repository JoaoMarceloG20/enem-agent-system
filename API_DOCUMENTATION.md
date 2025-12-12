# Documentação da API Edtech Agent

Esta documentação fornece uma visão detalhada dos endpoints disponíveis na API, suas funcionalidades, parâmetros esperados e modelos de resposta. A API é projetada para fornecer serviços educacionais inteligentes, incluindo tutoria, geração de quizzes, correção de redações e planejamento de estudos, tudo otimizado para integração com o frontend.

## Visão Geral

A API utiliza REST e JSON para comunicação. Todas as respostas seguem um formato padrão `BaseResponse` que inclui `status` e `message`.

**Base URL**: `/api/v1`

### Status Padrão
- `success`: Operação realizada com sucesso.
- `error`: Ocorreu um erro no processamento.
- `partial`: Operação parcialmente bem-sucedida (ex: health checks parciais).

---

## Módulos

### 1. Health Checks (`/health`)
Verificação de saúde do sistema e seus componentes.

#### `GET /health/`
Verificação simples de disponibilidade.
- **Retorno**: `HealthCheckResponse` (Status: success)

#### `GET /health/detailed`
Verificação completa de todos os subsistemas (BD, VectorDB, APIs externas).
- **Retorno**: Detalhes de cada serviço e status geral.

---

### 2. Tutor Agent (`/tutor`)
Agente especializado em explicar conceitos, resolver dúvidas e fornecer orientação educacional.

#### `GET /tutor/info`
Retorna informações sobre o agente tutor.
- **Retorno**: Capacidades, matérias suportadas, configuração do modelo.

#### `GET /tutor/subjects`
Lista todas as matérias suportadas pelo sistema.
- **Retorno**: Lista de objetos com `key` (id) e `name` (nome legível) das matérias.

#### `POST /tutor/chat`
Endpoint principal para interação com o tutor.
- **Body**:
  ```json
  {
    "message": "Explique a Teoria da Relatividade",
    "subject": "fisica",
    "user_id": "user123",
    "session_id": "optional-uuid"
  }
  ```
- **Retorno**: `TutorResponse` contendo a explicação, tópicos relacionados, exemplos e sugestões de prática.

#### `GET /tutor/subjects/{subject}/tree`
Retorna a árvore de tópicos hierárquica para uma matéria.
- **Path Param**: `subject` (ex: `matematica`)
- **Retorno**: Estrutura aninhada de tópicos e subtópicos.

#### `GET /tutor/learning-path/{subject}`
Gera uma trilha de aprendizado personalizada.
- **Query Params**: `current_level` (basic, intermediate, advanced), `focus_areas` (lista).
- **Retorno**: Lista sequencial de passos para estudo.

---

### 3. Quiz Agent (`/quiz`)
Gerador e avaliador de questões estilo ENEM.

#### `GET /quiz/info`
Informações sobre o agente de quiz.
- **Retorno**: Níveis de dificuldade, matérias e capacidades.

#### `GET /quiz/topics/{subject}`
Lista tópicos disponíveis para geração de quiz em uma matéria específica.
- **Path Param**: `subject`
- **Retorno**: Lista de tópicos com metadados (dificuldade disponível, estimativa de questões).

#### `POST /quiz/generate`
Gera um quiz completo com múltiplas questões.
- **Body**:
  ```json
  {
    "subject": "matematica",
    "difficulty": "medio",
    "num_questions": 5,
    "topics": ["Geometria Plana", "Trigonometria"]
  }
  ```
- **Retorno**: `QuizGenerationResponse` contendo lista de objetos `QuizQuestion`. O conteúdo é gerado estruturado (enunciado, alternativas, gabarito, explicação).

#### `GET /quiz/quick-generate`
Gera uma única questão rápida para prática imediata.
- **Query Params**: `subject`, `difficulty`, `topic`.
- **Retorno**: Uma única `QuizQuestion`.

#### `POST /quiz/submit`
Envia respostas de um quiz para correção.
- **Body**:
  ```json
  {
    "quiz_id": "uuid-do-quiz",
    "answers": {
      "q_1": "A",
      "q_2": "C"
    }
  }
  ```
- **Retorno**: `QuizResultResponse` com nota, acertos, erros e análise de desempenho detalhada.

---

### 4. Essay Agent (`/essay`)
Corretor automático de redações com base nas competências do ENEM.

#### `GET /essay/info`
Informações sobre o corretor e critérios de avaliação.
- **Retorno**: Detalhes das 5 competências do ENEM e níveis de pontuação.

#### `GET /essay/rubric-details`
Detalhes profundos da rubrica de avaliação.
- **Retorno**: Critérios específicos para cada nível de pontuação em cada competência.

#### `POST /essay/grade`
Corrige uma redação completa.
- **Body**:
  ```json
  {
    "essay_text": "Texto da redação...",
    "theme": "Desafios da Educação",
    "student_id": "user123"
  }
  ```
- **Retorno**: `EssayGradingResponse` com nota total, nota por competência, feedback geral e sugestões de melhoria.

#### `POST /essay/grade-detailed`
Análise aprofundada da redação (linha por linha, análise estrutural).
- **Body**: Mesmo de `/grade` com flag `include_line_by_line`.
- **Retorno**: Análise linguística, estrutural e argumentativa detalhada.

#### `GET /essay/sample-essays`
Retorna exemplos de redações com notas e comentários.
- **Query Params**: `grade_level` (Excelente, Bom...), `theme`.

---

### 5. Study Plan Agent (`/study-plan`)
Criador de cronogramas de estudo personalizados.

#### `GET /study-plan/info`
Informações sobre tipos de planos e intensidades.

#### `GET /study-plan/templates`
Lista templates de planos de estudo pré-definidos (ex: Intensivo 6 meses).

#### `POST /study-plan/generate`
Gera um plano de estudos personalizado do zero.
- **Body**:
  ```json
  {
    "available_hours_per_day": 4,
    "study_days_per_week": 6,
    "target_exam_date": "2024-11-03",
    "study_intensity": "medium",
    "priority_subjects": ["matematica", "redacao"],
    "weak_subjects": ["fisica"]
  }
  ```
- **Retorno**: `StudyPlanResponse` com cronograma semanal, distribuição de horas e metas.

#### `PUT /study-plan/update-progress`
Atualiza o progresso do usuário e recalibra o plano.
- **Body**: Horas estudadas e feedback de dificuldade.
- **Retorno**: Plano ajustado e novas recomendações.

---

### 6. Orchestrator (`/orchestrator`)
Roteador inteligente de intenções.

#### `POST /orchestrator/chat`
Ponto de entrada único que decide qual agente deve responder.
- **Body**: `{"message": "Quero estudar funções do segundo grau"}`.
- **Retorno**: Resposta processada pelo agente mais adequado (neste caso, provavelmente o Tutor).

---

### 7. Agentes Genéricos (`/agents`)
Endpoints legados/genéricos para listagem e execução direta de agentes por ID.

- `GET /agents`: Lista IDs dos agentes.
- `GET /agents/info`: Informações detalhadas.
- `POST /agents/{agent_id}/runs`: Executa um agente específico diretamente.

## Modelos de Dados Principais

### QuizQuestion
```json
{
  "question_id": "string",
  "context": "string (texto de apoio)",
  "command": "string (enunciado)",
  "alternatives": {
    "A": "string",
    "B": "string",
    "C": "string",
    "D": "string",
    "E": "string"
  },
  "correct_answer": "A",
  "explanation": "string",
  "topic": "string",
  "difficulty": "facil|medio|dificil",
  "subject": "matematica|..."
}
```

### CompetencyScore (Redação)
```json
{
  "competency_id": "string",
  "name": "string",
  "score": 120,
  "max_score": 200,
  "feedback": "string",
  "strengths": ["string"],
  "improvements": ["string"]
}
```

---

## Observações para Desenvolvedores
- **Parsers**: O sistema utiliza parsers robustos (especialmente em `quiz`) para transformar saídas textuais de LLMs em JSON estruturado.
- **Mocks**: Algumas funções auxiliares (como geração de histórico de progresso ou exemplos estáticos) podem retornar dados simulados para fins de demonstração/teste se o backend de IA não estiver totalmente configurado.
- **Tratamento de Erros**: Todos os endpoints retornam códigos HTTP apropriados (200, 400, 404, 500) e um corpo JSON com `status="error"` e `message` descritiva em caso de falha.
