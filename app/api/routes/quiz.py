"""
Quiz Agent API Routes

Rotas específicas para o QuizAgent com endpoints otimizados para frontend.
Inclui funcionalidades de geração e avaliação de quizzes estilo ENEM.
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field

from app.agents.selector import get_agent, AgentType
from app.api.models import (
    AgentRunRequest,
    QuizResponse,
    QuizQuestion,
    AgentRunMetadata,
    StatusEnum,
    BaseResponse,
    SubjectEnum,
    DifficultyEnum,
    ErrorResponse
)
from app.utils.quiz_parser import parse_quiz_content, QuizParsingError

router = APIRouter()

# Quiz-specific models
class QuizInfoResponse(BaseResponse):
    """Response for quiz agent information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_name: str
    description: str
    supported_subjects: List[Dict[str, str]]
    difficulty_levels: List[Dict[str, str]]
    capabilities: List[str]
    total_topics: int

class QuizGenerationRequest(BaseModel):
    """Request for quiz generation"""
    subject: Optional[SubjectEnum] = None
    difficulty: DifficultyEnum = DifficultyEnum.MEDIO
    num_questions: int = Field(5, ge=1, le=20)
    topics: Optional[List[str]] = None
    time_limit: Optional[int] = Field(None, description="Time limit in minutes")
    focus_areas: Optional[List[str]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class QuizGenerationResponse(QuizResponse):
    """Enhanced response for quiz generation"""
    total_questions: int
    estimated_time: int  # minutes
    difficulty_distribution: Dict[str, int]
    topics_covered: List[str]
    quiz_id: str
    instructions: str

class QuizSubmissionRequest(BaseModel):
    """Request for quiz submission"""
    quiz_id: str
    answers: Dict[str, str]  # question_id -> selected_answer
    time_taken: Optional[int] = None  # seconds
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class QuizResultResponse(BaseResponse):
    """Response for quiz results"""
    status: StatusEnum = StatusEnum.SUCCESS
    quiz_id: str
    total_questions: int
    correct_answers: int
    score_percentage: float
    grade: str
    detailed_results: List[Dict[str, Any]]
    performance_analysis: Dict[str, Any]
    recommendations: List[str]
    time_taken: Optional[int]

class QuickQuizResponse(BaseResponse):
    """Response for quick quiz generation"""
    status: StatusEnum = StatusEnum.SUCCESS
    question: QuizQuestion
    quiz_session_id: str
    context: Dict[str, Any]

class TopicsResponse(BaseResponse):
    """Response for topics by subject"""
    status: StatusEnum = StatusEnum.SUCCESS
    subject: str
    subject_name: str
    topics: List[Dict[str, Any]]
    total_count: int


class QuizDifficultyResponse(BaseResponse):
    """Response for quiz difficulty metadata"""
    status: StatusEnum = StatusEnum.SUCCESS
    difficulties: List[Dict[str, Any]]


@router.get("/info", response_model=QuizInfoResponse)
async def get_quiz_info():
    """
    Get detailed information about the QuizAgent.

    Returns comprehensive information about capabilities, subjects, and configuration.
    """
    try:
        from app.agents.quiz_agent import QuizAgent
        from app.agents.tutor_agent import TutorAgent

        # Get subjects with proper formatting
        subjects_data = []
        total_topics = 0
        for key, name in TutorAgent.ENEM_SUBJECTS.items():
            topic_count = len(QuizAgent.ENEM_TOPICS.get(key, []))
            subjects_data.append({
                "key": key,
                "name": name,
                "icon": _get_subject_icon(key),
                "topic_count": str(topic_count)  # Convert to string for Pydantic validation
            })
            total_topics += topic_count

        # Get difficulty levels
        difficulty_levels = []
        for key, info in QuizAgent.DIFFICULTY_LEVELS.items():
            difficulty_levels.append({
                "key": key,
                "name": info["description"],
                "weight": str(info["weight"])  # Convert to string for consistency
            })

        capabilities = [
            "Geração de questões estilo ENEM",
            "Múltiplos níveis de dificuldade",
            "Correção automática detalhada",
            "Análise de performance por tópico",
            "Explicações das alternativas",
            "Recomendações personalizadas",
            "Simulados adaptativos"
        ]

        return QuizInfoResponse(
            message="Informações do QuizAgent recuperadas com sucesso",
            agent_name="Quiz ENEM - Gerador de Questões",
            description="Gerador e avaliador de quizzes estilo ENEM com sistema de correção automática",
            supported_subjects=subjects_data,
            difficulty_levels=difficulty_levels,
            capabilities=capabilities,
            total_topics=total_topics
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do quiz: {str(e)}"
        )


@router.post("/generate", response_model=QuizGenerationResponse)
async def generate_quiz(request: QuizGenerationRequest):
    """
    Generate a custom quiz based on specified criteria.

    Creates questions tailored to subject, difficulty, and specific topics.
    """
    
    try:
        # Create quiz agent
        agent = get_agent(
            agent_id=AgentType.QUIZ,
            subject=request.subject,
            difficulty=request.difficulty,
            user_id=request.user_id,
            session_id=request.session_id
        )

        # Build generation prompt
        prompt = _build_generation_prompt(request)

        # Execute quiz generation
        response = agent.run(prompt)

        # Extract content from response
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)

        # Parse generated questions using robust parser
        try:
            questions = parse_quiz_content(
                content=content,
                expected_questions=request.num_questions,
                default_subject=request.subject,
                default_difficulty=request.difficulty
            )
        except QuizParsingError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao processar questões geradas: {str(e)}",
            )
        quiz_id = str(uuid.uuid4())

        # Calculate quiz metadata
        estimated_time = request.num_questions * 3  # 3 minutes per question
        topics_covered = request.topics or _get_default_topics(request.subject)

        # Create metadata
        metadata = AgentRunMetadata(
            agent_id="quiz",
            agent_name=agent.name,
            model_used="gemini-2.5-flash",
            temperature=0.4,
            max_tokens=3000,
            subject=request.subject,
            difficulty=request.difficulty
        )

        # Create response with questions first - content will be auto-generated
        response = QuizGenerationResponse(
            message=f"Quiz gerado com sucesso - {request.num_questions} questões",
            content="",  # Will be auto-generated from questions
            metadata=metadata,
            session_id=request.session_id or str(uuid.uuid4()),
            run_id=str(uuid.uuid4()),
            questions=questions,
            quiz_metadata={
                "generation_params": request.model_dump(),
                "created_at": datetime.now().isoformat(),
                "original_llm_content": content  # Store original for debugging
            },
            total_questions=request.num_questions,
            estimated_time=estimated_time,
            difficulty_distribution={request.difficulty: request.num_questions},
            topics_covered=topics_covered,
            quiz_id=quiz_id,
            instructions=_get_quiz_instructions(request.difficulty)
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na geração do quiz: {str(e)}"
        )


@router.get("/quick-generate", response_model=QuickQuizResponse)
async def quick_generate_question(
    subject: Optional[SubjectEnum] = Query(None),
    difficulty: DifficultyEnum = Query(DifficultyEnum.MEDIO),
    topic: Optional[str] = Query(None)
):
    """
    Quickly generate a single question for immediate practice.

    Perfect for quick study sessions and topic-specific practice.
    """
    try:
        # Create quiz agent
        agent = get_agent(
            agent_id=AgentType.QUIZ,
            subject=subject,
            difficulty=difficulty
        )

        # Build quick prompt
        if topic:
            prompt = f"Crie uma questão de {difficulty} sobre {topic}"
        elif subject:
            prompt = f"Crie uma questão de {subject} nível {difficulty}"
        else:
            prompt = f"Crie uma questão ENEM nível {difficulty}"

        # Execute generation
        response = agent.run(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        # Parse single question using robust parser
        try:
            questions = parse_quiz_content(
                content=content,
                expected_questions=1,
                default_subject=subject,
                default_difficulty=difficulty
            )
            question = questions[0]
        except QuizParsingError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao processar questão gerada: {str(e)}"
            )
        session_id = str(uuid.uuid4())

        context = {
            "subject": subject,
            "difficulty": difficulty,
            "topic": topic,
            "generated_at": datetime.now().isoformat()
        }

        return QuickQuizResponse(
            message="Questão rápida gerada com sucesso",
            question=question,
            quiz_session_id=session_id,
            context=context
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na geração rápida: {str(e)}"
        )


@router.post("/submit", response_model=QuizResultResponse)
async def submit_quiz(request: QuizSubmissionRequest):
    """
    Submit quiz answers and get detailed results with analysis.

    Provides comprehensive feedback and personalized recommendations.
    """
    try:
        # Simulate quiz grading (in real implementation, retrieve stored quiz)
        total_questions = len(request.answers)
        correct_answers = _grade_quiz(request.quiz_id, request.answers)
        score_percentage = (correct_answers / total_questions) * 100
        grade = _calculate_grade(score_percentage)

        # Generate detailed results
        detailed_results = _generate_detailed_results(request.quiz_id, request.answers)

        # Performance analysis
        performance_analysis = _analyze_performance(detailed_results, score_percentage)

        # Generate recommendations
        recommendations = _generate_recommendations(performance_analysis)

        return QuizResultResponse(
            message="Quiz avaliado com sucesso",
            quiz_id=request.quiz_id,
            total_questions=total_questions,
            correct_answers=correct_answers,
            score_percentage=score_percentage,
            grade=grade,
            detailed_results=detailed_results,
            performance_analysis=performance_analysis,
            recommendations=recommendations,
            time_taken=request.time_taken
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na avaliação do quiz: {str(e)}"
        )


@router.get("/topics/{subject}", response_model=TopicsResponse)
async def get_subject_topics(subject: SubjectEnum):
    """
    Get all available topics for a specific subject.

    Returns organized list of topics with metadata for quiz generation.
    """
    try:
        from app.agents.quiz_agent import QuizAgent
        from app.agents.tutor_agent import TutorAgent

        if subject not in QuizAgent.ENEM_TOPICS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tópicos para {subject} não encontrados"
            )

        subject_name = TutorAgent.ENEM_SUBJECTS.get(subject, subject.title())
        raw_topics = QuizAgent.ENEM_TOPICS[subject]

        # Enhance topics with metadata
        topics = []
        for i, topic in enumerate(raw_topics):
            topics.append({
                "id": f"{subject}_{i}",
                "name": topic,
                "subject": subject,
                "difficulty_available": ["facil", "medio", "dificil"],
                "estimated_questions": _estimate_available_questions(topic),
                "description": _get_topic_description(topic)
            })

        return TopicsResponse(
            message=f"Tópicos de {subject_name} recuperados com sucesso",
            subject=subject,
            subject_name=subject_name,
            topics=topics,
            total_count=len(topics)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter tópicos: {str(e)}"
        )


@router.get("/difficulties", response_model=QuizDifficultyResponse)
async def get_difficulty_levels():
    """
    Get all available difficulty levels with descriptions.

    Returns comprehensive information about each difficulty level.
    """
    try:
        from app.agents.quiz_agent import QuizAgent

        difficulties = []
        for key, info in QuizAgent.DIFFICULTY_LEVELS.items():
            difficulties.append({
                "key": key,
                "name": info["description"],
                "weight": info["weight"],
                "characteristics": _get_difficulty_characteristics(key),
                "typical_time": _get_typical_time_per_question(key)
            })
        
        return QuizDifficultyResponse(
            message="Níveis de dificuldade recuperados com sucesso",
            difficulties=difficulties
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dificuldades: {str(e)}"
        )


# Helper functions
def _get_subject_icon(subject: str) -> str:
    """Get icon for subject"""
    icons = {
        "matematica": "📊", "portugues": "📝", "literatura": "📚",
        "ingles": "🇺🇸", "espanhol": "🇪🇸", "fisica": "⚡",
        "quimica": "🧪", "biologia": "🧬", "historia": "🏛️",
        "geografia": "🌍", "filosofia": "🤔", "sociologia": "👥",
        "redacao": "✍️"
    }
    return icons.get(subject, "📖")

def _build_generation_prompt(request: QuizGenerationRequest) -> str:
    """Build prompt for quiz generation with clear examples"""
    subject_part = f" de {request.subject}" if request.subject else ""
    topics_part = f" focando em: {', '.join(request.topics)}" if request.topics else ""

    # Create few-shot examples for clarity
    example_section = """
EXEMPLO DE FORMATO ESPERADO (PARA 2 QUESTÕES):

QUESTÃO 1:
**Contexto:** [Situação-problema detalhada]

**Pergunta:** [Enunciado da questão]

**Alternativas:**
A) [Primeira alternativa]
B) [Segunda alternativa]
C) [Terceira alternativa]
D) [Quarta alternativa]
E) [Quinta alternativa]

**Gabarito:** C
**Justificativa:** [Explicação detalhada da resposta correta]
**Tópico:** [Tópico específico abordado]

QUESTÃO 2:
**Contexto:** [Situação-problema detalhada]

**Pergunta:** [Enunciado da questão]

**Alternativas:**
A) [Primeira alternativa]
B) [Segunda alternativa]
C) [Terceira alternativa]
D) [Quarta alternativa]
E) [Quinta alternativa]

**Gabarito:** A
**Justificativa:** [Explicação detalhada da resposta correta]
**Tópico:** [Tópico específico abordado]

---

"""

    return f"""Você deve criar EXATAMENTE {request.num_questions} questões{subject_part} no nível {request.difficulty}{topics_part}.

INSTRUÇÕES IMPORTANTES:
- Cada questão é INDEPENDENTE e COMPLETA
- SEMPRE gere {request.num_questions} questões diferentes (não {request.num_questions} alternativas!)
- Cada questão deve ter EXATAMENTE 5 alternativas (A, B, C, D, E)
- Siga rigorosamente o formato do exemplo abaixo

{example_section}

AGORA CRIE {request.num_questions} QUESTÕES SEGUINDO EXATAMENTE ESTE FORMATO:

Requisitos por questão:
- Contexto realista estilo ENEM
- Enunciado claro e objetivo
- 5 alternativas bem elaboradas (A, B, C, D, E)
- Apenas 1 alternativa correta
- Justificativa pedagógica completa
- Tópico específico identificado

LEMBRE-SE: Se solicitadas {request.num_questions} questões, deve gerar {request.num_questions} blocos completos de questão, cada um com suas próprias 5 alternativas."""

def _parse_generated_questions(content: str, request: QuizGenerationRequest) -> List[QuizQuestion]:
    """Parse generated questions from content"""
    # Simplified parsing for demo
    questions = []
    for i in range(request.num_questions):
        question = QuizQuestion(
            question_id=f"q_{i+1}",
            question_text=f"Questão {i+1} gerada sobre {request.subject or 'ENEM'}",
            context=f"Contexto da questão {i+1}",
            alternatives={
                "A": "Alternativa A",
                "B": "Alternativa B",
                "C": "Alternativa C",
                "D": "Alternativa D",
                "E": "Alternativa E"
            },
            correct_answer="A",
            explanation="Explicação da resposta correta",
            topic=request.topics[0] if request.topics else "Tópico geral",
            difficulty=request.difficulty,
            subject=request.subject or SubjectEnum.MATEMATICA
        )
        questions.append(question)

    return questions

def _parse_single_question(content: str, subject: Optional[SubjectEnum],
                          difficulty: DifficultyEnum, topic: Optional[str]) -> QuizQuestion:
    """Parse single question from content"""
    return QuizQuestion(
        question_id=str(uuid.uuid4()),
        question_text="Questão rápida gerada",
        context="Contexto da questão",
        alternatives={
            "A": "Alternativa A", "B": "Alternativa B", "C": "Alternativa C",
            "D": "Alternativa D", "E": "Alternativa E"
        },
        correct_answer="A",
        explanation="Explicação detalhada",
        topic=topic or "Tópico geral",
        difficulty=difficulty,
        subject=subject or SubjectEnum.MATEMATICA
    )

def _get_default_topics(subject: Optional[SubjectEnum]) -> List[str]:
    """Get default topics for subject"""
    if not subject:
        return ["Tópico geral"]

    from app.agents.quiz_agent import QuizAgent
    return QuizAgent.ENEM_TOPICS.get(subject, ["Tópico geral"])[:3]

def _get_quiz_instructions(difficulty: DifficultyEnum) -> str:
    """Get instructions for quiz difficulty"""
    instructions = {
        DifficultyEnum.FACIL: "Questões de nível básico focando em conceitos fundamentais.",
        DifficultyEnum.MEDIO: "Questões de nível intermediário com aplicação de conceitos.",
        DifficultyEnum.DIFICIL: "Questões avançadas exigindo análise e síntese."
    }
    return instructions.get(difficulty, "Questões estilo ENEM.")

def _grade_quiz(quiz_id: str, answers: Dict[str, str]) -> int:
    """Grade quiz answers (simplified)"""
    # In real implementation, retrieve stored correct answers
    return len(answers) // 2  # Simulate 50% correct

def _calculate_grade(score_percentage: float) -> str:
    """Calculate letter grade from percentage"""
    if score_percentage >= 90:
        return "Excelente"
    elif score_percentage >= 70:
        return "Bom"
    elif score_percentage >= 50:
        return "Regular"
    else:
        return "Precisa melhorar"

def _generate_detailed_results(quiz_id: str, answers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Generate detailed results for each question"""
    results = []
    for question_id, user_answer in answers.items():
        results.append({
            "question_id": question_id,
            "user_answer": user_answer,
            "correct_answer": "A",  # Simplified
            "is_correct": user_answer == "A",
            "explanation": "Explicação detalhada da resposta",
            "topic": "Tópico da questão",
            "difficulty": "medio"
        })
    return results

def _analyze_performance(detailed_results: List[Dict[str, Any]],
                        score_percentage: float) -> Dict[str, Any]:
    """Analyze performance and generate insights"""
    return {
        "overall_performance": "Boa" if score_percentage >= 70 else "Regular",
        "strong_areas": ["Álgebra", "Geometria"],
        "weak_areas": ["Estatística"],
        "time_management": "Adequado",
        "improvement_suggestions": [
            "Revisar conceitos de estatística",
            "Praticar mais questões de probabilidade"
        ]
    }

def _generate_recommendations(performance_analysis: Dict[str, Any]) -> List[str]:
    """Generate personalized recommendations"""
    return [
        "Continue praticando suas áreas fortes",
        "Foque nos tópicos identificados como fracos",
        "Faça simulados regulares para manter o ritmo",
        "Revise teoria antes de partir para exercícios"
    ]

def _estimate_available_questions(topic: str) -> int:
    """Estimate available questions for topic"""
    return 50  # Placeholder

def _get_topic_description(topic: str) -> str:
    """Get description for topic"""
    return f"Tópico importante para o ENEM: {topic}"

def _get_difficulty_characteristics(difficulty: str) -> List[str]:
    """Get characteristics of difficulty level"""
    characteristics = {
        "facil": ["Conceitos básicos", "Aplicação direta", "Pouco contexto"],
        "medio": ["Aplicação de conceitos", "Análise simples", "Contexto moderado"],
        "dificil": ["Síntese", "Análise complexa", "Alto contexto", "Interdisciplinar"]
    }
    return characteristics.get(difficulty, [])

def _get_typical_time_per_question(difficulty: str) -> str:
    """Get typical time per question for difficulty"""
    times = {
        "facil": "2-3 minutos",
        "medio": "3-4 minutos",
        "dificil": "4-5 minutos"
    }
    return times.get(difficulty, "3 minutos")
