"""
Quiz Agent Tools

Ferramentas para o agente de quiz salvar resultados e analisar performance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock database for POC
_QUIZ_RESULTS_DB = []

def save_quiz_result(user_id: str, score: float, topic: str, difficulty: str) -> str:
    """
    Salva o resultado de um quiz realizado pelo usuário.
    
    Args:
        user_id: ID do usuário.
        score: Nota obtida (0-100).
        topic: Tópico do quiz.
        difficulty: Nível de dificuldade.
        
    Returns:
        Mensagem de confirmação.
    """
    result = {
        "user_id": user_id,
        "score": score,
        "topic": topic,
        "difficulty": difficulty,
        "timestamp": datetime.now().isoformat()
    }
    _QUIZ_RESULTS_DB.append(result)
    return f"Resultado salvo com sucesso! Nota: {score} em {topic} ({difficulty})."

def get_user_performance(user_id: str, subject: Optional[str] = None) -> str:
    """
    Retorna o histórico de performance do usuário.
    
    Args:
        user_id: ID do usuário.
        subject: Filtro opcional por matéria.
        
    Returns:
        Resumo da performance.
    """
    user_results = [r for r in _QUIZ_RESULTS_DB if r["user_id"] == user_id]
    
    if not user_results:
        return "Nenhum histórico de quizzes encontrado para este usuário."
    
    total_quizzes = len(user_results)
    avg_score = sum(r["score"] for r in user_results) / total_quizzes
    
    return f"Performance do usuário {user_id}: {total_quizzes} quizzes realizados, Média: {avg_score:.1f}%"