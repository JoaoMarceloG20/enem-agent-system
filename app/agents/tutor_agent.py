"""
TutorAgent Implementation

Tutor educacional especializado em preparação para ENEM.
Suporta todas as 13 matérias do ENEM com ensino adaptativo.
"""

from textwrap import dedent
from typing import List, Any, Optional
from datetime import datetime

from app.agents.base_enem_agent import BaseENEMAgent


class TutorAgent(BaseENEMAgent):
    """
    Tutor IA especializado em preparação para ENEM.
    
    Características:
    - Ensino adaptativo para todas as 13 matérias do ENEM
    - Explicações didáticas e contextualizadas
    - Sugestões de estudo personalizadas
    - Integração com knowledge base por matéria
    """
    
    # Matérias suportadas pelo ENEM
    ENEM_SUBJECTS = {
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
    
    def __init__(self, subject: Optional[str] = None):
        """
        Inicializa o TutorAgent.
        
        Args:
            subject: Matéria específica para focar (opcional)
        """
        self.subject = subject
    
    def get_agent_type(self) -> str:
        """ID único do agente"""
        return 'tutor'
    
    def get_agent_name(self) -> str:
        """Nome do agente"""
        return 'Tutor ENEM'
    
    def get_agent_description(self) -> str:
        """Descrição do agente para o framework Agno"""
        return dedent(
            """\
            Tutor IA especializado em preparação para o ENEM.
            Oferece ensino personalizado em todas as matérias do ENEM.
            """
        )
    
    def get_agent_instructions(self) -> str:
        """Instruções específicas do agente"""
        return dedent(
            """\
            Você é um tutor especializado em preparação para o ENEM (Exame Nacional do Ensino Médio).
            
            Suas responsabilidades:
            1. Fornecer explicações claras e didáticas
            2. Adaptar conteúdo ao nível do estudante  
            3. Focar na preparação para o ENEM
            4. Usar linguagem acessível
            
            Mantenha sempre foco na qualidade educacional.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        """Tools específicas do TutorAgent"""
        # Temporariamente desabilitado para debug
        return []
    
    def get_agent_temperature(self) -> float:
        """Temperature específica para ensino (balanceada)"""
        return 0.7
    
    def get_max_output_tokens(self) -> int:
        """Limite de tokens para respostas educacionais"""
        return 2048
    
    def get_subject_name(self) -> str:
        """Retorna o nome da matéria atual"""
        if self.subject and self.subject in self.ENEM_SUBJECTS:
            return self.ENEM_SUBJECTS[self.subject]
        return "Todas as Matérias"


def get_tutor_agent(
    subject: Optional[str] = None,
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = False
):
    """
    Factory function para criar um TutorAgent.
    
    Args:
        subject: Matéria específica (opcional)
        model_id: Modelo Gemini a usar
        user_id: ID do usuário
        session_id: ID da sessão
        debug_mode: Modo debug
        
    Returns:
        Agent configurado para tutoria ENEM
    """
    tutor = TutorAgent(subject=subject)
    return tutor.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode,
        subject=subject
    )


def get_math_tutor_agent(**kwargs):
    """Factory específica para tutor de Matemática"""
    return get_tutor_agent(subject='matematica', **kwargs)


def get_portuguese_tutor_agent(**kwargs):
    """Factory específica para tutor de Português"""
    return get_tutor_agent(subject='portugues', **kwargs)


def get_science_tutor_agent(subject: str, **kwargs):
    """
    Factory para tutores de Ciências da Natureza.
    
    Args:
        subject: 'fisica', 'quimica', ou 'biologia'
    """
    if subject not in ['fisica', 'quimica', 'biologia']:
        raise ValueError(f"Subject deve ser 'fisica', 'quimica' ou 'biologia', recebido: {subject}")
    
    return get_tutor_agent(subject=subject, **kwargs)


def get_humanities_tutor_agent(subject: str, **kwargs):
    """
    Factory para tutores de Ciências Humanas.
    
    Args:
        subject: 'historia', 'geografia', 'filosofia', ou 'sociologia'
    """
    if subject not in ['historia', 'geografia', 'filosofia', 'sociologia']:
        raise ValueError(f"Subject deve ser 'historia', 'geografia', 'filosofia' ou 'sociologia', recebido: {subject}")
    
    return get_tutor_agent(subject=subject, **kwargs)