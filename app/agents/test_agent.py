"""
Test Agent Implementation

Simple implementation of BaseENEMAgent for testing purposes.
This demonstrates how to extend the base class.
"""

from textwrap import dedent
from typing import List, Any

from app.agents.base_enem_agent import BaseENEMAgent


class TestENEMAgent(BaseENEMAgent):
    """Test implementation of BaseENEMAgent for validation"""
    
    def get_agent_type(self) -> str:
        return 'test_enem'
    
    def get_agent_name(self) -> str:
        return 'Test ENEM Agent'
    
    def get_agent_description(self) -> str:
        return dedent(
            """\
            Agente de teste para validação do sistema ENEM.
            Este agente serve para testar a infraestrutura base antes da implementação dos agentes principais.
            """
        )
    
    def get_agent_instructions(self) -> str:
        return dedent(
            """\
            Você é um agente de teste do sistema ENEM Tutor.
            
            Suas responsabilidades:
            1. Responder de forma educada e útil
            2. Confirmar que o sistema está funcionando
            3. Testar funcionalidades básicas como memória e conhecimento
            4. Fornecer informações sobre o status do sistema
            
            Mantenha sempre um tom profissional e educativo.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        # Test agent doesn't need additional tools beyond ReasoningTools
        return []
    
    def get_agent_temperature(self) -> float:
        return 0.5  # Balanced for testing
    
    def get_max_output_tokens(self) -> int:
        return 1024  # Lower limit for testing


def get_test_enem_agent(
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = True,
):
    """
    Factory function to create a test ENEM agent.
    
    Args:
        model_id: Gemini model ID
        user_id: Optional user ID
        session_id: Optional session ID  
        debug_mode: Enable debug logging
        
    Returns:
        Configured Agent instance for testing
    """
    test_agent = TestENEMAgent()
    return test_agent.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode
    )