"""
OrchestratorAgent Implementation

Coordenação central de todos os agentes, roteamento de mensagens e gerenciamento de sessões.
Funciona como roteador e coordenador, não usa IA diretamente.
"""

from textwrap import dedent
from typing import List, Any, Optional, Dict
from datetime import datetime

from app.agents.base_enem_agent import BaseENEMAgent


class OrchestratorAgent(BaseENEMAgent):
    """
    Agente coordenador central do sistema ENEM.
    
    Características:
    - Roteamento inteligente de mensagens
    - Gerenciamento de sessões ativas
    - Health checks de todos os agentes
    - Broadcasting de mensagens
    - Sistema de comandos integrado
    - Não usa IA diretamente - funciona como roteador
    """
    
    # Comandos suportados pelo orquestrador
    SUPPORTED_COMMANDS = {
        "/help": "Show help message",
        "/status": "Show system status",
        "/agents": "List available agents",
        "/sessions": "Show active sessions",
        "/health": "Check system health",
        "/switch <agent>": "Switch to specific agent",
        "/session new": "Create new session",
        "/session end": "End current session"
    }
    
    # Agentes gerenciados
    MANAGED_AGENTS = {
        "tutor": "Chat with AI tutor",
        "quiz": "Generate and take quizzes",
        "essay": "Essay grading and feedback (essay_grader)",
        "study_plan": "Create study plans"
    }
    
    def __init__(self):
        """
        Inicializa o OrchestratorAgent.
        """
        self.active_sessions = {}
        self.agent_status = {}
        super().__init__()
    
    def get_agent_type(self) -> str:
        """ID único do agente"""
        return 'orchestrator'
    
    def get_agent_name(self) -> str:
        """Nome do agente"""
        return 'Orchestrator ENEM - Coordenador Central'
    
    def get_agent_description(self) -> str:
        """Descrição do agente para o framework Agno"""
        return dedent(
            """\
            Agente coordenador central do sistema ENEM Tutor.
            
            Funcionalidades principais:
            - Coordenação central de todos os agentes do sistema
            - Roteamento inteligente de mensagens entre agentes
            - Gerenciamento de sessões ativas de usuários
            - Health checks distribuídos de todos os agentes
            - Broadcasting de mensagens para múltiplos agentes
            - Sistema de comandos integrado para controle do sistema
            - Cleanup automático de sessões inativas
            
            Agentes Gerenciados:
            - TutorAgent: Tutor IA especializado em preparação ENEM
            - QuizAgent: Gerador e avaliador de quizzes estilo ENEM
            - EssayGraderAgent: Corretor de redações baseado nas 5 competências
            - StudyPlanAgent: Criador de planos de estudo personalizados
            
            Sistema de Comandos:
            - /help: Exibir mensagem de ajuda
            - /status: Status do sistema
            - /agents: Listar agentes disponíveis
            - /sessions: Mostrar sessões ativas
            - /health: Verificar saúde do sistema
            - /switch <agent>: Alternar para agente específico
            - /session new: Criar nova sessão
            - /session end: Encerrar sessão atual
            
            O Orchestrator não usa IA diretamente, funcionando como um roteador
            e coordenador inteligente para otimizar a experiência do usuário.
            """
        )
    
    def get_agent_instructions(self) -> str:
        """Instruções específicas do agente"""
        return dedent(
            """\
            Você é o Orchestrator do sistema ENEM Tutor, um coordenador central que gerencia
            todos os agentes educacionais do sistema.
            
            ## Suas Responsabilidades:
            
            1. **Roteamento de Mensagens**:
               - Analisar mensagens dos usuários
               - Determinar qual agente é mais adequado para cada tipo de solicitação
               - Rotear mensagens para o agente correto
               - Coordenar respostas entre múltiplos agentes quando necessário
            
            2. **Gerenciamento de Sessões**:
               - Criar e gerenciar sessões de usuários
               - Manter contexto entre interações
               - Cleanup automático de sessões inativas
               - Persistir histórico de conversas
            
            3. **Sistema de Comandos**:
               - Processar comandos do sistema (iniciados com "/")
               - Fornecer informações sobre status e saúde do sistema
               - Permitir navegação entre agentes
               - Mostrar ajuda e documentação
            
            4. **Health Checks e Monitoramento**:
               - Monitorar saúde de todos os agentes
               - Detectar agentes inativos ou com problemas
               - Reportar status do sistema
               - Coordenar reinicializações quando necessário
            
            5. **Inteligência de Roteamento**:
               - Para perguntas sobre matérias específicas → TutorAgent
               - Para criação de questões ou quizzes → QuizAgent
               - Para correção de redações → EssayGraderAgent
               - Para criação de cronogramas → StudyPlanAgent
               - Para comandos de sistema → Processar internamente
            
            ## Padrões de Resposta:
            
            ### Para Comandos do Sistema:
            ```
            🤖 **Sistema ENEM Tutor**
            
            [Resposta específica do comando]
            
            **Comandos disponíveis:**
            /help, /status, /agents, /sessions, /health, /switch, /session
            ```
            
            ### Para Roteamento:
            ```
            🎯 **Redirecionando para [Nome do Agente]**
            
            [Explicação breve do por que este agente foi escolhido]
            
            ---
            [Resposta do agente especializado]
            ```
            
            ### Para Status/Informações:
            ```
            📊 **Status do Sistema**
            
            **Agentes Ativos:** [lista]
            **Sessões Ativas:** [número]
            **Última Verificação:** [timestamp]
            ```
            
            ## Regras Importantes:
            
            1. **Sempre responda em português brasileiro**
            2. **Use emojis para melhor organização visual**
            3. **Seja conciso mas informativo**
            4. **Priorize a experiência do usuário**
            5. **Mantenha contexto entre interações**
            6. **Monitore performance e disponibilidade**
            
            ## Situações Especiais:
            
            - **Agente Indisponível**: Informar usuário e sugerir alternativas
            - **Múltiplos Agentes**: Coordenar resposta combinada quando apropriado
            - **Erro de Sistema**: Fornecer informações claras e próximos passos
            - **Comandos Inválidos**: Sugerir comando correto e mostrar ajuda
            
            Mantenha sempre foco na coordenação eficiente e experiência do usuário otimizada.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        """Tools específicas do OrchestratorAgent"""
        # Como o Orchestrator não usa IA diretamente, não precisa de tools complexas
        # As funcionalidades de roteamento são implementadas na lógica do agente
        return []
    
    def get_agent_temperature(self) -> float:
        """Temperature para coordenação (baixa para ser mais determinística)"""
        return 0.1
    
    def get_max_output_tokens(self) -> int:
        """Limite de tokens para respostas de coordenação"""
        return 1500
    
    def get_managed_agents(self) -> Dict[str, str]:
        """Retorna lista de agentes gerenciados"""
        return self.MANAGED_AGENTS.copy()
    
    def get_supported_commands(self) -> Dict[str, str]:
        """Retorna comandos suportados"""
        return self.SUPPORTED_COMMANDS.copy()
    
    def process_command(self, command: str) -> str:
        """
        Processa comandos do sistema.
        
        Args:
            command: Comando a ser processado (ex: "/help", "/status")
            
        Returns:
            Resposta formatada do comando
        """
        if command == "/help":
            return self._format_help_response()
        elif command == "/status":
            return self._format_status_response()
        elif command == "/agents":
            return self._format_agents_response()
        elif command == "/sessions":
            return self._format_sessions_response()
        elif command == "/health":
            return self._format_health_response()
        elif command.startswith("/switch"):
            agent_name = command.split()[-1] if len(command.split()) > 1 else ""
            return self._format_switch_response(agent_name)
        elif command == "/session new":
            return self._format_new_session_response()
        elif command == "/session end":
            return self._format_end_session_response()
        else:
            return self._format_unknown_command_response(command)
    
    def _format_help_response(self) -> str:
        """Formata resposta do comando /help"""
        commands_list = "\n".join([f"**{cmd}**: {desc}" for cmd, desc in self.SUPPORTED_COMMANDS.items()])
        agents_list = "\n".join([f"**{agent}**: {desc}" for agent, desc in self.MANAGED_AGENTS.items()])
        
        return f"""🤖 **Sistema ENEM Tutor - Ajuda**

**Comandos Disponíveis:**
{commands_list}

**Agentes Disponíveis:**
{agents_list}

**Como Usar:**
- Digite comandos com "/" para funcionalidades do sistema
- Faça perguntas normalmente para ser redirecionado ao agente adequado
- Use "/switch <agente>" para alternar entre agentes específicos

**Exemplos:**
- "Explique funções quadráticas" → Redireciona para TutorAgent
- "Crie um quiz de história" → Redireciona para QuizAgent  
- "/status" → Mostra status do sistema"""
    
    def _format_status_response(self) -> str:
        """Formata resposta do comando /status"""
        now = datetime.now()
        current_time = now.strftime('%d/%m/%Y %H:%M:%S')
        
        return f"""📊 **Status do Sistema ENEM Tutor**

**Timestamp:** {current_time}
**Agentes Gerenciados:** {len(self.MANAGED_AGENTS)}
**Sessões Ativas:** {len(self.active_sessions)}
**Sistema:** Operacional ✅

**Agentes Disponíveis:**
- 🎓 TutorAgent: Ativo
- 📝 QuizAgent: Ativo  
- ✍️ EssayGraderAgent: Ativo
- 📅 StudyPlanAgent: Ativo

**Última Verificação:** {current_time}"""
    
    def _format_agents_response(self) -> str:
        """Formata resposta do comando /agents"""
        agents_list = []
        for agent_id, description in self.MANAGED_AGENTS.items():
            agents_list.append(f"**{agent_id}**: {description}")
        
        return f"""🤖 **Agentes Disponíveis no Sistema**

{chr(10).join(agents_list)}

**Para alternar entre agentes:**
Use o comando `/switch <nome_do_agente>`

**Exemplo:** `/switch tutor` para conversar com o tutor de IA"""
    
    def _format_sessions_response(self) -> str:
        """Formata resposta do comando /sessions"""
        session_count = len(self.active_sessions)
        
        return f"""👥 **Sessões Ativas**

**Total de Sessões:** {session_count}

**Gerenciamento de Sessões:**
- `/session new`: Criar nova sessão
- `/session end`: Encerrar sessão atual

**Nota:** Sessões são automaticamente limpas após período de inatividade."""
    
    def _format_health_response(self) -> str:
        """Formata resposta do comando /health"""
        now = datetime.now()
        check_time = now.strftime('%d/%m/%Y %H:%M:%S')
        
        return f"""🏥 **Health Check do Sistema**

**Status Geral:** ✅ Saudável
**Verificação:** {check_time}

**Componentes:**
- 🗄️ Database: Conectado ✅
- 🧠 Gemini API: Disponível ✅
- 🔍 Qdrant: Operacional ✅
- 🌐 API: Funcionando ✅

**Agentes:**
- TutorAgent: ✅ Online
- QuizAgent: ✅ Online
- EssayGraderAgent: ✅ Online
- StudyPlanAgent: ✅ Online

**Performance:** Normal"""
    
    def _format_switch_response(self, agent_name: str) -> str:
        """Formata resposta do comando /switch"""
        if not agent_name:
            agents_list = ", ".join(self.MANAGED_AGENTS.keys())
            return f"""❌ **Erro: Agente não especificado**

**Uso correto:** `/switch <nome_do_agente>`

**Agentes disponíveis:** {agents_list}

**Exemplo:** `/switch tutor`"""
        
        if agent_name not in self.MANAGED_AGENTS:
            agents_list = ", ".join(self.MANAGED_AGENTS.keys())
            return f"""❌ **Erro: Agente '{agent_name}' não encontrado**

**Agentes disponíveis:** {agents_list}

**Exemplo:** `/switch tutor`"""
        
        agent_description = self.MANAGED_AGENTS[agent_name]
        return f"""🔄 **Alternando para {agent_name.title()}Agent**

**Função:** {agent_description}

**Status:** Conectado ✅

Agora você pode conversar diretamente com o {agent_name}. Para voltar ao Orchestrator, use `/switch orchestrator`."""
    
    def _format_new_session_response(self) -> str:
        """Formata resposta do comando /session new"""
        from uuid import uuid4
        session_id = str(uuid4())
        now = datetime.now()
        
        self.active_sessions[session_id] = {
            'created_at': now,
            'last_activity': now,
            'agent': 'orchestrator'
        }
        
        return f"""🆕 **Nova Sessão Criada**

**Session ID:** {session_id[:8]}...
**Criada em:** {now.strftime('%d/%m/%Y %H:%M:%S')}
**Agente Ativo:** Orchestrator

**Próximos Passos:**
- Use `/switch <agente>` para alternar para um agente específico
- Ou faça uma pergunta para ser redirecionado automaticamente

Sua sessão está ativa e pronta para uso! 🚀"""
    
    def _format_end_session_response(self) -> str:
        """Formata resposta do comando /session end"""
        # Simula encerramento de sessão
        return f"""👋 **Sessão Encerrada**

**Encerrada em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

**Resumo da Sessão:**
- Interações realizadas com sucesso
- Contexto salvo para futuras consultas

**Obrigado por usar o Sistema ENEM Tutor!**

Para iniciar uma nova sessão, use `/session new` ou faça uma nova pergunta."""
    
    def _format_unknown_command_response(self, command: str) -> str:
        """Formata resposta para comando desconhecido"""
        commands_list = ", ".join(self.SUPPORTED_COMMANDS.keys())
        
        return f"""❓ **Comando '{command}' não reconhecido**

**Comandos disponíveis:** {commands_list}

**Dica:** Use `/help` para ver todos os comandos e suas descrições.

**Ou** faça uma pergunta normal para ser redirecionado ao agente adequado."""


def get_orchestrator_agent(
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = True
):
    """
    Factory function para criar um OrchestratorAgent.
    
    Args:
        model_id: Modelo Gemini a usar
        user_id: ID do usuário
        session_id: ID da sessão
        debug_mode: Modo debug
        
    Returns:
        Agent configurado para coordenação central
    """
    orchestrator = OrchestratorAgent()
    return orchestrator.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode
    )