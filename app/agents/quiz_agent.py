"""
QuizAgent Implementation

Gerador e avaliador de quizzes estilo ENEM com análise de desempenho.
Cria questões contextualizadas seguindo padrões do ENEM.
"""

from textwrap import dedent
from typing import List, Any, Optional, Dict
from datetime import datetime

from app.agents.base_enem_agent import BaseENEMAgent


class QuizAgent(BaseENEMAgent):
    """
    Agente especializado em geração e avaliação de quizzes ENEM.
    
    Características:
    - Geração de questões contextualizadas estilo ENEM
    - Três níveis de dificuldade (fácil, médio, difícil)
    - Sistema de correção automática
    - Análise de performance detalhada
    - Suporte a todas as 13 matérias do ENEM
    """
    
    # Tópicos por matéria do ENEM
    ENEM_TOPICS = {
        "matematica": [
            "Aritmética", "Álgebra", "Geometria Plana", "Geometria Espacial",
            "Trigonometria", "Estatística", "Probabilidade", "Funções",
            "Progressões", "Análise Combinatória", "Matrizes", "Logaritmos"
        ],
        "portugues": [
            "Interpretação de Texto", "Gramática", "Literatura Brasileira",
            "Figuras de Linguagem", "Sintaxe", "Semântica", "Fonética",
            "Morfologia", "Gêneros Textuais", "Variações Linguísticas"
        ],
        "fisica": [
            "Mecânica", "Termologia", "Ondulatória", "Óptica", 
            "Eletricidade", "Magnetismo", "Física Moderna"
        ],
        "quimica": [
            "Química Geral", "Química Orgânica", "Físico-Química",
            "Estequiometria", "Soluções", "Termoquímica", "Cinética",
            "Equilíbrio Químico", "Eletroquímica", "Radioatividade"
        ],
        "biologia": [
            "Citologia", "Histologia", "Anatomia", "Fisiologia",
            "Genética", "Evolução", "Ecologia", "Botânica", 
            "Zoologia", "Microbiologia", "Biotecnologia"
        ],
        "historia": [
            "História Antiga", "História Medieval", "História Moderna",
            "História Contemporânea", "História do Brasil", "Historiografia"
        ],
        "geografia": [
            "Geografia Física", "Geografia Humana", "Geografia do Brasil",
            "Geopolítica", "Cartografia", "Climatologia", "Urbanização"
        ],
        "filosofia": [
            "Filosofia Antiga", "Filosofia Medieval", "Filosofia Moderna",
            "Filosofia Contemporânea", "Ética", "Política", "Estética",
            "Epistemologia", "Lógica"
        ],
        "sociologia": [
            "Teoria Sociológica", "Estratificação Social", "Cultura",
            "Movimentos Sociais", "Globalização", "Trabalho", "Família"
        ],
        "literatura": [
            "Literatura Brasileira", "Literatura Portuguesa", "Escolas Literárias",
            "Análise Literária", "Gêneros Literários", "Figuras de Linguagem"
        ],
        "ingles": [
            "Reading Comprehension", "Grammar", "Vocabulary", "Text Interpretation"
        ],
        "espanhol": [
            "Comprensión Lectora", "Gramática", "Vocabulario", "Interpretación de Textos"
        ],
        "redacao": [
            "Estrutura Textual", "Argumentação", "Coesão", "Coerência",
            "Tipos de Texto", "Proposta de Intervenção"
        ]
    }
    
    # Níveis de dificuldade
    DIFFICULTY_LEVELS = {
        "facil": {"description": "Fácil - Conceitos básicos", "weight": 0.3},
        "medio": {"description": "Médio - Aplicação de conceitos", "weight": 0.5},
        "dificil": {"description": "Difícil - Análise e síntese", "weight": 0.2}
    }
    
    def __init__(self, subject: Optional[str] = None, difficulty: str = "medio"):
        """
        Inicializa o QuizAgent.
        
        Args:
            subject: Matéria específica (opcional)
            difficulty: Nível de dificuldade ('facil', 'medio', 'dificil')
        """
        self.subject = subject
        self.difficulty = difficulty if difficulty in self.DIFFICULTY_LEVELS else "medio"
        super().__init__()
    
    def get_agent_type(self) -> str:
        """ID único do agente"""
        if self.subject:
            return f'quiz_{self.subject}_{self.difficulty}'
        return f'quiz_{self.difficulty}'
    
    def get_agent_name(self) -> str:
        """Nome do agente"""
        difficulty_name = self.DIFFICULTY_LEVELS[self.difficulty]["description"]
        
        if self.subject and self.subject in self.ENEM_TOPICS:
            from .tutor_agent import TutorAgent
            subject_name = TutorAgent.ENEM_SUBJECTS.get(self.subject, self.subject.title())
            return f'Quiz ENEM - {subject_name} ({difficulty_name})'
        
        return f'Quiz ENEM - Todas as Matérias ({difficulty_name})'
    
    def get_agent_description(self) -> str:
        """Descrição do agente para o framework Agno"""
        return dedent(
            """\
            Agente especializado em geração e avaliação de quizzes estilo ENEM.
            
            Funcionalidades principais:
            - Geração de questões contextualizadas seguindo padrões do ENEM
            - Suporte a três níveis de dificuldade (fácil, médio, difícil)
            - Sistema de correção automática com feedback detalhado
            - Análise de performance por tópico e matéria
            - Questões de múltipla escolha (5 alternativas)
            - Recomendações de estudo baseadas em fraquezas identificadas
            
            Matérias cobertas:
            - Matemática e suas Tecnologias
            - Linguagens, Códigos e suas Tecnologias (Português, Literatura, Inglês, Espanhol)
            - Ciências da Natureza e suas Tecnologias (Física, Química, Biologia)
            - Ciências Humanas e suas Tecnologias (História, Geografia, Filosofia, Sociologia)
            - Redação
            
            O agente segue rigorosamente os padrões de questões do ENEM:
            - Contextualização adequada
            - Interdisciplinaridade quando apropriado  
            - Foco em competências e habilidades
            - Linguagem acessível mas precisa
            """
        )
    
    def get_agent_instructions(self) -> str:
        """Instruções específicas do agente"""
        difficulty_info = self.DIFFICULTY_LEVELS[self.difficulty]
        subject_context = ""
        
        if self.subject and self.subject in self.ENEM_TOPICS:
            from .tutor_agent import TutorAgent
            subject_name = TutorAgent.ENEM_SUBJECTS.get(self.subject, self.subject.title())
            topics = ", ".join(self.ENEM_TOPICS[self.subject][:5])  # Primeiros 5 tópicos
            subject_context = f"""
Matéria de especialização: {subject_name}
Tópicos principais: {topics}... (e outros)"""
        
        return dedent(
            f"""\
            Você é um especialista em criar e avaliar questões para o ENEM (Exame Nacional do Ensino Médio).{subject_context}
            
            Nível de dificuldade atual: {difficulty_info['description']}
            
            ## Suas Responsabilidades:
            
            1. **Geração de Questões ENEM**:
               - Criar questões de múltipla escolha com 5 alternativas (A, B, C, D, E)
               - Seguir rigorosamente o padrão ENEM: contextualizada, interdisciplinar
               - Adequar ao nível de dificuldade especificado
               - Incluir textos de apoio quando necessário (gráficos, imagens, tabelas)
               - Abordar competências e habilidades da matriz de referência do ENEM
            
            2. **Correção e Feedback**:
               - Corrigir respostas de forma precisa e justa
               - Explicar detalhadamente por que cada alternativa está correta ou incorreta
               - Fornecer feedback construtivo sobre erros
               - Identificar lacunas no conhecimento do estudante
               - Sugerir tópicos para revisão baseados nos erros
            
            3. **Análise de Performance**:
               - Calcular porcentagens de acerto por tópico
               - Identificar padrões de erro e forças do estudante
               - Gerar relatórios de performance detalhados
               - Comparar desempenho com médias esperadas
               - Sugerir estratégias de estudo personalizadas
            
            4. **Personalização de Questões**:
               - Adaptar dificuldade baseada no histórico do usuário
               - Focar em tópicos com maior dificuldade identificada
               - Criar séries de questões progressivas
               - Balancear tipos de questões (conceitual, aplicação, análise)
            
            ## Padrões de Questões ENEM:
            
            ### Estrutura Obrigatória:
            1. **Contexto/Situação-problema** (texto, gráfico, imagem)
            2. **Comando da questão** (o que está sendo perguntado)
            3. **5 alternativas** claramente identificadas (A, B, C, D, E)
            4. **Gabarito** com justificativa completa
            
            ### Características Essenciais:
            - **Contextualização**: Situações reais, cotidianas ou científicas
            - **Interdisciplinaridade**: Conectar com outras áreas quando possível
            - **Competências**: Focar nas 30 habilidades específicas de cada área
            - **Linguagem**: Clara, precisa, sem pegadinhas
            - **Distratores**: Alternativas incorretas plausíveis
            
            ### Níveis de Dificuldade:
            - **Fácil (30%)**: Conceitos básicos, aplicação direta
            - **Médio (50%)**: Aplicação de conceitos, análise simples
            - **Difícil (20%)**: Síntese, análise complexa, interdisciplinaridade
            
            ## Formato de Resposta:
            
            Para questões, use o formato:
            ```
            ## Questão [número]
            
            **Contexto:** [situação-problema]
            
            **Comando:** [pergunta específica]
            
            A) [alternativa A]
            B) [alternativa B]  
            C) [alternativa C]
            D) [alternativa D]
            E) [alternativa E]
            
            **Gabarito:** [letra correta]
            **Justificativa:** [explicação detalhada]
            **Tópico:** [tópico abordado]
            **Dificuldade:** [nível]
            ```
            
            Para correções, use:
            ```
            ## Correção - Questão [número]
            
            **Sua resposta:** [alternativa escolhida]
            **Resposta correta:** [gabarito]
            **Status:** ✅ Correto / ❌ Incorreto
            
            **Explicação:** [por que a resposta está certa/errada]
            **Dica de estudo:** [sugestão para melhorar]
            ```
            
            Mantenha sempre foco na qualidade pedagógica e na preparação eficaz para o ENEM.
            """
        )
    
    def get_agent_tools(self) -> List[Any]:
        """Tools específicas do QuizAgent"""
        # Temporariamente desabilitado para debug do datetime
        return []
    
    def get_agent_temperature(self) -> float:
        """Temperature específica para geração de questões (mais determinística)"""
        return 0.4
    
    def get_max_output_tokens(self) -> int:
        """Limite de tokens para questões detalhadas"""
        return 3000
    
    def get_subject_topics(self) -> List[str]:
        """Retorna tópicos da matéria atual"""
        if self.subject and self.subject in self.ENEM_TOPICS:
            return self.ENEM_TOPICS[self.subject]
        return []
    
    def get_difficulty_info(self) -> Dict[str, Any]:
        """Retorna informações do nível de dificuldade atual"""
        return self.DIFFICULTY_LEVELS[self.difficulty]


def get_quiz_agent(
    subject: Optional[str] = None,
    difficulty: str = "medio",
    model_id: str = 'gemini-2.5-flash',
    user_id: str = None,
    session_id: str = None,
    debug_mode: bool = False
):
    """
    Factory function para criar um QuizAgent.
    
    Args:
        subject: Matéria específica (opcional)
        difficulty: Nível de dificuldade ('facil', 'medio', 'dificil')
        model_id: Modelo Gemini a usar
        user_id: ID do usuário
        session_id: ID da sessão
        debug_mode: Modo debug
        
    Returns:
        Agent configurado para geração de quizzes ENEM
    """
    quiz = QuizAgent(subject=subject, difficulty=difficulty)
    return quiz.get_agent(
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode,
        subject=subject
    )


def get_math_quiz_agent(difficulty: str = "medio", **kwargs):
    """Factory específica para quiz de Matemática"""
    return get_quiz_agent(subject='matematica', difficulty=difficulty, **kwargs)


def get_portuguese_quiz_agent(difficulty: str = "medio", **kwargs):
    """Factory específica para quiz de Português"""
    return get_quiz_agent(subject='portugues', difficulty=difficulty, **kwargs)


def get_science_quiz_agent(subject: str, difficulty: str = "medio", **kwargs):
    """
    Factory para quiz de Ciências da Natureza.
    
    Args:
        subject: 'fisica', 'quimica', ou 'biologia'
        difficulty: Nível de dificuldade
    """
    if subject not in ['fisica', 'quimica', 'biologia']:
        raise ValueError(f"Subject deve ser 'fisica', 'quimica' ou 'biologia', recebido: {subject}")
    
    return get_quiz_agent(subject=subject, difficulty=difficulty, **kwargs)


def get_humanities_quiz_agent(subject: str, difficulty: str = "medio", **kwargs):
    """
    Factory para quiz de Ciências Humanas.
    
    Args:
        subject: 'historia', 'geografia', 'filosofia', ou 'sociologia'
        difficulty: Nível de dificuldade
    """
    if subject not in ['historia', 'geografia', 'filosofia', 'sociologia']:
        raise ValueError(f"Subject deve ser 'historia', 'geografia', 'filosofia' ou 'sociologia', recebido: {subject}")
    
    return get_quiz_agent(subject=subject, difficulty=difficulty, **kwargs)


def get_easy_quiz_agent(subject: Optional[str] = None, **kwargs):
    """Factory para quiz fácil"""
    return get_quiz_agent(subject=subject, difficulty="facil", **kwargs)


def get_hard_quiz_agent(subject: Optional[str] = None, **kwargs):
    """Factory para quiz difícil"""
    return get_quiz_agent(subject=subject, difficulty="dificil", **kwargs)