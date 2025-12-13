"""
Essay Agent API Routes

Rotas específicas para o EssayGraderAgent com endpoints otimizados para frontend.
Inclui funcionalidades de correção automática de redações estilo ENEM.
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field

from app.agents.selector import get_agent, AgentType
from app.api.models import (
    AgentRunRequest,
    AgentRunMetadata,
    StatusEnum,
    BaseResponse,
    ErrorResponse
)

router = APIRouter()

# Essay-specific models
class EssayInfoResponse(BaseResponse):
    """Response for essay agent information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_name: str
    description: str
    competencies: List[Dict[str, Any]]
    scoring_system: Dict[str, Any]
    capabilities: List[str]
    supported_themes: List[str]

class EssaySubmissionRequest(BaseModel):
    """Request for essay grading"""
    essay_text: str = Field(..., min_length=100, max_length=5000)
    theme: Optional[str] = None
    student_id: Optional[str] = None
    session_id: Optional[str] = None
    detailed_feedback: bool = True

class CompetencyScore(BaseModel):
    """Score for individual competency"""
    competency_id: str
    name: str
    score: int
    max_score: int
    percentage: float
    feedback: str
    strengths: List[str]
    improvements: List[str]

class EssayGradingResponse(BaseResponse):
    """Response for essay grading"""
    status: StatusEnum = StatusEnum.SUCCESS
    essay_id: str
    total_score: int
    max_total_score: int
    final_percentage: float
    grade_level: str
    competency_scores: List[CompetencyScore]
    general_feedback: str
    text_statistics: Dict[str, Any]
    improvement_suggestions: List[str]
    estimated_enem_score: int
    processing_time: float

class DetailedGradingRequest(BaseModel):
    """Request for detailed essay analysis"""
    essay_text: str = Field(..., min_length=100, max_length=5000)
    theme: Optional[str] = None
    focus_competencies: Optional[List[str]] = None
    include_line_by_line: bool = False
    student_id: Optional[str] = None
    session_id: Optional[str] = None

class DetailedGradingResponse(BaseResponse):
    """Response for detailed essay analysis"""
    status: StatusEnum = StatusEnum.SUCCESS
    essay_id: str
    detailed_analysis: Dict[str, Any]
    line_by_line_feedback: Optional[List[Dict[str, Any]]]
    competency_breakdown: List[Dict[str, Any]]
    comparative_analysis: Dict[str, Any]
    improvement_roadmap: List[Dict[str, Any]]

class ScoringLevel(BaseModel):
    """Scoring level model"""
    score: int
    description: str

class RubricResponse(BaseResponse):
    """Response for rubric details"""
    status: StatusEnum = StatusEnum.SUCCESS
    competencies: List[Dict[str, Any]]
    scoring_levels: List[ScoringLevel]
    evaluation_criteria: Dict[str, List[str]]
    examples: Dict[str, str]

class SampleEssay(BaseModel):
    """Sample essay model"""
    essay_id: str
    theme: str
    score: int
    grade_level: str
    text_preview: str
    competency_highlights: List[str]
    learning_points: List[str]

class SampleEssaysResponse(BaseResponse):
    """Response for sample essays"""
    status: StatusEnum = StatusEnum.SUCCESS
    essays: List[SampleEssay]
    total_count: int
    filter_applied: Dict[str, Any]


@router.get("/info", response_model=EssayInfoResponse)
async def get_essay_info():
    """
    Get detailed information about the EssayGraderAgent.
    
    Returns:
        EssayInfoResponse: Details about the 5 ENEM competencies, scoring system,
        capabilities, and supported themes.
    """
    try:
        from app.agents.essay_grader_agent import EssayGraderAgent
        
        # Get competencies with detailed information
        competencies = []
        for comp_id, comp_data in EssayGraderAgent.ENEM_COMPETENCIES.items():
            competencies.append({
                "id": comp_id,
                "name": comp_data["name"],
                "description": comp_data["description"],
                "max_score": str(comp_data["max_score"]),
                "criteria": comp_data["criteria"]
            })
        
        # Scoring system information
        scoring_system = {
            "scale": "0 a 200 pontos por competência",
            "total_max_score": "1000 pontos",
            "score_levels": ["0", "40", "80", "120", "160", "200"],
            "grade_mapping": {
                "900-1000": "Excelente",
                "800-899": "Muito Bom", 
                "700-799": "Bom",
                "600-699": "Regular",
                "0-599": "Precisa Melhorar"
            }
        }
        
        capabilities = [
            "Correção automática nas 5 competências ENEM",
            "Feedback detalhado e personalizado",
            "Análise estatística do texto",
            "Identificação de pontos fortes e fracos",
            "Sugestões específicas de melhoria",
            "Estimativa de pontuação ENEM",
            "Análise comparativa com padrões",
            "Roadmap de desenvolvimento"
        ]
        
        supported_themes = [
            "Desafios da educação no Brasil",
            "Mobilidade urbana sustentável", 
            "Democratização do acesso à internet",
            "Combate à desinformação",
            "Inclusão digital e social",
            "Sustentabilidade ambiental",
            "Direitos humanos e cidadania",
            "Desigualdade social e econômica"
        ]
        
        return EssayInfoResponse(
            message="Informações do EssayGraderAgent recuperadas com sucesso",
            agent_name="Corretor de Redações ENEM",
            description="Corretor automático especializado em redações ENEM com avaliação nas 5 competências oficiais",
            competencies=competencies,
            scoring_system=scoring_system,
            capabilities=capabilities,
            supported_themes=supported_themes
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do corretor: {str(e)}"
        )


@router.post("/grade", response_model=EssayGradingResponse)
async def grade_essay(request: EssaySubmissionRequest):
    """
    Grade an essay using ENEM criteria across all 5 competencies.
    
    Provides comprehensive scoring, feedback for each competency, general feedback,
    and suggestions for improvement.

    Args:
        request (EssaySubmissionRequest): The essay text and optional theme.

    Returns:
        EssayGradingResponse: Detailed grading results including total score and
        individual competency scores.
    """
    try:
        start_time = datetime.now()
        
        # Create essay grader agent
        agent = get_agent(
            agent_id=AgentType.ESSAY,
            user_id=request.student_id,
            session_id=request.session_id
        )
        
        # Build grading prompt
        prompt = _build_grading_prompt(request)
        
        # Execute essay grading
        response = agent.run(prompt)
        
        # Extract content from response
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)
        
        # Parse grading results (simplified for demo)
        essay_id = str(uuid.uuid4())
        competency_scores = _parse_competency_scores(content)
        total_score = sum(score.score for score in competency_scores)
        final_percentage = (total_score / 1000) * 100
        grade_level = _calculate_grade_level(total_score)
        
        # Calculate text statistics
        text_stats = _calculate_text_statistics(request.essay_text)
        
        # Generate improvement suggestions
        improvement_suggestions = _generate_improvement_suggestions(competency_scores)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return EssayGradingResponse(
            message="Redação corrigida com sucesso",
            essay_id=essay_id,
            total_score=total_score,
            max_total_score=1000,
            final_percentage=final_percentage,
            grade_level=grade_level,
            competency_scores=competency_scores,
            general_feedback=_generate_general_feedback(competency_scores, total_score),
            text_statistics=text_stats,
            improvement_suggestions=improvement_suggestions,
            estimated_enem_score=total_score,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na correção da redação: {str(e)}"
        )


@router.post("/grade-detailed", response_model=DetailedGradingResponse)
async def grade_essay_detailed(request: DetailedGradingRequest):
    """
    Perform detailed essay analysis with comprehensive feedback.
    
    Includes structural analysis, linguistic analysis, comparative insights,
    and optionally line-by-line feedback.

    Args:
        request (DetailedGradingRequest): Essay text and configuration for detailed analysis.

    Returns:
        DetailedGradingResponse: In-depth analysis of the essay.
    """
    try:
        # Create essay grader agent
        agent = get_agent(
            agent_id=AgentType.ESSAY,
            user_id=request.student_id,
            session_id=request.session_id
        )
        
        # Build detailed analysis prompt
        prompt = _build_detailed_analysis_prompt(request)
        
        # Execute detailed analysis
        response = agent.run(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        essay_id = str(uuid.uuid4())
        
        # Generate detailed analysis components
        detailed_analysis = _generate_detailed_analysis(content, request)
        competency_breakdown = _generate_competency_breakdown(content)
        comparative_analysis = _generate_comparative_analysis(request.essay_text)
        improvement_roadmap = _generate_improvement_roadmap(competency_breakdown)
        
        line_by_line_feedback = None
        if request.include_line_by_line:
            line_by_line_feedback = _generate_line_by_line_feedback(request.essay_text)
        
        return DetailedGradingResponse(
            message="Análise detalhada da redação concluída",
            essay_id=essay_id,
            detailed_analysis=detailed_analysis,
            line_by_line_feedback=line_by_line_feedback,
            competency_breakdown=competency_breakdown,
            comparative_analysis=comparative_analysis,
            improvement_roadmap=improvement_roadmap
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na análise detalhada: {str(e)}"
        )


@router.get("/rubric-details", response_model=RubricResponse)
async def get_rubric_details():
    """
    Get detailed rubric information for essay evaluation.
    
    Returns:
        RubricResponse: Comprehensive scoring criteria for each competency,
        scoring levels description, and evaluation examples.
    """
    try:
        from app.agents.essay_grader_agent import EssayGraderAgent
        
        # Get competencies with detailed criteria
        competencies = []
        for comp_id, comp_data in EssayGraderAgent.ENEM_COMPETENCIES.items():
            competencies.append({
                "id": comp_id,
                "name": comp_data["name"],
                "description": comp_data["description"],
                "max_score": comp_data["max_score"],
                "criteria": comp_data["criteria"],
                "evaluation_focus": _get_competency_focus(comp_id)
            })
        
        # Scoring levels with descriptions
        scoring_levels = [
            {"score": 0, "description": "Demonstra desconhecimento total"},
            {"score": 40, "description": "Demonstra domínio precário"},
            {"score": 80, "description": "Demonstra domínio insuficiente"},
            {"score": 120, "description": "Demonstra domínio mediano"},
            {"score": 160, "description": "Demonstra bom domínio"},
            {"score": 200, "description": "Demonstra excelente domínio"}
        ]
        
        # Evaluation criteria by category
        evaluation_criteria = {
            "estrutura": [
                "Introdução clara e objetiva",
                "Desenvolvimento com argumentos",
                "Conclusão com proposta de intervenção"
            ],
            "linguagem": [
                "Norma culta da língua",
                "Coesão e coerência",
                "Repertório sociocultural"
            ],
            "argumentacao": [
                "Defesa consistente do ponto de vista",
                "Uso de dados e exemplos",
                "Articulação entre ideias"
            ]
        }
        
        # Examples for each scoring level
        examples = {
            "excelente": "Texto com estrutura perfeita, argumentos sólidos e linguagem exemplar",
            "bom": "Texto bem estruturado com alguns pontos de melhoria",
            "regular": "Texto com estrutura básica mas argumentos limitados",
            "insuficiente": "Texto com problemas estruturais e argumentativos"
        }
        
        return RubricResponse(
            message="Detalhes da rubrica recuperados com sucesso",
            competencies=competencies,
            scoring_levels=scoring_levels,
            evaluation_criteria=evaluation_criteria,
            examples=examples
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter detalhes da rubrica: {str(e)}"
        )


@router.get("/sample-essays", response_model=SampleEssaysResponse)
async def get_sample_essays(
    grade_level: Optional[str] = Query(None, description="Filter by grade level"),
    theme: Optional[str] = Query(None, description="Filter by theme"),
    min_score: Optional[int] = Query(None, ge=0, le=1000, description="Minimum score filter"),
    limit: int = Query(10, ge=1, le=50, description="Number of essays to return")
):
    """
    Get sample essays with different score levels and themes.
    
    Useful for students to understand scoring patterns and quality levels.

    Args:
        grade_level (Optional[str]): Filter by grade (e.g., "Excelente").
        theme (Optional[str]): Filter by essay theme.
        min_score (Optional[int]): Minimum score to include.
        limit (int): Maximum number of essays to return.

    Returns:
        SampleEssaysResponse: A list of sample essays matching the criteria.
    """
    try:
        # Generate sample essays (in real implementation, fetch from database)
        sample_essays = _generate_sample_essays(grade_level, theme, min_score, limit)
        
        filter_applied = {
            "grade_level": grade_level,
            "theme": theme,
            "min_score": min_score,
            "limit": limit
        }
        
        return SampleEssaysResponse(
            message=f"Retornados {len(sample_essays)} exemplos de redações",
            essays=sample_essays,
            total_count=len(sample_essays),
            filter_applied=filter_applied
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter redações de exemplo: {str(e)}"
        )


# Helper functions
def _build_grading_prompt(request: EssaySubmissionRequest) -> str:
    """Build prompt for essay grading"""
    theme_part = f" sobre o tema '{request.theme}'" if request.theme else ""
    
    return f"""Corrija esta redação{theme_part} seguindo os critérios das 5 competências do ENEM:

REDAÇÃO:
{request.essay_text}

Avalie cada competência de 0 a 200 pontos e forneça:
1. Pontuação por competência
2. Feedback específico para cada competência
3. Pontos fortes identificados
4. Sugestões de melhoria
5. Comentário geral da redação"""

def _build_detailed_analysis_prompt(request: DetailedGradingRequest) -> str:
    """Build prompt for detailed analysis"""
    focus_part = ""
    if request.focus_competencies:
        focus_part = f" com foco nas competências: {', '.join(request.focus_competencies)}"
    
    line_analysis = ""
    if request.include_line_by_line:
        line_analysis = "\n- Análise linha por linha com comentários específicos"
    
    return f"""Realize análise detalhada desta redação{focus_part}:

REDAÇÃO:
{request.essay_text}

Forneça:
- Análise aprofundada de cada competência
- Breakdown detalhado dos critérios
- Comparação com padrões de excelência
- Roadmap de desenvolvimento{line_analysis}"""

def _parse_competency_scores(content: str) -> List[CompetencyScore]:
    """Parse competency scores from AI response (simplified)"""
    from app.agents.essay_grader_agent import EssayGraderAgent
    
    scores = []
    for i, (comp_id, comp_data) in enumerate(EssayGraderAgent.ENEM_COMPETENCIES.items()):
        # Simulate scores (in real implementation, parse AI response)
        score = 120 + (i * 20)  # Vary scores for demo
        percentage = (score / 200) * 100
        
        scores.append(CompetencyScore(
            competency_id=comp_id,
            name=comp_data["name"],
            score=score,
            max_score=200,
            percentage=percentage,
            feedback=f"Feedback para {comp_data['name']}",
            strengths=[f"Ponto forte {i+1}", f"Ponto forte {i+2}"],
            improvements=[f"Melhoria {i+1}", f"Melhoria {i+2}"]
        ))
    
    return scores

def _calculate_grade_level(total_score: int) -> str:
    """Calculate grade level from total score"""
    if total_score >= 900:
        return "Excelente"
    elif total_score >= 800:
        return "Muito Bom"
    elif total_score >= 700:
        return "Bom"
    elif total_score >= 600:
        return "Regular"
    else:
        return "Precisa Melhorar"

def _calculate_text_statistics(text: str) -> Dict[str, Any]:
    """Calculate text statistics"""
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    return {
        "word_count": words,
        "sentence_count": sentences,
        "paragraph_count": paragraphs,
        "character_count": len(text),
        "avg_words_per_sentence": round(words / max(sentences, 1), 1),
        "reading_time_minutes": round(words / 200, 1)  # 200 words per minute
    }

def _generate_improvement_suggestions(competency_scores: List[CompetencyScore]) -> List[str]:
    """Generate improvement suggestions based on scores"""
    suggestions = []
    
    for score in competency_scores:
        if score.percentage < 70:
            suggestions.extend(score.improvements)
    
    # Add general suggestions
    suggestions.extend([
        "Pratique redações regulares sobre temas variados",
        "Leia textos de qualidade para ampliar repertório",
        "Revise regras gramaticais com mais atenção",
        "Estruture melhor os parágrafos de desenvolvimento"
    ])
    
    return suggestions[:6]  # Return top 6 suggestions

def _generate_general_feedback(competency_scores: List[CompetencyScore], total_score: int) -> str:
    """Generate general feedback for the essay"""
    avg_percentage = sum(score.percentage for score in competency_scores) / len(competency_scores)
    
    if avg_percentage >= 80:
        return "Excelente redação! Demonstra domínio sólido das competências ENEM."
    elif avg_percentage >= 70:
        return "Boa redação com pontos fortes evidentes. Continue aprimorando."
    elif avg_percentage >= 60:
        return "Redação regular com potencial de melhoria em aspectos específicos."
    else:
        return "Redação precisa de mais desenvolvimento. Foque nos pontos de melhoria."

def _generate_detailed_analysis(content: str, request: DetailedGradingRequest) -> Dict[str, Any]:
    """Generate detailed analysis"""
    return {
        "structural_analysis": {
            "introduction_quality": "Boa",
            "development_coherence": "Regular", 
            "conclusion_effectiveness": "Boa"
        },
        "linguistic_analysis": {
            "grammar_accuracy": "85%",
            "vocabulary_richness": "Moderada",
            "cohesion_devices": "Adequados"
        },
        "argumentative_analysis": {
            "thesis_clarity": "Clara",
            "evidence_quality": "Suficiente",
            "counterargument_handling": "Limitado"
        }
    }

def _generate_competency_breakdown(content: str) -> List[Dict[str, Any]]:
    """Generate detailed competency breakdown"""
    return [
        {
            "competency": "Competência 1",
            "subscore_breakdown": {
                "grammar": 80,
                "spelling": 90,
                "punctuation": 85
            },
            "specific_issues": ["Alguns desvios de concordância"],
            "improvement_priority": "Média"
        }
    ]

def _generate_comparative_analysis(essay_text: str) -> Dict[str, Any]:
    """Generate comparative analysis with standards"""
    return {
        "compared_to_grade_level": {
            "above_average": ["Estrutura textual", "Vocabulário"],
            "average": ["Argumentação"],
            "below_average": ["Proposta de intervenção"]
        },
        "percentile_ranking": 65,
        "similar_essays_performance": "Médio-alto"
    }

def _generate_improvement_roadmap(competency_breakdown: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate improvement roadmap"""
    return [
        {
            "priority": "Alta",
            "focus_area": "Competência 1 - Gramática",
            "specific_actions": [
                "Revisar concordância verbal",
                "Praticar pontuação em períodos complexos"
            ],
            "timeline": "2 semanas",
            "resources": ["Gramática específica", "Exercícios online"]
        }
    ]

def _generate_line_by_line_feedback(essay_text: str) -> List[Dict[str, Any]]:
    """Generate line by line feedback"""
    lines = essay_text.split('\n')
    feedback = []
    
    for i, line in enumerate(lines[:5]):  # First 5 lines for demo
        if line.strip():
            feedback.append({
                "line_number": i + 1,
                "text": line.strip(),
                "feedback": f"Comentário sobre a linha {i+1}",
                "suggestions": [f"Sugestão {i+1}"],
                "severity": "low" if i % 2 else "medium"
            })
    
    return feedback

def _get_competency_focus(competency_id: str) -> List[str]:
    """Get focus areas for competency"""
    focus_map = {
        "competencia_1": ["Gramática", "Ortografia", "Pontuação"],
        "competencia_2": ["Tema", "Tipo textual", "Conhecimentos"],
        "competencia_3": ["Argumentos", "Informações", "Ponto de vista"],
        "competencia_4": ["Coesão", "Coerência", "Conectivos"],
        "competencia_5": ["Proposta", "Intervenção", "Detalhamento"]
    }
    return focus_map.get(competency_id, [])

def _generate_sample_essays(grade_level: Optional[str], theme: Optional[str], 
                          min_score: Optional[int], limit: int) -> List[SampleEssay]:
    """Generate sample essays for demonstration"""
    samples = []
    
    themes = ["Educação no Brasil", "Sustentabilidade", "Tecnologia e Sociedade"]
    grades = ["Excelente", "Bom", "Regular"]
    
    for i in range(min(limit, 10)):
        score = 700 + (i * 30)
        if min_score and score < min_score:
            continue
            
        samples.append(SampleEssay(
            essay_id=f"sample_{i+1}",
            theme=themes[i % len(themes)],
            score=score,
            grade_level=grades[i % len(grades)],
            text_preview=f"Início da redação exemplo {i+1}...",
            competency_highlights=[
                f"Excelente {grades[i % len(grades)]} em competência {(i % 5) + 1}"
            ],
            learning_points=[
                f"Ponto de aprendizado {i+1}",
                f"Técnica demonstrada {i+1}"
            ]
        ))
    
    return samples