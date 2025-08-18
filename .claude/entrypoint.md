# 🚪 Entrypoint - Edtech Agent API

## 👋 Bem-vindo ao Projeto Edtech Agent API

Este é o ponto de entrada para modelos/agentes que iniciam uma nova sessão de trabalho neste projeto.

## 📋 Primeiro, Leia Estes Arquivos

1. **`.claude/projeto_contexto.md`** - Contexto completo do projeto
2. **`.claude/instrucoes_desenvolvimento.md`** - Procedimentos e padrões de desenvolvimento
3. **`AGENTES_MAPEAMENTO.md`** - Especificações detalhadas dos agentes da POC

## 🎯 Status Atual do Projeto - ATUALIZADO 15/08/2025

### ✅ PROJETO BASE COMPLETO (100%)
- [x] Setup inicial da estrutura .claude
- [x] Análise das especificações dos agentes
- [x] Análise do projeto de referência ubyfol-platform
- [x] Criação da estrutura base do projeto
- [x] Implementação do BaseENEMAgent
- [x] **TODOS OS 6 AGENTES IMPLEMENTADOS E FUNCIONAIS**
- [x] Integração com docker-compose
- [x] Testes e validação
- [x] Correção de bugs críticos (datetime formatting)

### 🔄 MELHORIAS EM ANDAMENTO (20% concluído)
- [x] Roadmap de melhorias criado
- [x] Router específico TutorAgent (funcionando)
- [ ] Router específico QuizAgent (erro Pydantic)
- [ ] Router específico EssayAgent
- [ ] Router específico StudyPlanAgent
- [ ] Router específico OrchestratorAgent

### 🎯 PRÓXIMA SESSÃO
**PONTO DE RETOMADA**: Corrigir erro validação Pydantic no QuizAgent e continuar routers específicos.
**ARQUIVO IMPORTANTE**: `.claude/post_compact_entrypoint.md` - contexto completo da sessão atual

## 📁 Estrutura do Projeto

```
edtech-agent-api/
├── .claude/                    # Contexto e instruções
│   ├── projeto_contexto.md
│   ├── instrucoes_desenvolvimento.md
│   ├── entrypoint.md          # Este arquivo
│   └── memoria/               # Informações importantes
├── tasks/                     # Tasks para desenvolvimento paralelo
├── app/                       # Código fonte principal (a ser criado)
│   └── agents/               # Diretório dos agentes
├── docker-compose.yml        # Container setup (a ser copiado)
└── AGENTES_MAPEAMENTO.md     # Especificações da POC
```

## 🤖 Agentes a Implementar

### Prioridade 1 - Base
1. **BaseENEMAgent** - Classe abstrata base
2. **OrchestratorAgent** - Coordenação central

### Prioridade 2 - Agentes Principais
3. **TutorAgent** - Tutor educacional
4. **QuizAgent** - Gerador de quiz
5. **EssayGraderAgent** - Corretor de redação
6. **StudyPlanAgent** - Planos de estudo

## 🛠 Como Continuar o Desenvolvimento

### 1. Verificar Tasks Pendentes
```bash
ls tasks/TASK_*
ls tasks/DONE_TASK_*
```

### 2. Consultar Status das Tasks
Ler arquivos DONE_TASK_ para entender o que já foi implementado.

### 3. Escolher Próxima Task
- Se houver TASK_ sem DONE_TASK_ correspondente, continuar implementação
- Se todas as tasks estão concluídas, verificar próximos passos no roadmap

### 4. Análise do Projeto de Referência
Antes de implementar qualquer agent, analisar:
- `/Users/pablofernando/work/ntropy/ubyfol/repos/ubyfol-platform/backend/app/agents/dr_ubyfol/`
- Estrutura de arquivos e padrões de código
- Tecnologias e dependencies utilizadas

## 📞 Quando Consultar o Usuário

### Consultar Antes de:
- Implementar patterns não presentes no dr_ubyfol
- Fazer mudanças na arquitetura
- Escolher tecnologias diferentes da referência
- Modificar estrutura de dados importantes

### Implementar Diretamente:
- Seguir padrões já estabelecidos no dr_ubyfol
- Reproduzir especificações do AGENTES_MAPEAMENTO.md
- Aplicar instruções de desenvolvimento já definidas
- Criar testes e documentação

## 🎯 Metas Principais

1. **Compatibilidade Total**: Com estrutura ubyfol-platform
2. **Funcionalidade Completa**: Todos os 6 agentes funcionais
3. **Qualidade**: Testes, logs, health checks
4. **Produção**: Docker, configurações, deployment ready

## 🚀 Comandos Úteis

```bash
# Verificar estrutura atual
find . -name "*.py" | head -10

# Ver tasks pendentes  
ls tasks/

# Verificar dependências
cat requirements.txt

# Status git
git status
```

---

**💡 Dica**: Sempre consulte os arquivos na pasta `.claude/` antes de iniciar qualquer implementação. Eles contêm o contexto completo e as instruções mais atualizadas do projeto.