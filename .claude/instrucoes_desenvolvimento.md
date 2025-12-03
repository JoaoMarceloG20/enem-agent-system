# 📋 Instruções de Desenvolvimento - Edtech Agent API

## 🚀 Procedimento de Desenvolvimento

### 1. Estrutura de Tasks
Todas as tarefas de desenvolvimento devem seguir o padrão estabelecido:

#### Arquivo TASK_[nome_da_task]
```markdown
# TASK: [Nome da Tarefa]

## Objetivo
Descrição clara e concisa do que deve ser implementado.

## Contexto Completo
- Informações de fundo necessárias
- Dependencies e pré-requisitos
- Arquivos de referência
- Padrões a seguir

## Requisitos Detalhados
1. Requisito funcional 1
2. Requisito funcional 2
3. Requisitos não funcionais

## Critérios de Aceitação
- [ ] Critério 1
- [ ] Critério 2
- [ ] Testes passando
- [ ] Documentação atualizada

## Referências
- Arquivos de referência no projeto ubyfol-platform
- Especificações do AGENTES_MAPEAMENTO.md
- Padrões do agent dr_ubyfol
```

#### Arquivo DONE_TASK_[nome_da_task]
```markdown
# DONE: [Nome da Tarefa]

## Status
- [x] Concluída / [ ] Em Andamento / [ ] Pausada

## Implementação Realizada
Descrição do que foi implementado.

## Arquivos Modificados/Criados
- arquivo1.py
- arquivo2.py

## Testes
- [ ] Testes unitários criados
- [ ] Testes de integração passando
- [ ] Health checks funcionando

## Próximos Passos (se aplicável)
Lista de itens para continuar o desenvolvimento.

## Notas Importantes
Observações importantes sobre a implementação.
```

### 2. Fluxo de Trabalho

#### Antes de Iniciar uma Task
1. Ler completamente o arquivo TASK_
2. Verificar se todos os pré-requisitos estão atendidos
3. Analisar arquivos de referência mencionados
4. Criar/atualizar DONE_TASK_ como "Em Andamento"

#### Durante o Desenvolvimento
1. Seguir padrões do projeto de referência (dr_ubyfol)
2. Implementar logs e métricas consistentes
3. Incluir health checks quando aplicável
4. Manter compatibilidade com estrutura existente
5. Consultar antes de implementar patterns não presentes na referência

#### Ao Finalizar uma Task
1. Executar testes (lint, typecheck, unit tests)
2. Atualizar DONE_TASK_ com status "Concluída"
3. Documentar arquivos modificados/criados
4. Listar próximos passos se houver dependencies

### 3. Estrutura de Diretórios

```
.claude/
├── projeto_contexto.md          # Contexto geral do projeto
├── instrucoes_desenvolvimento.md # Este arquivo
├── entrypoint.md               # Ponto de entrada para novas sessões
└── memoria/                    # Informações importantes para "memória"
    ├── agentes_especificacoes.md
    ├── padroes_codigo.md
    └── tecnologias_utilizadas.md

tasks/
├── TASK_setup_project_structure
├── DONE_TASK_setup_project_structure
├── TASK_implement_base_agent
├── DONE_TASK_implement_base_agent
└── ...
```

### 4. Tecnologias e Padrões

#### Tecnologias Base (do ubyfol-platform)
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL/SQLite
- Redis
- Docker

#### Tecnologias IA (da POC)
- Google Gemini 1.5 Flash
- Langchain (se usado na referência)
- Qdrant (vector database)

#### Padrões de Código
- Seguir estrutura do agent dr_ubyfol
- Usar type hints em Python
- Implementar logging estruturado
- Health checks em todos os agentes
- Tratamento de exceções consistente

### 5. Processo de Validação

#### Antes de Considerar uma Task Concluída
1. **Testes**: Todos os testes passando
2. **Lint**: Código seguindo padrões de estilo
3. **Type Check**: Verificação de tipos sem erros
4. **Health Check**: Agent respondendo corretamente
5. **Compatibilidade**: Integração com estrutura existente
6. **Documentação**: DONE_TASK_ atualizada completamente

#### Critérios de Qualidade
- Código compatível com padrões da referência
- Performance adequada para uso em produção
- Tratamento de erros robusto
- Logs informativos e estruturados
- APIs RESTful seguindo convenções

### 6. Paralelização de Tasks

#### Tasks Independentes (podem ser executadas em paralelo)
- Implementação de agentes individuais
- Criação de modelos de dados
- Implementação de APIs específicas
- Testes unitários por módulo

#### Tasks Dependentes (devem ser executadas em sequência)
- Setup da estrutura base → Implementação de agentes
- Base Agent → Agentes específicos
- Modelos de dados → APIs que os utilizam
- Implementação → Testes de integração

### 7. Comunicação e Consultas

#### Quando Consultar
- Pattern não presente no agent dr_ubyfol
- Dúvidas sobre compatibilidade
- Decisões arquiteturais importantes
- Problemas de integração com ubyfol-platform

#### Como Consultar
- Descrever o problema/dúvida claramente
- Incluir contexto da task atual
- Mencionar alternativas consideradas
- Sugerir solução preferida (se houver)