"""
Essay Grader Agent Tools

Ferramentas para o corretor de redações salvar feedback e histórico.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock database for POC
_ESSAY_DB = []

def grade_essay_competencies(text: str) -> Dict[str, Any]:
    """
    Helper para estruturar a lógica de correção (simulado).
    Na prática, o LLM faz a correção, esta tool apenas ajuda a formatar ou validar.
    
    Args:
        text: Texto da redação.
        
    Returns:
        Estrutura base para as notas.
    """
    return {
        "competencia_1": 0,
        "competencia_2": 0,
        "competencia_3": 0,
        "competencia_4": 0,
        "competencia_5": 0,
        "total": 0
    }

def save_essay_feedback(user_id: str, text: str, grades: Dict[str, int], feedback: str) -> str:
    """
    Salva a redação e o feedback gerado.
    
    Args:
        user_id: ID do usuário.
        text: Texto da redação.
        grades: Dicionário com notas por competência.
        feedback: Comentário geral.
        
    Returns:
        Mensagem de confirmação.
    """
    entry = {
        "user_id": user_id,
        "text": text[:50] + "...", # Armazena apenas o início para economizar espaço no mock
        "grades": grades,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    _ESSAY_DB.append(entry)
    total = sum(grades.values()) if isinstance(grades, dict) else 0
    return f"Redação salva com sucesso! Nota total: {total}"

def get_essay_history(user_id: str) -> str:
    """
    Retorna o histórico de redações do usuário.
    
    Args:
        user_id: ID do usuário.
        
    Returns:
        Histórico formatado.
    """
    user_essays = [e for e in _ESSAY_DB if e["user_id"] == user_id]
    
    if not user_essays:
        return "Nenhuma redação encontrada para este usuário."
    
    history = []
    for i, essay in enumerate(user_essays, 1):
        grades = essay.get("grades", {})
        total = sum(grades.values()) if isinstance(grades, dict) else 0
        date = essay["timestamp"].split("T")[0]
        history.append(f"{i}. Data: {date} - Nota: {total} - Feedback: {essay['feedback'][:30]}...")
        
    return "\n".join(history)

# Placeholder functions for imports in agent
def get_essay_statistics(user_id: str) -> str:
    return "Estatísticas não disponíveis na POC."

def suggest_essay_theme() -> str:
    return "Sugestão de tema: Os desafios da mobilidade urbana."

def get_writing_tips() -> str:
    return "Dica: Use conectivos para melhorar a coesão."

def get_enem_competencies() -> str:
    return "Competências 1 a 5 do ENEM."

def get_essay_by_id(essay_id: str) -> str:
    return "Redação não encontrada."

def analyze_text_statistics(text: str) -> str:
    return f"Texto com {len(text.split())} palavras."
