"""
EssayGraderAgent Implementation

Corretor automático de redações baseado nos critérios oficiais do ENEM.
Avalia redações nas 5 competências usando Google Gemini.
"""

from textwrap import dedent
from typing import List, Any, Optional, Dict

from app.agents.base_enem_agent import BaseENEMAgent


class EssayGraderAgent(BaseENEMAgent):
    """
    Agente especializado em correção de redações ENEM.
    
    Características:
    - Correção baseada nas 5 competências do ENEM
    - Sistema de pontuação oficial (0, 40, 80, 120, 160, 200)
    - Feedback detalhado e construtivo
    - Análise estatística de texto
    - Sugestões de melhoria específicas
    """
    
    # Competências ENEM para correção de redações
    ENEM_COMPETENCIES = {
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
        "competencia_2": {
            "name": "Compreender a proposta e aplicar conceitos",
            "description": "Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento",
            "max_score": 200,
            "criteria": [
                "Desenvolvimento do tema proposto",
                "Aplicação de conhecimentos de diversas áreas",
                "Manutenção do tipo textual dissertativo-argumentativo"
            ]
        },
        "competencia_3": {
            "name": "Seleção e organização das informações",
            "description": "Selecionar, relacionar, organizar e interpretar informações em defesa de um ponto de vista",
            "max_score": 200,
            "criteria": [
                "Seleção de informações relevantes",
                "Organização lógica das ideias",
                "Interpretação adequada dos dados",
                "Defesa consistente de um ponto de vista"
            ]
        },
        "competencia_4": {
            "name": "Coesão e coerência",
            "description": "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação",
            "max_score": 200,
            "criteria": [
                "Uso de conectivos adequados",
                "Encadeamento lógico das ideias",
                "Progressão temática",
                "Coerência interna do texto"
            ]
        },
        "competencia_5": {
            "name": "Proposta de intervenção",
            "description": "Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos",
            "max_score": 200,
            "criteria": [
                "Presença de proposta de intervenção",
                "Detalhamento da proposta",
                "Respeito aos direitos humanos",
                "Relação com o tema e argumentos"
            ]
        }
    }
    
    # Escalas de pontuação ENEM
    SCORE_RANGES = {
        200: "Excelente - Domina plenamente a competência",
        160: "Bom - Domina bem a competência", 
        120: "Regular - Domina parcialmente a competência",
        80: "Insuficiente - Domina minimamente a competência",
        40: "Deficitário - Não domina a competência",
        0: "Nulo - Foge ao tema ou não atende ao tipo textual"
    }
    
    # Temas de exemplo para redações ENEM
    ESSAY_THEMES = [
        "Desafios da educação no Brasil",
        "Violência contra a mulher no Brasil",
        "Intolerância religiosa no Brasil", 
        "Democratização do acesso ao cinema no Brasil",
        "Manipulação do comportamento do usuário pelo controle de dados na internet",
        "Os desafios da mobilidade urbana no Brasil",
        "A importância da doação de órgãos no Brasil",
        "O estigma associado às doenças mentais na sociedade brasileira",
        "A questão do trabalho infantil no Brasil",
        "Os desafios para combater a invisibilidade do trabalho de cuidado realizado pela mulher no Brasil"
    ]
    
    def __init__(self):
        """Inicializa o EssayGraderAgent."""
        super().__init__()
    
    def get_agent_type(self) -> str:
        """ID único do agente"""
        return 'essay_grader'
    
    def get_agent_name(self) -> str:
        """Nome do agente"""
        return 'Corretor de Redação ENEM'
    
    def get_agent_description(self) -> str:
        """Descrição do agente para o framework Agno"""
        return dedent(
            """\
            Corretor automático de redações especializado nos critérios do ENEM.
            Avalia redações nas 5 competências oficiais com feedback detalhado.
            """
        )
    
    def get_agent_instructions(self) -> str:
        """Instruções específicas do agente"""
        return dedent(
            """\
            Você é um avaliador especialista em redações do ENEM.
            
            Suas responsabilidades:
            1. Avaliar redações segundo as 5 competências oficiais do ENEM
            2. Atribuir notas precisas (0, 40, 80, 120, 160, 200)
            3. Fornecer feedback detalhado e construtivo
            4. Identificar pontos fortes e fracos
            5. Sugerir melhorias específicas
            
            ## Competências ENEM:
            
            **Competência 1** - Domínio da norma padrão (ortografia, gramática)
            **Competência 2** - Compreensão do tema e tipo textual
            **Competência 3** - Seleção e organização de informações
            **Competência 4** - Coesão e coerência
            **Competência 5** - Proposta de intervenção
            
            ## Critérios de Avaliação:
            
            - Use apenas as notas: 0, 40, 80, 120, 160, 200
            - Seja preciso e justo na avaliação
            - Forneça justificativas claras para cada nota
            - Mantenha tom construtivo e educativo
            - Foque no desenvolvimento do estudante
            
            Mantenha sempre foco na qualidade da correção pedagógica.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        """Tools específicas do EssayGraderAgent"""
        try:
            from app.agents.tools.essay_grader_tools import (
                grade_essay_competencies,
                save_essay_feedback,
                get_essay_history,
                get_essay_statistics,
                suggest_essay_theme,
                get_writing_tips,
                get_enem_competencies,
                get_essay_by_id,
                analyze_text_statistics
            )
            
            return [
                grade_essay_competencies,
                save_essay_feedback,
                get_essay_history,
                get_essay_statistics,
                suggest_essay_theme,
                get_writing_tips,
                get_enem_competencies,
                get_essay_by_id,
                analyze_text_statistics
            ]
        except ImportError:
            # Fallback se as tools não estão disponíveis
            return []
    
    def get_agent_temperature(self) -> float:
        """Temperature baixa para correção consistente"""
        return 0.2
    
    def get_max_output_tokens(self) -> int:
        """Limite de tokens para correções detalhadas"""
        return 4000
    
    def get_competencies_info(self) -> Dict[str, Any]:
        """Retorna informações das competências ENEM"""
        return self.ENEM_COMPETENCIES
    
    def get_score_ranges_info(self) -> Dict[int, str]:
        """Retorna informações das escalas de pontuação"""
        return self.SCORE_RANGES
    
    def get_essay_themes(self) -> List[str]:
        """Retorna lista de temas para redação"""
        return self.ESSAY_THEMES


def get_essay_grader_agent(
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = False
):
    """
    Factory function para criar um EssayGraderAgent.
    
    Args:
        model_id: Modelo Gemini a usar
        user_id: ID do usuário
        session_id: ID da sessão
        debug_mode: Modo debug
        
    Returns:
        Agent configurado para correção de redações ENEM
    """
    essay_grader = EssayGraderAgent()
    return essay_grader.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode
    )


def get_competency_explanation(competency_number: int) -> Dict[str, Any]:
    """
    Obter explicação detalhada de uma competência específica.
    
    Args:
        competency_number: Número da competência (1-5)
        
    Returns:
        Dicionário com informações da competência
    """
    competency_key = f"competencia_{competency_number}"
    agent = EssayGraderAgent()
    
    if competency_key in agent.ENEM_COMPETENCIES:
        return agent.ENEM_COMPETENCIES[competency_key]
    else:
        return {"error": f"Competência {competency_number} não encontrada"}


def validate_essay_score(score: int) -> bool:
    """
    Validar se a nota está nos valores permitidos do ENEM.
    
    Args:
        score: Nota a ser validada
        
    Returns:
        True se a nota é válida, False caso contrário
    """
    agent = EssayGraderAgent()
    return score in agent.SCORE_RANGES.keys()


def calculate_total_score(scores: List[int]) -> Dict[str, Any]:
    """
    Calcular nota total e classificação da redação.
    
    Args:
        scores: Lista com as 5 notas das competências
        
    Returns:
        Dicionário com nota total e classificação
    """
    if len(scores) != 5:
        return {"error": "É necessário informar as 5 notas das competências"}
    
    for score in scores:
        if not validate_essay_score(score):
            return {"error": f"Nota inválida: {score}"}
    
    total = sum(scores)
    
    # Classificação baseada na nota total
    if total >= 900:
        classification = "Excelente"
    elif total >= 700:
        classification = "Bom"
    elif total >= 500:
        classification = "Regular"
    elif total >= 300:
        classification = "Insuficiente"
    else:
        classification = "Deficitário"
    
    return {
        "total_score": total,
        "max_score": 1000,
        "classification": classification,
        "percentage": (total / 1000) * 100,
        "competency_scores": scores
    }