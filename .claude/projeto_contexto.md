# 📋 Contexto do Projeto Edtech Agent API

## 🎯 Objetivo Principal
Criar o backend da API dos agentes do projeto edtech (AI agents para educação), reproduzindo exatamente os mesmos agentes da POC documentada em AGENTES_MAPEAMENTO.md, porém com nossa nova estrutura baseada no projeto ubyfol-platform.

## 📁 Estrutura de Referência
- **Projeto de referência**: `/Users/pablofernando/work/ntropy/ubyfol/repos/ubyfol-platform/backend`
- **Diretório de agentes**: `app/agents/`
- **Padrão ouro**: Agent `dr_ubyfol` (referência para código e tecnologias)
- **Docker**: Usar docker-compose de ubyfol-platform como base

## 🤖 Agentes a Implementar (baseado em AGENTES_MAPEAMENTO.md)

### 1. BaseENEMAgent (Classe Base)
- Classe abstrata base para todos os agentes
- Integração com sistema de logs e métricas
- Gerenciamento de sessões e contexto
- Health checks automatizados

### 2. TutorAgent (Tutor Educacional)
- Tutor IA especializado em preparação para ENEM
- Todas as 13 matérias do ENEM
- Temperature: 0.7, Max tokens: 2048
- Tools: histórico, estatísticas, recomendações

### 3. QuizAgent (Gerador de Quiz)
- Geração e avaliação de quizzes estilo ENEM
- Temperature: 0.4, Max tokens: 3000
- Níveis: fácil, médio, difícil
- Sistema de correção automática

### 4. EssayGraderAgent (Corretor de Redação)
- Correção baseada nas 5 competências ENEM
- Temperature: 0.2, Max tokens: 4000
- Escalas de pontuação oficiais
- Feedback detalhado

### 5. StudyPlanAgent (Planos de Estudo)
- Planos personalizados e adaptativos
- Temperature: 0.3, Max tokens: 3000
- 4 níveis de intensidade
- Cronogramas semanais

### 6. OrchestratorAgent (Orquestrador Central)
- Coordenação central de todos os agentes
- Roteamento de mensagens
- Comandos do sistema
- Gerenciamento de sessões

## 🛠 Tecnologias Utilizadas na POC
- **Framework**: Agno (multi-agente)
- **Modelo IA**: Google Gemini 1.5 Flash
- **Backend**: FastAPI
- **Database**: SQLite
- **Vector DB**: Qdrant (preparado)
- **Cache**: Redis (preparado)

## 📋 Padrão de Tarefas
Todas as tasks devem seguir a estrutura:
- **TASK_(task_name_or_id)**: Arquivo com prompt detalhado, contexto completo para execução standalone
- **DONE_TASK_(task_name_or_id)**: Status de conclusão ou ponto de parada atual

## 🎯 Diretrizes de Desenvolvimento
1. Seguir padrões do agent dr_ubyfol como referência
2. Manter compatibilidade com estrutura ubyfol-platform
3. Implementar sistema de logs e métricas
4. Incluir health checks para todos os agentes
5. Usar as mesmas tecnologias da referência
6. Consultar antes de implementar patterns não presentes no dr_ubyfol