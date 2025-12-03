# Exemplos de uso das rotas da API

Base das URLs: defina `BASE_URL="http://localhost:8000/api/v1"`. Para chamadas
que enviam corpo, use `-H "Content-Type: application/json"`.
Respostas baseadas em `BaseResponse` trazem sempre `status`, `message` e
`timestamp`; os exemplos omitiram `timestamp` e ids longos com `...` para ficar
mais curto.

## Health
- `GET $BASE_URL/health/`
  ```bash
  curl "$BASE_URL/health/"
  # => {"status":"success","message":"Edtech Agent API is running"}
  ```
- `GET $BASE_URL/health/detailed`
  ```bash
  curl "$BASE_URL/health/detailed"
  # => {"status":"success","message":"Detailed health check completed","services":{"overall_status":"healthy","components":{"database":{"status":"healthy"},"qdrant":{"status":"healthy"},"google_api":{"status":"unhealthy"}},"system_info":{"project_name":"Edtech Agent API","environment":"local","api_version":"/api/v1"},"total_agents":5,"healthy_agents":5,"agents":{"tutor":{"healthy":true},"quiz":{"healthy":true}},"health_percentage":100.0},"version":"1.0.0"}
  ```
- `GET $BASE_URL/health/system`
  ```bash
  curl "$BASE_URL/health/system"
  # => {"status":"partial","message":"System health check completed","services":{"overall_status":"unhealthy","components":{"database":{"status":"healthy"},"qdrant":{"status":"unhealthy"},"google_api":{"status":"healthy"}},"system_info":{"project_name":"Edtech Agent API","environment":"local","api_version":"/api/v1"}}}
  ```
- `GET $BASE_URL/health/agents`
  ```bash
  curl "$BASE_URL/health/agents"
  # => {"status":"success","message":"Agents health check completed","services":{"total_agents":5,"healthy_agents":4,"agents":{"tutor":{"healthy":true},"quiz":{"healthy":true},"essay_grader":{"healthy":true},"study_plan":{"healthy":false}},"health_percentage":80.0}}
  ```

## Agents (legacy)
- `GET $BASE_URL/agents`
  ```bash
  curl "$BASE_URL/agents"
  # => {"status":"success","message":"Agents retrieved successfully","agents":["tutor","quiz","essay_grader","study_plan"],"total_count":4}
  ```
- `GET $BASE_URL/agents/info`
  ```bash
  curl "$BASE_URL/agents/info"
  # => {"status":"success","message":"Agent information retrieved successfully","agents":{"tutor":{"name":"Tutor ENEM","supports_subject":true,...}}}
  ```
- `GET $BASE_URL/agents/subjects`
  ```bash
  curl "$BASE_URL/agents/subjects"
  # => {"status":"success","message":"Subjects retrieved successfully","subjects":[{"key":"matematica","name":"Matematica"}]}
  ```
- `GET $BASE_URL/agents/quiz/topics?subject=matematica`
  ```bash
  curl "$BASE_URL/agents/quiz/topics?subject=matematica"
  # => {"status":"success","message":"Topics for matematica retrieved successfully","subject":"matematica","topics":["funcoes","estatistica", "..."]}
  ```
- `GET $BASE_URL/agents/quiz/difficulties`
  ```bash
  curl "$BASE_URL/agents/quiz/difficulties"
  # => {"status":"success","message":"Difficulties retrieved successfully","difficulties":[{"key":"facil","description":"Basico"}]}
  ```
- `GET $BASE_URL/agents/study/intensities`
  ```bash
  curl "$BASE_URL/agents/study/intensities"
  # => {"status":"success","message":"Study intensities retrieved successfully","intensities":[{"key":"light","description":"Plano leve"}]}
  ```
- `POST $BASE_URL/agents/create`
  ```bash
  curl -X POST "$BASE_URL/agents/create" \
    -H "Content-Type: application/json" \
    -d '{"agent_id":"tutor","subject":"matematica","user_id":"user-123","debug_mode":false}'
  # => {"status":"success","message":"Agent 'tutor' created successfully","agent_id":"tutor","agent_name":"Tutor ENEM","session_id":"...","configuration":{"agent_id":"tutor","model":"gemini-2.5-flash","subject":"matematica"}}
  ```
- `POST $BASE_URL/agents/{agent_id}/runs`
  (agent_id aceito: tutor, quiz, essay_grader, study_plan, test_enem)
  ```bash
  curl -X POST "$BASE_URL/agents/tutor/runs?subject=matematica" \
    -H "Content-Type: application/json" \
    -d '{"message":"Explique a formula de Bhaskara","session_id":"sess-1"}'
  # => {"status":"success","message":"Agent 'tutor' executed successfully","content":"[resposta do tutor]","metadata":{"agent_id":"tutor","subject":"matematica"}, "session_id":"sess-1","run_id":"..."}
  ```

## Tutor
- `GET $BASE_URL/tutor/info`
  ```bash
  curl "$BASE_URL/tutor/info"
  # => {"status":"success","message":"Informacoes do TutorAgent recuperadas com sucesso","agent_name":"Tutor ENEM - Especialista Educacional","supported_subjects":[{"key":"matematica","name":"Matematica","icon":"chart"}]}
  ```
- `POST $BASE_URL/tutor/chat`
  ```bash
  curl -X POST "$BASE_URL/tutor/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"Como resolver equacao do 2o grau?","subject":"matematica","user_id":"user-123"}'
  # => {"status":"success","message":"Resposta do tutor gerada com sucesso","content":"[explicacao]","metadata":{"agent_id":"tutor"},"session_id":"...","explanation_type":"problem","difficulty_level":"basic"}
  ```
- `GET $BASE_URL/tutor/subjects/{subject}/tree`
  ```bash
  curl "$BASE_URL/tutor/subjects/matematica/tree"
  # => {"status":"success","message":"Estrutura de topicos para Matematica recuperada com sucesso","subject":"matematica","subject_name":"Matematica","topics":[{"id":"algebra","name":"Algebra","subtopics":["Equacoes","Funcoes"]}],"total_topics":2}
  ```
- `GET $BASE_URL/tutor/learning-path/{subject}`
  ```bash
  curl "$BASE_URL/tutor/learning-path/portugues?current_level=intermediate&focus_areas=coesao&focus_areas=interpretacao"
  # => {"status":"success","message":"Trilha de aprendizagem para portugues criada com sucesso","subject":"portugues","current_level":"intermediate","recommended_path":[{"step":1,"topic":"Fundamentos"}],"estimated_duration":"5-6 semanas"}
  ```
- `GET $BASE_URL/tutor/subjects`
  ```bash
  curl "$BASE_URL/tutor/subjects"
  # => {"status":"success","message":"Materias suportadas recuperadas com sucesso","subjects":[{"key":"historia","name":"Historia","description":"Historia do ENEM","difficulty":"medium","estimated_hours":40}]}
  ```

## Quiz
- `GET $BASE_URL/quiz/info`
  ```bash
  curl "$BASE_URL/quiz/info"
  # => {"status":"success","message":"Informacoes do QuizAgent recuperadas com sucesso","agent_name":"Quiz ENEM - Gerador de Questoes","supported_subjects":[{"key":"fisica","topic_count":"12"}]}
  ```
- `POST $BASE_URL/quiz/generate`
  ```bash
  curl -X POST "$BASE_URL/quiz/generate" \
    -H "Content-Type: application/json" \
    -d '{"subject":"biologia","difficulty":"medio","num_questions":3,"topics":["genetica"]}'
  # => {"status":"success","message":"Quiz gerado com sucesso - 3 questoes","questions":[{"question_id":"...","command":"Enunciado","alternatives":{"A":"...","B":"..."},"correct_answer":"C"}],"total_questions":3,"quiz_id":"...","instructions":"Questoes de nivel medio..."}
  ```
- `GET $BASE_URL/quiz/quick-generate`
  ```bash
  curl "$BASE_URL/quiz/quick-generate?subject=historia&difficulty=facil&topic=era_vargas"
  # => {"status":"success","message":"Questao rapida gerada com sucesso","question":{"question_id":"...","command":"Enunciado rapido","alternatives":{"A":"...","B":"...","C":"...","D":"...","E":"..."}},"quiz_session_id":"..."}
  ```
- `POST $BASE_URL/quiz/submit`
  ```bash
  curl -X POST "$BASE_URL/quiz/submit" \
    -H "Content-Type: application/json" \
    -d '{"quiz_id":"quiz-123","answers":{"q1":"A","q2":"C","q3":"B"},"time_taken":780}'
  # => {"status":"success","message":"Quiz avaliado com sucesso","quiz_id":"quiz-123","total_questions":3,"correct_answers":1,"score_percentage":33.3,"grade":"Precisa melhorar","detailed_results":[{"question_id":"q1","is_correct":true}]}
  ```
- `GET $BASE_URL/quiz/topics/{subject}`
  ```bash
  curl "$BASE_URL/quiz/topics/quimica"
  # => {"status":"success","message":"Topicos de Quimica recuperados com sucesso","subject":"quimica","subject_name":"Quimica","topics":[{"id":"quimica_0","name":"Tabela periodica","estimated_questions":50,"description":"Topico importante para o ENEM: Tabela periodica"}],"total_count":1}
  ```
- `GET $BASE_URL/quiz/difficulties`
  ```bash
  curl "$BASE_URL/quiz/difficulties"
  # => {"status":"success","message":"Niveis de dificuldade recuperados com sucesso","difficulties":[{"key":"dificil","name":"Nivel avancado","weight":1.5,"characteristics":["Sintese","Analise complexa"]}]}
  ```

## Essay
- `GET $BASE_URL/essay/info`
  ```bash
  curl "$BASE_URL/essay/info"
  # => {"status":"success","message":"Informacoes do EssayGraderAgent recuperadas com sucesso","agent_name":"Corretor de Redacoes ENEM","competencies":[{"id":"competencia_1","name":"Dominio da lingua","max_score":"200"}],"capabilities":["Correcao automatica nas 5 competencias ENEM","Feedback detalhado e personalizado"]}
  ```
- `POST $BASE_URL/essay/grade`
  ```bash
  curl -X POST "$BASE_URL/essay/grade" \
    -H "Content-Type: application/json" \
    -d '{"essay_text":"Texto de exemplo com mais de cem caracteres para validar a correcao automatica do modelo. Ele inclui introducao, desenvolvimento e conclusao.", "theme":"Inclusao digital","student_id":"aluno-42"}'
  # => {"status":"success","message":"Redacao corrigida com sucesso","essay_id":"...","total_score":820,"final_percentage":82.0,"grade_level":"Muito Bom","competency_scores":[{"competency_id":"competencia_1","score":120}],"improvement_suggestions":["Praticar coesao"],"estimated_enem_score":820}
  ```
- `POST $BASE_URL/essay/grade-detailed`
  ```bash
  curl -X POST "$BASE_URL/essay/grade-detailed" \
    -H "Content-Type: application/json" \
    -d '{"essay_text":"Mesmo texto longo aqui para analise detalhada.","focus_competencies":["competencia_2","competencia_3"],"include_line_by_line":true}'
  # => {"status":"success","message":"Analise detalhada da redacao concluida","essay_id":"...","detailed_analysis":{"structural_analysis":{"introduction_quality":"Boa"}},"line_by_line_feedback":[{"line_number":1,"feedback":"Comentario sobre a linha 1"}]}
  ```
- `GET $BASE_URL/essay/rubric-details`
  ```bash
  curl "$BASE_URL/essay/rubric-details"
  # => {"status":"success","message":"Detalhes da rubrica recuperados com sucesso","competencies":[{"id":"competencia_4","name":"Coesao","criteria":["Introducao","Conclusao"]}],"scoring_levels":[{"score":0,"description":"Demonstra desconhecimento total"}]}
  ```
- `GET $BASE_URL/essay/sample-essays`
  ```bash
  curl "$BASE_URL/essay/sample-essays?grade_level=Excelente&theme=Educacao&min_score=800&limit=3"
  # => {"status":"success","message":"Retornados 3 exemplos de redacoes","essays":[{"essay_id":"sample_1","score":820,"grade_level":"Excelente","text_preview":"Inicio..." }],"total_count":3}
  ```

## Study Plan
- `GET $BASE_URL/study-plan/info`
  ```bash
  curl "$BASE_URL/study-plan/info"
  # => {"status":"success","message":"Informacoes do StudyPlanAgent recuperadas com sucesso","agent_name":"Planejador de Estudos ENEM","study_intensities":[{"level":"light","name":"Leve"}],"available_templates":[{"id":"enem_6_months","intensity":"medium"}]}
  ```
- `POST $BASE_URL/study-plan/generate`
  ```bash
  curl -X POST "$BASE_URL/study-plan/generate" \
    -H "Content-Type: application/json" \
    -d '{"available_hours_per_day":4,"study_days_per_week":5,"target_exam_date":"2025-11-10","priority_subjects":["matematica"],"weak_subjects":["fisica","quimica"],"study_intensity":"medium","include_breaks":true,"include_weekends":false}'
  # => {"status":"success","message":"Plano de estudos gerado com sucesso","plan_id":"...","total_duration_weeks":20,"weekly_schedules":[{"week_number":1,"total_hours":20}],"subject_distribution":{"matematica":{"percentage":"25.0%"}},"estimated_preparation_level":"Medio - Preparacao adequada"}
  ```
- `PUT $BASE_URL/study-plan/update-progress`
  ```bash
  curl -X PUT "$BASE_URL/study-plan/update-progress" \
    -H "Content-Type: application/json" \
    -d '{"plan_id":"plan-123","completed_hours":{"matematica":6,"portugues":3},"difficulty_feedback":{"matematica":"medium","portugues":"hard"},"topics_mastered":["funcoes"],"current_week":2}'
  # => {"status":"success","message":"Progresso atualizado e plano ajustado com sucesso","updated_plan_id":"plan-123_updated_20250101","adjustments_made":["Aumentar horas de portugues na proxima semana"],"completion_percentage":36.0}
  ```
- `GET $BASE_URL/study-plan/templates`
  ```bash
  curl "$BASE_URL/study-plan/templates?intensity=intensive&duration_weeks=24&daily_hours=6"
  # => {"status":"success","message":"Retornados 1 templates de estudo","templates":[{"template_id":"enem_intensive_6m","duration_weeks":24}],"recommended_template":"enem_intensive_6m"}
  ```

## Orchestrator
- `POST $BASE_URL/orchestrator/chat`
  ```bash
  curl -X POST "$BASE_URL/orchestrator/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"Preciso de um plano de estudos para matematica","user_id":"user-123"}'
  # => {"status":"success","message":"Mensagem processada com sucesso","response":"Aqui esta um plano de estudos focado em matematica...","agent_id":"study_plan","metadata":{"routed_to":"study_plan"}}
  ```
- `GET $BASE_URL/orchestrator/info`
  ```bash
  curl "$BASE_URL/orchestrator/info"
  # => {"name":"Orchestrator ENEM","description":"Coordenador central que roteia mensagens para agentes especializados.","capabilities":["Roteamento inteligente","Tutor (Materias)","Quiz (Questoes)","Essay (Redacao)","Study Plan (Cronogramas)"]}
  ```
