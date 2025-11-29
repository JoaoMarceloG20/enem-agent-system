"""
OrchestratorAgent Implementation

Coordenação central de todos os agentes, roteamento de mensagens e gerenciamento de sessões.
Funciona como roteador e coordenador, usando IA para classificar intenções.
"""

from textwrap import dedent
from typing import List, Any, Optional, Dict
from datetime import datetime
import json

from agno.agent import Agent
from app.agents.base_enem_agent import BaseENEMAgent
from app.core.config import settings

# Import other agents for delegation
from app.agents.tutor_agent import get_tutor_agent
from app.agents.quiz_agent import get_quiz_agent
from app.agents.essay_grader_agent import get_essay_grader_agent
from app.agents.study_plan_agent import get_study_plan_agent

class OrchestratorAgent(BaseENEMAgent):
    """
    Agente coordenador central do sistema ENEM.
    
    Características:
    - Roteamento inteligente de mensagens usando LLM
    - Delegação para agentes especializados
    - Gerenciamento de sessões
    """
    
    def get_agent_type(self) -> str:
        return 'orchestrator'
    
    def get_agent_name(self) -> str:
        return 'Orchestrator ENEM'
    
    def get_agent_description(self) -> str:
        return dedent(
            """\
            Agente coordenador central do sistema ENEM Tutor.
            Responsável por analisar a intenção do usuário e rotear para o agente especialista adequado.
            """
        )
    
    def get_agent_instructions(self) -> str:
        return dedent(
            """\
            Você é o Orchestrator do sistema ENEM Tutor.
            Sua função é analisar a mensagem do usuário e decidir qual agente deve responder.
            
            Agentes disponíveis:
            - TutorAgent: Para dúvidas de matérias, explicações de conceitos.
            - QuizAgent: Para criar quizzes, questões de prova.
            - EssayGraderAgent: Para corrigir redações ou dar dicas de escrita.
            - StudyPlanAgent: Para criar cronogramas e planos de estudo.
            
            Analise a mensagem e retorne APENAS um JSON com o formato:
            {
                "target_agent": "tutor" | "quiz" | "essay" | "study_plan" | "orchestrator",
                "reason": "breve explicação"
            }
            
            Se for uma saudação ou algo genérico, use "orchestrator".
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        return []
    
    def process_message(self, message: str, user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Processa a mensagem do usuário, classifica a intenção e delega para o agente correto.
        """
        # 1. Classify Intent using a lightweight Agent run
        classifier = Agent(
            model=self.get_agent(model_id=settings.gemini_model).model,
            instructions=self.get_agent_instructions(),
            show_tool_calls=False,
            markdown=False
        )
        
        try:
            response = classifier.run(message)
            # Clean up response to ensure it's valid JSON
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            intent_data = json.loads(content)
            target_agent = intent_data.get("target_agent", "tutor") # Default to tutor
            
        except Exception as e:
            print(f"Error classifying intent: {e}")
            target_agent = "tutor" # Fallback
            
        # 2. Delegate to the target agent
        if target_agent == "orchestrator":
            return {
                "content": "Olá! Sou o assistente central do ENEM. Posso te ajudar com estudos, quizzes, redação e planos de estudo. Como posso ajudar hoje?",
                "agent_id": "orchestrator"
            }
            
        # Map target to factory function
        agent_factories = {
            "tutor": get_tutor_agent,
            "quiz": get_quiz_agent,
            "essay": get_essay_grader_agent,
            "study_plan": get_study_plan_agent
        }
        
        factory = agent_factories.get(target_agent, get_tutor_agent)
        
        # Create and run the specialized agent
        # Note: We pass the same session_id to maintain context if supported, 
        # but ideally each agent might need its own session or a shared memory.
        # For this POC, we just run it.
        specialized_agent = factory(user_id=user_id, session_id=session_id, debug_mode=True)
        
        agent_response = specialized_agent.run(message)
        
        return {
            "content": agent_response.content,
            "agent_id": target_agent,
            "metadata": {
                "routed_to": target_agent,
                "reason": intent_data.get("reason", "Direct routing") if 'intent_data' in locals() else "Fallback"
            }
        }

def get_orchestrator_agent(
    model_id: str = settings.gemini_model,
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = True
):
    return OrchestratorAgent()