"""
QuizAgent Tools

Ferramentas específicas para o QuizAgent do sistema ENEM.
Geração, correção e análise de quizzes estilo ENEM.
"""

import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agno import Agent
else:
    Agent = None


def generate_quiz_questions(
    agent, 
    subject: str, 
    num_questions: int = 5,
    difficulty: str = "medio",
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gera questões de quiz estilo ENEM.
    
    Args:
        agent: Instância do Agent
        subject: Matéria para as questões
        num_questions: Número de questões (default: 5)
        difficulty: Nível de dificuldade ('facil', 'medio', 'dificil')
        topic: Tópico específico (opcional)
        
    Returns:
        Dict com as questões geradas
    """
    # Importa tópicos do QuizAgent
    try:
        from app.agents.quiz_agent import QuizAgent
        topics_map = QuizAgent.ENEM_TOPICS
        subject_names = QuizAgent.ENEM_SUBJECTS if hasattr(QuizAgent, 'ENEM_SUBJECTS') else {}
    except ImportError:
        topics_map = {}
        subject_names = {}
    
    # Seleciona tópico aleatório se não especificado
    if not topic and subject in topics_map:
        topic = random.choice(topics_map[subject])
    elif not topic:
        topic = f"Conceitos gerais de {subject}"
    
    # Estrutura base para questões
    current_timestamp = datetime.now()
    quiz_structure = {
        "quiz_id": f"quiz_{subject}_{difficulty}_{current_timestamp.strftime('%Y%m%d_%H%M%S')}",
        "subject": subject,
        "subject_name": subject_names.get(subject, subject.title()),
        "topic": topic,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "created_at": current_timestamp.isoformat(),
        "questions": [],
        "instructions": f"""
        Quiz de {subject.title()} - Nível {difficulty.title()}
        
        - {num_questions} questões de múltipla escolha
        - Cada questão tem 5 alternativas (A, B, C, D, E)
        - Apenas uma alternativa correta por questão
        - Questões seguem o padrão ENEM
        - Tópico: {topic}
        
        Leia cada questão cuidadosamente e marque a alternativa correta.
        """
    }
    
    # Template para questões (será preenchido pelo LLM)
    for i in range(num_questions):
        question_template = {
            "question_id": f"q{i+1}",
            "number": i + 1,
            "context": f"[Contexto da questão {i+1} sobre {topic}]",
            "statement": f"[Comando da questão {i+1}]",
            "alternatives": {
                "A": "[Alternativa A]",
                "B": "[Alternativa B]", 
                "C": "[Alternativa C]",
                "D": "[Alternativa D]",
                "E": "[Alternativa E]"
            },
            "correct_answer": "[Letra correta]",
            "explanation": f"[Explicação detalhada da questão {i+1}]",
            "topic": topic,
            "difficulty": difficulty,
            "competency": f"[Competência ENEM relacionada]"
        }
        quiz_structure["questions"].append(question_template)
    
    # Salva na memória do agente se disponível
    try:
        if hasattr(agent, 'memory') and agent.memory:
            agent.memory.update_memory(
                user_id=agent.user_id,
                data={
                    "quiz_generated": quiz_structure["quiz_id"],
                    "subject": subject,
                    "difficulty": difficulty,
                    "questions_count": num_questions,
                    "generated_at": datetime.now().isoformat()
                }
            )
    except Exception as e:
        print(f"Erro ao salvar quiz na memória: {e}")
    
    return quiz_structure


def submit_quiz_answers(
    agent,
    quiz_id: str,
    answers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Submete respostas do quiz para correção.
    
    Args:
        agent: Instância do Agent
        quiz_id: ID do quiz
        answers: Dicionário com respostas (question_id -> alternativa)
        
    Returns:
        Resultado da correção com score e feedback
    """
    # Simula correção (em implementação real, recuperaria o gabarito)
    # Por agora, gera resultado simulado para demonstração
    
    total_questions = len(answers)
    correct_answers = 0
    
    # Simula correção aleatória para demonstração
    # Em implementação real, compararia com gabarito armazenado
    question_results = {}
    
    for question_id, user_answer in answers.items():
        # Simula 70% de chance de acerto para demonstração
        is_correct = random.random() > 0.3
        if is_correct:
            correct_answers += 1
        
        question_results[question_id] = {
            "user_answer": user_answer,
            "correct_answer": random.choice(["A", "B", "C", "D", "E"]),
            "is_correct": is_correct,
            "explanation": f"Explicação da questão {question_id}",
            "feedback": "Correto! Boa análise." if is_correct else "Revise este conceito."
        }
    
    # Calcula estatísticas
    score_percentage = (correct_answers / total_questions) * 100
    
    # Performance level baseado no score
    if score_percentage >= 80:
        performance_level = "Excelente"
        performance_color = "green"
    elif score_percentage >= 60:
        performance_level = "Bom"
        performance_color = "blue"
    elif score_percentage >= 40:
        performance_level = "Regular"
        performance_color = "yellow"
    else:
        performance_level = "Precisa melhorar"
        performance_color = "red"
    
    correction_result = {
        "quiz_id": quiz_id,
        "submitted_at": datetime.now().isoformat(),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "incorrect_answers": total_questions - correct_answers,
        "score_percentage": round(score_percentage, 1),
        "performance_level": performance_level,
        "performance_color": performance_color,
        "question_results": question_results,
        "overall_feedback": f"Você acertou {correct_answers} de {total_questions} questões ({score_percentage:.1f}%). {performance_level}!",
        "recommendations": [
            "Continue praticando questões similares",
            "Revise os tópicos com maior dificuldade",
            "Foque na interpretação de texto",
            "Pratique resolução de problemas passo a passo"
        ]
    }
    
    # Salva resultado na memória
    try:
        if hasattr(agent, 'memory') and agent.memory:
            agent.memory.update_memory(
                user_id=agent.user_id,
                data={
                    "quiz_completed": quiz_id,
                    "score": score_percentage,
                    "correct_answers": correct_answers,
                    "total_questions": total_questions,
                    "completed_at": datetime.now().isoformat()
                }
            )
    except Exception as e:
        print(f"Erro ao salvar resultado na memória: {e}")
    
    return correction_result


def get_quiz_statistics(agent, period_days: int = 30) -> Dict[str, Any]:
    """
    Obtém estatísticas de performance em quizzes.
    
    Args:
        agent: Instância do Agent
        period_days: Período em dias para análise
        
    Returns:
        Estatísticas detalhadas de performance
    """
    # Recupera dados de quizzes da memória
    quiz_history = []
    
    try:
        if hasattr(agent, 'memory') and agent.memory:
            memories = agent.memory.get_memories(
                user_id=agent.user_id,
                limit=100
            )
            
            # Filtra memories de quizzes
            for memory in memories:
                content = memory.get('content', {})
                if isinstance(content, dict) and 'quiz_completed' in content:
                    quiz_history.append(content)
                    
    except Exception as e:
        print(f"Erro ao recuperar estatísticas: {e}")
    
    # Calcula estatísticas
    stats = {
        "period_days": period_days,
        "total_quizzes": len(quiz_history),
        "total_questions": sum(q.get('total_questions', 0) for q in quiz_history),
        "total_correct": sum(q.get('correct_answers', 0) for q in quiz_history),
        "overall_accuracy": 0,
        "average_score": 0,
        "quiz_history": quiz_history[-10:],  # Últimos 10 quizzes
        "performance_trend": "stable",
        "subjects_performance": {},
        "recommendations": []
    }
    
    if stats["total_questions"] > 0:
        stats["overall_accuracy"] = round((stats["total_correct"] / stats["total_questions"]) * 100, 1)
    
    if quiz_history:
        scores = [q.get('score', 0) for q in quiz_history]
        stats["average_score"] = round(sum(scores) / len(scores), 1)
        
        # Analisa tendência (últimos 5 vs primeiros 5)
        if len(scores) >= 10:
            recent_avg = sum(scores[-5:]) / 5
            older_avg = sum(scores[:5]) / 5
            
            if recent_avg > older_avg + 5:
                stats["performance_trend"] = "improving"
            elif recent_avg < older_avg - 5:
                stats["performance_trend"] = "declining"
    
    # Gera recomendações baseadas na performance
    if stats["overall_accuracy"] < 50:
        stats["recommendations"].extend([
            "Revise conceitos fundamentais",
            "Pratique mais questões básicas",
            "Busque ajuda do tutor para tópicos difíceis"
        ])
    elif stats["overall_accuracy"] < 70:
        stats["recommendations"].extend([
            "Continue praticando regularmente", 
            "Foque nos tópicos com maior dificuldade",
            "Desenvolva técnicas de resolução rápida"
        ])
    else:
        stats["recommendations"].extend([
            "Excelente desempenho! Continue assim",
            "Desafie-se com questões mais difíceis",
            "Ajude outros estudantes com suas dificuldades"
        ])
    
    return stats


def get_quiz_history(agent, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Recupera histórico de quizzes realizados.
    
    Args:
        agent: Instância do Agent
        limit: Número máximo de quizzes no histórico
        
    Returns:
        Lista com histórico de quizzes
    """
    history = []
    
    try:
        if hasattr(agent, 'memory') and agent.memory:
            memories = agent.memory.get_memories(
                user_id=agent.user_id,
                limit=limit * 2  # Busca mais para filtrar
            )
            
            for memory in memories:
                content = memory.get('content', {})
                if isinstance(content, dict) and 'quiz_completed' in content:
                    history.append({
                        'quiz_id': content.get('quiz_completed'),
                        'score': content.get('score', 0),
                        'correct_answers': content.get('correct_answers', 0),
                        'total_questions': content.get('total_questions', 0),
                        'completed_at': content.get('completed_at'),
                        'accuracy': round((content.get('correct_answers', 0) / max(content.get('total_questions', 1), 1)) * 100, 1)
                    })
            
            # Ordena por data (mais recentes primeiro)
            history.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
            
    except Exception as e:
        print(f"Erro ao recuperar histórico: {e}")
    
    return history[:limit]


def get_enem_topics(subject: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Retorna tópicos disponíveis por matéria do ENEM.
    
    Args:
        subject: Matéria específica (opcional)
        
    Returns:
        Dicionário com tópicos por matéria
    """
    try:
        from app.agents.quiz_agent import QuizAgent
        topics_map = QuizAgent.ENEM_TOPICS
        
        if subject and subject in topics_map:
            return {subject: topics_map[subject]}
        
        return topics_map
        
    except ImportError:
        # Fallback básico
        fallback_topics = {
            "matematica": ["Álgebra", "Geometria", "Estatística", "Funções"],
            "portugues": ["Gramática", "Interpretação", "Literatura"],
            "fisica": ["Mecânica", "Eletricidade", "Ondulatória"],
            "quimica": ["Química Geral", "Orgânica", "Físico-Química"],
            "biologia": ["Citologia", "Genética", "Ecologia"],
        }
        
        if subject and subject in fallback_topics:
            return {subject: fallback_topics[subject]}
            
        return fallback_topics


def generate_custom_quiz(
    agent,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gera quiz customizado baseado em configurações específicas.
    
    Args:
        agent: Instância do Agent
        config: Configurações do quiz
            - subjects: List[str] - Matérias
            - topics: List[str] - Tópicos específicos
            - difficulty_distribution: Dict[str, int] - Distribuição de dificuldade
            - total_questions: int - Total de questões
            
    Returns:
        Quiz customizado
    """
    # Configurações padrão
    default_config = {
        "subjects": ["matematica"],
        "topics": [],
        "difficulty_distribution": {"facil": 2, "medio": 3, "dificil": 1},
        "total_questions": 6,
        "time_limit_minutes": 30
    }
    
    # Merge configurações
    final_config = {**default_config, **config}
    
    # Gera questões por dificuldade
    current_timestamp = datetime.now()
    custom_quiz = {
        "quiz_id": f"custom_quiz_{current_timestamp.strftime('%Y%m%d_%H%M%S')}",
        "type": "custom",
        "config": final_config,
        "created_at": current_timestamp.isoformat(),
        "questions_by_difficulty": {},
        "total_questions": final_config["total_questions"],
        "estimated_time": final_config["time_limit_minutes"]
    }
    
    # Distribui questões por dificuldade
    for difficulty, count in final_config["difficulty_distribution"].items():
        if count > 0:
            # Para cada matéria, gera questões
            questions = []
            for subject in final_config["subjects"]:
                subject_questions = generate_quiz_questions(
                    agent=agent,
                    subject=subject,
                    num_questions=count,
                    difficulty=difficulty,
                    topic=random.choice(final_config["topics"]) if final_config["topics"] else None
                )
                questions.extend(subject_questions.get("questions", []))
            
            custom_quiz["questions_by_difficulty"][difficulty] = questions[:count]
    
    # Salva configuração na memória
    try:
        if hasattr(agent, 'memory') and agent.memory:
            agent.memory.update_memory(
                user_id=agent.user_id,
                data={
                    "custom_quiz_generated": custom_quiz["quiz_id"],
                    "config": final_config,
                    "generated_at": datetime.now().isoformat()
                }
            )
    except Exception as e:
        print(f"Erro ao salvar quiz customizado: {e}")
    
    return custom_quiz


def analyze_quiz_performance(agent, subject: str) -> Dict[str, Any]:
    """
    Analisa performance detalhada em uma matéria específica.
    
    Args:
        agent: Instância do Agent
        subject: Matéria para análise
        
    Returns:
        Análise detalhada de performance
    """
    # Recupera histórico da matéria
    subject_history = []
    
    try:
        if hasattr(agent, 'memory') and agent.memory:
            memories = agent.memory.get_memories(user_id=agent.user_id)
            
            for memory in memories:
                content = memory.get('content', {})
                if (isinstance(content, dict) and 
                    content.get('subject') == subject and
                    'quiz_completed' in content):
                    subject_history.append(content)
                    
    except Exception as e:
        print(f"Erro na análise de performance: {e}")
    
    # Análise detalhada
    analysis = {
        "subject": subject,
        "analysis_date": datetime.now().isoformat(),
        "total_attempts": len(subject_history),
        "performance_metrics": {
            "average_score": 0,
            "best_score": 0,
            "worst_score": 100,
            "consistency": "stable",
            "improvement_rate": 0
        },
        "topic_performance": {},
        "difficulty_analysis": {
            "facil": {"attempted": 0, "correct": 0, "accuracy": 0},
            "medio": {"attempted": 0, "correct": 0, "accuracy": 0},
            "dificil": {"attempted": 0, "correct": 0, "accuracy": 0}
        },
        "recommendations": [],
        "next_steps": []
    }
    
    if subject_history:
        scores = [h.get('score', 0) for h in subject_history]
        analysis["performance_metrics"]["average_score"] = round(sum(scores) / len(scores), 1)
        analysis["performance_metrics"]["best_score"] = max(scores)
        analysis["performance_metrics"]["worst_score"] = min(scores)
        
        # Analisa tendência de melhoria
        if len(scores) >= 4:
            recent_scores = scores[-2:]
            older_scores = scores[:2]
            recent_avg = sum(recent_scores) / len(recent_scores)
            older_avg = sum(older_scores) / len(older_scores)
            
            analysis["performance_metrics"]["improvement_rate"] = round(recent_avg - older_avg, 1)
    
    # Gera recomendações específicas
    avg_score = analysis["performance_metrics"]["average_score"]
    
    if avg_score < 40:
        analysis["recommendations"].extend([
            f"Revise conceitos fundamentais de {subject}",
            "Pratique questões básicas diariamente",
            "Busque material didático adicional"
        ])
        analysis["next_steps"] = [
            "Identifique suas principais dificuldades",
            "Crie um cronograma de estudos focado",
            "Pratique 5 questões básicas por dia"
        ]
    elif avg_score < 70:
        analysis["recommendations"].extend([
            f"Continue praticando {subject} regularmente",
            "Foque nos tópicos com maior dificuldade",
            "Aumente gradualmente a dificuldade das questões"
        ])
        analysis["next_steps"] = [
            "Pratique questões de nível médio",
            "Revise tópicos com menor desempenho",
            "Faça simulados periódicos"
        ]
    else:
        analysis["recommendations"].extend([
            f"Excelente desempenho em {subject}!",
            "Desafie-se com questões mais difíceis",
            "Ajude outros estudantes com dificuldades"
        ])
        analysis["next_steps"] = [
            "Mantenha a consistência nos estudos",
            "Explore tópicos avançados",
            "Pratique questões interdisciplinares"
        ]
    
    return analysis


def get_difficulty_distribution(recommended_total: int = 10) -> Dict[str, int]:
    """
    Retorna distribuição recomendada de dificuldade para quizzes.
    
    Args:
        recommended_total: Total de questões desejado
        
    Returns:
        Distribuição por dificuldade seguindo padrão ENEM
    """
    # Distribuição baseada no padrão ENEM
    # 30% fácil, 50% médio, 20% difícil
    
    facil = int(recommended_total * 0.3)
    dificil = int(recommended_total * 0.2)
    medio = recommended_total - facil - dificil
    
    return {
        "facil": facil,
        "medio": medio,
        "dificil": dificil,
        "total": recommended_total,
        "distribution_info": {
            "facil": "30% - Conceitos básicos",
            "medio": "50% - Aplicação de conceitos", 
            "dificil": "20% - Análise e síntese"
        }
    }