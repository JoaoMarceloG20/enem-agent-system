"""
StudyPlanAgent Implementation

Criação de planos de estudo personalizados e adaptativos para o ENEM.
Distribui horas de estudo baseado na importância e dificuldade das matérias.
"""

from textwrap import dedent
from typing import List, Any, Optional, Dict
from datetime import datetime, timedelta

from app.agents.base_enem_agent import BaseENEMAgent


class StudyPlanAgent(BaseENEMAgent):
    """
    Agente especializado em criação de planos de estudo para o ENEM.
    
    Características:
    - Planos personalizados baseados em tempo disponível
    - Distribuição inteligente de horas por matéria
    - Múltiplos níveis de intensidade
    - Cronogramas semanais detalhados
    - Sistema de marcos e milestones
    - Adaptação baseada em performance
    """
    
    # Pesos das matérias baseados na importância no ENEM
    SUBJECT_WEIGHTS = {
        "matematica": {
            "hours_per_week": 8,
            "difficulty": "high", 
            "weight": 0.20,
            "description": "Matemática e suas Tecnologias"
        },
        "portugues": {
            "hours_per_week": 6,
            "difficulty": "medium",
            "weight": 0.15,
            "description": "Língua Portuguesa"
        },
        "fisica": {
            "hours_per_week": 6,
            "difficulty": "high",
            "weight": 0.15,
            "description": "Física"
        },
        "quimica": {
            "hours_per_week": 6,
            "difficulty": "high",
            "weight": 0.15,
            "description": "Química"
        },
        "biologia": {
            "hours_per_week": 5,
            "difficulty": "medium",
            "weight": 0.10,
            "description": "Biologia"
        },
        "redacao": {
            "hours_per_week": 4,
            "difficulty": "medium",
            "weight": 0.10,
            "description": "Redação"
        },
        "historia": {
            "hours_per_week": 3,
            "difficulty": "medium",
            "weight": 0.06,
            "description": "História"
        },
        "geografia": {
            "hours_per_week": 3,
            "difficulty": "medium",
            "weight": 0.06,
            "description": "Geografia"
        },
        "literatura": {
            "hours_per_week": 2,
            "difficulty": "low",
            "weight": 0.02,
            "description": "Literatura"
        },
        "filosofia": {
            "hours_per_week": 1,
            "difficulty": "low",
            "weight": 0.005,
            "description": "Filosofia"
        },
        "sociologia": {
            "hours_per_week": 1,
            "difficulty": "low",
            "weight": 0.005,
            "description": "Sociologia"
        },
        "ingles": {
            "hours_per_week": 1,
            "difficulty": "low",
            "weight": 0.005,
            "description": "Inglês"
        },
        "espanhol": {
            "hours_per_week": 1,
            "difficulty": "low",
            "weight": 0.005,
            "description": "Espanhol"
        }
    }
    
    # Níveis de intensidade de estudo
    INTENSITY_LEVELS = {
        "light": {
            "hours_per_day": 2,
            "days_per_week": 5,
            "total_hours_per_week": 10,
            "description": "Ritmo leve - 2h/dia, 5 dias/semana",
            "suitable_for": "Estudantes com pouco tempo disponível"
        },
        "moderate": {
            "hours_per_day": 4,
            "days_per_week": 6,
            "total_hours_per_week": 24,
            "description": "Ritmo moderado - 4h/dia, 6 dias/semana",
            "suitable_for": "Estudantes com tempo regular"
        },
        "intensive": {
            "hours_per_day": 6,
            "days_per_week": 6,
            "total_hours_per_week": 36,
            "description": "Ritmo intensivo - 6h/dia, 6 dias/semana",
            "suitable_for": "Estudantes dedicados com boa disponibilidade"
        },
        "extreme": {
            "hours_per_day": 8,
            "days_per_week": 7,
            "total_hours_per_week": 56,
            "description": "Ritmo extremo - 8h/dia, 7 dias/semana",
            "suitable_for": "Preparação final ou estudantes em tempo integral"
        }
    }
    
    # Fases de estudo típicas para o ENEM
    STUDY_PHASES = {
        "foundation": {
            "name": "Base Conceitual",
            "duration_weeks": 8,
            "focus": "Conceitos fundamentais e teoria",
            "activities": ["Leitura de teoria", "Exercícios básicos", "Resumos"]
        },
        "practice": {
            "name": "Prática Intensiva", 
            "duration_weeks": 12,
            "focus": "Resolução de exercícios e aplicação",
            "activities": ["Exercícios variados", "Questões ENEM", "Simulados parciais"]
        },
        "review": {
            "name": "Revisão e Simulados",
            "duration_weeks": 6,
            "focus": "Revisão geral e simulados completos",
            "activities": ["Revisão de pontos fracos", "Simulados completos", "Estratégias de prova"]
        },
        "final": {
            "name": "Reta Final",
            "duration_weeks": 2,
            "focus": "Manutenção e estratégias finais",
            "activities": ["Revisão leve", "Estratégias de prova", "Controle de ansiedade"]
        }
    }
    
    def __init__(self, intensity: str = "moderate"):
        """
        Inicializa o StudyPlanAgent.
        
        Args:
            intensity: Nível de intensidade do plano ('light', 'moderate', 'intensive', 'extreme')
        """
        self.intensity = intensity if intensity in self.INTENSITY_LEVELS else "moderate"
        super().__init__()
    
    def get_agent_type(self) -> str:
        """ID único do agente"""
        return f'study_plan_{self.intensity}'
    
    def get_agent_name(self) -> str:
        """Nome do agente"""
        intensity_info = self.INTENSITY_LEVELS[self.intensity]
        return f'Plano de Estudos ENEM - {intensity_info["description"]}'
    
    def get_agent_description(self) -> str:
        """Descrição do agente para o framework Agno"""
        return dedent(
            """\
            Especialista em criação de planos de estudo personalizados para o ENEM.
            Cria cronogramas detalhados com distribuição inteligente de tempo.
            """
        )
    
    def get_agent_instructions(self) -> str:
        """Instruções específicas do agente"""
        intensity_info = self.INTENSITY_LEVELS[self.intensity]
        
        return dedent(
            f"""\
            Você é um especialista em planejamento de estudos para o ENEM.
            
            Intensidade atual: {intensity_info['description']}
            Horas semanais: {intensity_info['total_hours_per_week']}h
            
            Suas responsabilidades:
            1. Criar planos de estudo personalizados e realistas
            2. Distribuir tempo adequadamente entre as matérias
            3. Considerar a dificuldade e peso de cada matéria no ENEM
            4. Criar cronogramas semanais detalhados
            5. Definir marcos e metas claras
            6. Adaptar planos baseado no progresso do estudante
            
            ## Princípios de Planejamento:
            
            **Distribuição de Matérias por Importância:**
            - Matemática: 20% do tempo (maior peso no ENEM)
            - Português: 15% do tempo (fundamental)
            - Física/Química: 15% cada (exatas importantes)
            - Biologia/Redação: 10% cada (moderada importância)
            - Humanas: 6% cada (História, Geografia)
            - Linguagens: menor percentual (Literatura, Inglês, etc.)
            
            **Fases do Cronograma:**
            1. **Base Conceitual** (8 semanas) - Teoria e fundamentos
            2. **Prática Intensiva** (12 semanas) - Exercícios e aplicação
            3. **Revisão e Simulados** (6 semanas) - Preparação final
            4. **Reta Final** (2 semanas) - Manutenção e estratégias
            
            **Estrutura Semanal:**
            - Segunda a Sexta: Matérias principais
            - Sábado: Revisão e exercícios mistos
            - Domingo: Descanso ou revisão leve
            
            ## Diretrizes:
            
            - Sempre considere o tempo disponível do estudante
            - Seja realista com as metas e prazos
            - Inclua momentos de revisão e descanso
            - Adapte baseado no nível atual do estudante
            - Foque nas matérias com maior peso no ENEM
            - Considere a proximidade da prova
            
            Mantenha sempre foco na qualidade do planejamento pedagógico.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        """Tools específicas do StudyPlanAgent"""
        try:
            from app.agents.tools.study_plan_tools import (
                create_study_plan,
                get_study_plan,
                list_user_plans,
                update_plan_progress,
                adapt_study_plan,
                get_weekly_schedule,
                create_custom_plan,
                get_plan_analytics,
                calculate_time_distribution
            )
            
            return [
                create_study_plan,
                get_study_plan,
                list_user_plans,
                update_plan_progress,
                adapt_study_plan,
                get_weekly_schedule,
                create_custom_plan,
                get_plan_analytics,
                calculate_time_distribution
            ]
        except ImportError:
            # Fallback se as tools não estão disponíveis
            return []
    
    def get_agent_temperature(self) -> float:
        """Temperature estruturada para planejamento"""
        return 0.3
    
    def get_max_output_tokens(self) -> int:
        """Limite de tokens para planos detalhados"""
        return 3000
    
    def get_intensity_info(self) -> Dict[str, Any]:
        """Retorna informações do nível de intensidade atual"""
        return self.INTENSITY_LEVELS[self.intensity]
    
    def get_subject_weights_info(self) -> Dict[str, Any]:
        """Retorna informações dos pesos das matérias"""
        return self.SUBJECT_WEIGHTS
    
    def get_study_phases_info(self) -> Dict[str, Any]:
        """Retorna informações das fases de estudo"""
        return self.STUDY_PHASES
    
    def calculate_hours_distribution(self, total_hours: int) -> Dict[str, int]:
        """
        Calcula a distribuição de horas entre as matérias.
        
        Args:
            total_hours: Total de horas disponíveis para estudo
            
        Returns:
            Dicionário com horas por matéria
        """
        distribution = {}
        
        for subject, info in self.SUBJECT_WEIGHTS.items():
            hours = int(total_hours * info['weight'])
            distribution[subject] = max(1, hours)  # Mínimo 1 hora por matéria
        
        return distribution
    
    def create_weekly_template(self, total_hours_per_week: int) -> Dict[str, List[str]]:
        """
        Cria um template semanal de estudos.
        
        Args:
            total_hours_per_week: Horas totais por semana
            
        Returns:
            Template semanal com distribuição por dia
        """
        intensity_info = self.INTENSITY_LEVELS[self.intensity]
        hours_per_day = intensity_info['hours_per_day']
        days_per_week = intensity_info['days_per_week']
        
        # Distribui as matérias pelos dias da semana
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        weekly_template = {}
        
        # Matérias principais nos dias úteis
        main_subjects = ['matematica', 'portugues', 'fisica', 'quimica', 'biologia']
        
        for i, day in enumerate(days[:days_per_week]):
            if i < len(main_subjects):
                subject = main_subjects[i]
                subject_name = self.SUBJECT_WEIGHTS[subject]['description']
                weekly_template[day] = [f"{subject_name} ({hours_per_day}h)"]
            elif day == 'Sábado':
                weekly_template[day] = [f"Revisão e Simulados ({hours_per_day}h)"]
            else:
                weekly_template[day] = [f"Estudo Complementar ({hours_per_day}h)"]
        
        # Domingo como descanso ou revisão leve
        if 'Domingo' not in weekly_template and days_per_week < 7:
            weekly_template['Domingo'] = ['Descanso ou Revisão Leve']
        
        return weekly_template


def get_study_plan_agent(
    intensity: str = 'moderate',
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = True
):
    """
    Factory function para criar um StudyPlanAgent.
    
    Args:
        intensity: Nível de intensidade ('light', 'moderate', 'intensive', 'extreme')
        model_id: Modelo Gemini a usar
        user_id: ID do usuário
        session_id: ID da sessão
        debug_mode: Modo debug
        
    Returns:
        Agent configurado para criação de planos de estudo ENEM
    """
    study_plan = StudyPlanAgent(intensity=intensity)
    return study_plan.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode
    )


def get_light_study_plan_agent(**kwargs):
    """Factory para plano de estudos leve"""
    return get_study_plan_agent(intensity='light', **kwargs)


def get_moderate_study_plan_agent(**kwargs):
    """Factory para plano de estudos moderado"""
    return get_study_plan_agent(intensity='moderate', **kwargs)


def get_intensive_study_plan_agent(**kwargs):
    """Factory para plano de estudos intensivo"""
    return get_study_plan_agent(intensity='intensive', **kwargs)


def get_extreme_study_plan_agent(**kwargs):
    """Factory para plano de estudos extremo"""
    return get_study_plan_agent(intensity='extreme', **kwargs)


def calculate_study_duration(target_date: str, intensity: str = 'moderate') -> Dict[str, Any]:
    """
    Calcula a duração e distribuição do plano baseado na data objetivo.
    
    Args:
        target_date: Data objetivo no formato 'YYYY-MM-DD'
        intensity: Nível de intensidade
        
    Returns:
        Informações de duração e distribuição
    """
    agent = StudyPlanAgent(intensity=intensity)
    
    try:
        target = datetime.strptime(target_date, '%Y-%m-%d')
        today = datetime.now()
        
        if target <= today:
            return {"error": "Data objetivo deve ser futura"}
        
        days_available = (target - today).days
        weeks_available = days_available // 7
        
        intensity_info = agent.INTENSITY_LEVELS[intensity]
        total_hours = weeks_available * intensity_info['total_hours_per_week']
        
        hours_distribution = agent.calculate_hours_distribution(total_hours)
        
        return {
            "target_date": target_date,
            "days_available": days_available,
            "weeks_available": weeks_available,
            "intensity": intensity,
            "total_hours": total_hours,
            "hours_per_week": intensity_info['total_hours_per_week'],
            "hours_distribution": hours_distribution,
            "weekly_template": agent.create_weekly_template(intensity_info['total_hours_per_week'])
        }
        
    except ValueError:
        return {"error": "Formato de data inválido. Use YYYY-MM-DD"}


def get_intensity_recommendations(available_hours_per_week: int) -> Dict[str, Any]:
    """
    Recomenda o nível de intensidade baseado no tempo disponível.
    
    Args:
        available_hours_per_week: Horas disponíveis por semana
        
    Returns:
        Recomendações de intensidade
    """
    agent = StudyPlanAgent()
    recommendations = []
    
    for intensity, info in agent.INTENSITY_LEVELS.items():
        if available_hours_per_week >= info['total_hours_per_week']:
            recommendations.append({
                "intensity": intensity,
                "description": info['description'],
                "suitable": True,
                "hours_needed": info['total_hours_per_week']
            })
        else:
            recommendations.append({
                "intensity": intensity,
                "description": info['description'],
                "suitable": False,
                "hours_needed": info['total_hours_per_week'],
                "hours_missing": info['total_hours_per_week'] - available_hours_per_week
            })
    
    # Encontra a melhor recomendação
    suitable_options = [r for r in recommendations if r['suitable']]
    best_recommendation = max(suitable_options, key=lambda x: x['hours_needed']) if suitable_options else None
    
    return {
        "available_hours": available_hours_per_week,
        "all_options": recommendations,
        "recommended": best_recommendation,
        "message": "Recomendação baseada no tempo disponível"
    }