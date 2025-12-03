"""
ENEM Knowledge Management System

This module provides helpers for managing ENEM educational content
in the knowledge base, following the same patterns as dr_ubyfol.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from agno.agent import AgentKnowledge
from agno.document.chunking.agentic import AgenticChunking
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.models.google import Gemini
from agno.vectordb.qdrant import Qdrant

from app.core.config import settings
from app.core.qdrant import get_enem_subjects


def get_vector_db(collection_name: str | None = None) -> Qdrant:
    """
    Get Qdrant vector database instance for ENEM knowledge.
    
    Args:
        collection_name: Name of the collection (defaults to enem_knowledge)
        
    Returns:
        Configured Qdrant instance
    """
    collection_name = collection_name or settings.QDRANT_COLLECTION_NAME
    
    return Qdrant(
        collection=collection_name,
        url=f'http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}',
        embedder=FastEmbedEmbedder(),
    )


def get_enem_knowledge_base(
    subject: Optional[str] = None,
    pdf_filename: Optional[str] = None,
    collection_name: Optional[str] = None
) -> AgentKnowledge:
    """
    Get ENEM knowledge base for a specific subject or general content.
    
    Args:
        subject: ENEM subject (matematica, portugues, etc.)
        pdf_filename: Specific PDF file name
        collection_name: Qdrant collection name
        
    Returns:
        Configured PDFKnowledgeBase
    """
    # Default to main ENEM knowledge collection
    if not collection_name:
        if subject:
            collection_name = f'enem-{subject}'
        else:
            collection_name = settings.QDRANT_COLLECTION_NAME
    
    # Default PDF path
    data_dir = Path(__file__).parent / 'data/pdfs'
    if pdf_filename:
        pdf_path = data_dir / pdf_filename
    elif subject:
        pdf_path = data_dir / f'enem-{subject}.pdf'
    else:
        pdf_path = data_dir / 'enem-geral.pdf'
    
    # Short-circuit if PDF not available
    if not pdf_path.exists():
        return None  # type: ignore[return-value]
    
    # Create knowledge base following dr_ubyfol pattern
    return PDFKnowledgeBase(
        path=pdf_path,
        vector_db=get_vector_db(collection_name),
        reader=PDFReader(),
        chunking_strategy=AgenticChunking(
            model=Gemini(
                id='gemini-2.5-flash',
                api_key=settings.GOOGLE_API_KEY
            )
        ),
    )


def get_subject_knowledge(subject: str) -> AgentKnowledge:
    """
    Get knowledge base for a specific ENEM subject.
    
    Args:
        subject: ENEM subject identifier
        
    Returns:
        Subject-specific knowledge base
        
    Raises:
        ValueError: If subject is not valid
    """
    valid_subjects = get_enem_subjects()
    if subject not in valid_subjects:
        raise ValueError(f"Invalid ENEM subject '{subject}'. Valid subjects: {valid_subjects}")
    
    return get_enem_knowledge_base(subject=subject)


def get_unified_knowledge() -> AgentKnowledge:
    """
    Get unified ENEM knowledge base containing all subjects.
    
    Returns:
        Unified knowledge base
    """
    return get_enem_knowledge_base()


# ENEM subject metadata for knowledge organization
ENEM_SUBJECT_METADATA: Dict[str, Dict[str, Any]] = {
    'matematica': {
        'name': 'Matemática e suas Tecnologias',
        'topics': [
            'Aritmética', 'Álgebra', 'Geometria Plana', 'Geometria Espacial',
            'Trigonometria', 'Estatística', 'Probabilidade', 'Funções',
            'Progressões', 'Análise Combinatória', 'Matrizes', 'Logaritmos'
        ]
    },
    'portugues': {
        'name': 'Linguagens, Códigos e suas Tecnologias - Português',
        'topics': [
            'Interpretação de Texto', 'Gramática', 'Literatura Brasileira',
            'Figuras de Linguagem', 'Sintaxe', 'Semântica', 'Fonética',
            'Morfologia', 'Gêneros Textuais', 'Variações Linguísticas'
        ]
    },
    'literatura': {
        'name': 'Linguagens, Códigos e suas Tecnologias - Literatura',
        'topics': [
            'Escolas Literárias', 'Literatura Brasileira', 'Literatura Portuguesa',
            'Análise de Obras', 'Gêneros Literários', 'Figuras de Linguagem'
        ]
    },
    'ingles': {
        'name': 'Linguagens, Códigos e suas Tecnologias - Inglês',
        'topics': [
            'Interpretação de Textos', 'Vocabulário', 'Gramática',
            'Compreensão Textual', 'Gêneros Textuais'
        ]
    },
    'espanhol': {
        'name': 'Linguagens, Códigos e suas Tecnologias - Espanhol',
        'topics': [
            'Interpretação de Textos', 'Vocabulário', 'Gramática',
            'Compreensão Textual', 'Cultura Hispânica'
        ]
    },
    'fisica': {
        'name': 'Ciências da Natureza e suas Tecnologias - Física',
        'topics': [
            'Mecânica', 'Termologia', 'Óptica', 'Ondulatória',
            'Eletromagnetismo', 'Física Moderna'
        ]
    },
    'quimica': {
        'name': 'Ciências da Natureza e suas Tecnologias - Química',
        'topics': [
            'Química Geral', 'Físico-Química', 'Química Orgânica',
            'Química Inorgânica', 'Bioquímica'
        ]
    },
    'biologia': {
        'name': 'Ciências da Natureza e suas Tecnologias - Biologia',
        'topics': [
            'Citologia', 'Genética', 'Evolução', 'Ecologia',
            'Anatomia', 'Fisiologia', 'Botânica', 'Zoologia'
        ]
    },
    'historia': {
        'name': 'Ciências Humanas e suas Tecnologias - História',
        'topics': [
            'História do Brasil', 'História Geral', 'História Contemporânea',
            'Movimentos Sociais', 'Revoluções', 'Períodos Históricos'
        ]
    },
    'geografia': {
        'name': 'Ciências Humanas e suas Tecnologias - Geografia',
        'topics': [
            'Geografia Física', 'Geografia Humana', 'Geopolítica',
            'Climatologia', 'Cartografia', 'Geografia do Brasil'
        ]
    },
    'filosofia': {
        'name': 'Ciências Humanas e suas Tecnologias - Filosofia',
        'topics': [
            'Filosofia Antiga', 'Filosofia Medieval', 'Filosofia Moderna',
            'Filosofia Contemporânea', 'Ética', 'Política', 'Estética'
        ]
    },
    'sociologia': {
        'name': 'Ciências Humanas e suas Tecnologias - Sociologia',
        'topics': [
            'Teorias Sociológicas', 'Movimentos Sociais', 'Cultura',
            'Estratificação Social', 'Trabalho', 'Poder e Política'
        ]
    },
    'redacao': {
        'name': 'Redação',
        'topics': [
            'Dissertação Argumentativa', 'Competências ENEM',
            'Estrutura Textual', 'Argumentação', 'Proposta de Intervenção'
        ]
    }
}
