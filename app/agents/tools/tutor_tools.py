"""
TutorAgent Tools

Ferramentas específicas para o TutorAgent do sistema ENEM.
Seguindo padrão do framework Agno para tools.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from agno import Agent


def get_conversation_history(agent: Agent, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Recupera o histórico de conversas do estudante.
    
    Args:
        agent: Instância do Agent
        limit: Número máximo de mensagens (default: 20)
        
    Returns:
        Lista com histórico de conversas formatado
    """
    try:
        # Utiliza o sistema de storage do Agent para recuperar histórico
        if hasattr(agent, 'storage') and agent.storage:
            # Recupera sessões recentes
            sessions = agent.storage.get_sessions(
                user_id=agent.user_id,
                session_id=agent.session_id
            )
            
            history = []
            for session in sessions[-limit:]:
                history.append({
                    'timestamp': session.get('created_at', datetime.now().isoformat()),
                    'message': session.get('message', ''),
                    'response': session.get('response', ''),
                    'subject': session.get('metadata', {}).get('subject', 'geral')
                })
            
            return history
        
        return []
        
    except Exception as e:
        print(f"Erro ao recuperar histórico: {e}")
        return []


def get_subject_statistics(agent: Agent, subject: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtém estatísticas de estudo por matéria.
    
    Args:
        agent: Instância do Agent
        subject: Matéria específica (opcional)
        
    Returns:
        Dicionário com estatísticas da matéria
    """
    try:
        if hasattr(agent, 'memory') and agent.memory:
            # Recupera dados de performance do usuário
            memory_data = agent.memory.get_memories(
                user_id=agent.user_id,
                limit=100
            )
            
            # Processa estatísticas
            stats = {
                'total_interactions': len(memory_data),
                'subjects_studied': [],
                'performance_trends': {},
                'study_time_distribution': {},
                'recent_activity': []
            }
            
            # Analisa padrões de estudo
            for memory in memory_data:
                content = memory.get('content', {})
                if isinstance(content, dict):
                    mem_subject = content.get('subject', 'geral')
                    if mem_subject not in stats['subjects_studied']:
                        stats['subjects_studied'].append(mem_subject)
            
            # Se subject específico foi solicitado
            if subject:
                subject_memories = [m for m in memory_data 
                                 if m.get('content', {}).get('subject') == subject]
                stats[f'{subject}_specific'] = {
                    'interactions': len(subject_memories),
                    'last_activity': subject_memories[-1].get('created_at') if subject_memories else None
                }
            
            return stats
        
        return {'message': 'Estatísticas não disponíveis'}
        
    except Exception as e:
        print(f"Erro ao obter estatísticas: {e}")
        return {'error': str(e)}


def suggest_study_topics(agent: Agent, subject: str, difficulty_level: str = 'medio') -> List[str]:
    """
    Sugere tópicos de estudo baseado no perfil do estudante.
    
    Args:
        agent: Instância do Agent
        subject: Matéria para sugestões
        difficulty_level: 'basico', 'medio', 'avancado'
        
    Returns:
        Lista de tópicos sugeridos
    """
    # Mapeamento de tópicos por matéria e nível
    topics_map = {
        'matematica': {
            'basico': [
                'Operações básicas e números',
                'Regra de três e porcentagem',
                'Geometria plana básica',
                'Funções do 1º grau'
            ],
            'medio': [
                'Funções quadráticas',
                'Trigonometria',
                'Geometria espacial',
                'Estatística e probabilidade'
            ],
            'avancado': [
                'Logaritmos e exponenciais',
                'Geometria analítica',
                'Análise combinatória',
                'Matemática financeira'
            ]
        },
        'fisica': {
            'basico': [
                'Cinemática - movimento uniforme',
                'Força e leis de Newton',
                'Energia mecânica',
                'Calor e temperatura'
            ],
            'medio': [
                'Ondas e acústica',
                'Eletricidade básica',
                'Óptica geométrica',
                'Hidrostática'
            ],
            'avancado': [
                'Eletromagnetismo',
                'Física moderna',
                'Oscilações e ondas',
                'Termodinâmica'
            ]
        },
        'quimica': {
            'basico': [
                'Estrutura atômica',
                'Tabela periódica',
                'Ligações químicas',
                'Funções inorgânicas'
            ],
            'medio': [
                'Estequiometria',
                'Soluções e concentrações',
                'Termoquímica',
                'Cinética química'
            ],
            'avancado': [
                'Equilíbrio químico',
                'Eletroquímica',
                'Química orgânica',
                'Radioatividade'
            ]
        },
        'biologia': {
            'basico': [
                'Características dos seres vivos',
                'Citologia básica',
                'Classificação dos seres vivos',
                'Fotossíntese e respiração'
            ],
            'medio': [
                'Genética mendeliana',
                'Evolução biológica',
                'Anatomia humana',
                'Ecologia'
            ],
            'avancado': [
                'Biologia molecular',
                'Biotecnologia',
                'Fisiologia comparada',
                'Genética de populações'
            ]
        },
        'portugues': {
            'basico': [
                'Classes de palavras',
                'Concordância verbal e nominal',
                'Regência verbal e nominal',
                'Ortografia e acentuação'
            ],
            'medio': [
                'Análise sintática',
                'Figuras de linguagem',
                'Interpretação de textos',
                'Variações linguísticas'
            ],
            'avancado': [
                'Sintaxe complexa',
                'Semântica e pragmática',
                'Intertextualidade',
                'Análise do discurso'
            ]
        }
    }
    
    # Retorna tópicos da matéria e nível especificados
    if subject in topics_map and difficulty_level in topics_map[subject]:
        return topics_map[subject][difficulty_level]
    
    # Fallback para matérias não mapeadas
    return [
        f'Conceitos fundamentais de {subject}',
        f'Tópicos intermediários de {subject}',
        f'Aplicações práticas de {subject}',
        f'Questões de {subject} no ENEM'
    ]


def explain_concept(agent: Agent, concept: str, subject: str, detail_level: str = 'medio') -> str:
    """
    Gera explicação detalhada de um conceito específico.
    
    Args:
        agent: Instância do Agent
        concept: Conceito a ser explicado
        subject: Matéria do conceito
        detail_level: 'basico', 'medio', 'detalhado'
        
    Returns:
        Explicação formatada do conceito
    """
    # Calculate current date safely to avoid framework conflicts
    now = datetime.now()
    current_date = now.strftime('%d/%m/%Y')
    explanation_template = f"""
    # 📚 Explicação: {concept}
    
    **Matéria:** {subject.title()}
    **Nível:** {detail_level.title()}
    **Data:** {current_date}
    
    ## Definição
    [Aqui seria integrada a explicação do conceito baseada na knowledge base]
    
    ## Importância no ENEM
    Este conceito é frequentemente cobrado no ENEM porque...
    
    ## Exemplo Prático
    Para entender melhor, considere o seguinte exemplo...
    
    ## Dica de Estudo
    Para dominar este conceito, recomendo...
    
    ## Próximos Passos
    Após entender {concept}, estude:
    1. [Conceito relacionado 1]
    2. [Conceito relacionado 2]
    3. [Aplicação prática]
    """
    
    return explanation_template


def solve_problem(agent: Agent, problem: str, subject: str, show_steps: bool = True) -> str:
    """
    Resolve um problema passo a passo.
    
    Args:
        agent: Instância do Agent
        problem: Problema a ser resolvido
        subject: Matéria do problema
        show_steps: Se deve mostrar os passos da resolução
        
    Returns:
        Solução formatada com passos
    """
    if show_steps:
        solution_template = f"""
        # 🧮 Resolução: {problem[:50]}...
        
        **Matéria:** {subject.title()}
        **Método:** Resolução passo a passo
        
        ## Análise do Problema
        Primeiro, vamos identificar o que o problema está pedindo...
        
        ## Dados Fornecidos
        - [Listar dados conhecidos]
        
        ## Fórmulas/Conceitos Necessários
        - [Listar fórmulas relevantes]
        
        ## Resolução
        
        **Passo 1:** [Primeiro passo]
        **Passo 2:** [Segundo passo]
        **Passo 3:** [Terceiro passo]
        
        ## Resposta Final
        [Resposta com explicação]
        
        ## Verificação
        Para verificar se está correto...
        
        ## Dicas para Problemas Similares
        Em questões como esta no ENEM, lembre-se de...
        """
    else:
        solution_template = f"""
        # 💡 Solução Rápida
        
        **Problema:** {problem[:100]}...
        **Resposta:** [Resposta direta]
        **Conceito-chave:** [Conceito principal utilizado]
        """
    
    return solution_template


def get_enem_subjects() -> Dict[str, str]:
    """
    Retorna todas as matérias disponíveis no ENEM.
    
    Returns:
        Dicionário com código e nome das matérias
    """
    return {
        "matematica": "Matemática e suas Tecnologias",
        "portugues": "Linguagens, Códigos e suas Tecnologias - Português", 
        "literatura": "Linguagens, Códigos e suas Tecnologias - Literatura",
        "ingles": "Linguagens, Códigos e suas Tecnologias - Inglês",
        "espanhol": "Linguagens, Códigos e suas Tecnologias - Espanhol",
        "fisica": "Ciências da Natureza e suas Tecnologias - Física",
        "quimica": "Ciências da Natureza e suas Tecnologias - Química",
        "biologia": "Ciências da Natureza e suas Tecnologias - Biologia",
        "historia": "Ciências Humanas e suas Tecnologias - História",
        "geografia": "Ciências Humanas e suas Tecnologias - Geografia",
        "filosofia": "Ciências Humanas e suas Tecnologias - Filosofia",
        "sociologia": "Ciências Humanas e suas Tecnologias - Sociologia",
        "redacao": "Redação"
    }


def switch_subject_context(agent: Agent, new_subject: str) -> Dict[str, str]:
    """
    Troca o contexto para uma nova matéria.
    
    Args:
        agent: Instância do Agent
        new_subject: Nova matéria para focar
        
    Returns:
        Confirmação da troca de contexto
    """
    enem_subjects = get_enem_subjects()
    
    if new_subject not in enem_subjects:
        return {
            'success': False,
            'message': f'Matéria "{new_subject}" não encontrada.',
            'available_subjects': list(enem_subjects.keys())
        }
    
    # Atualiza contexto na memória do agent
    try:
        if hasattr(agent, 'memory') and agent.memory:
            agent.memory.update_memory(
                user_id=agent.user_id,
                data={
                    'current_subject': new_subject,
                    'subject_name': enem_subjects[new_subject],
                    'context_changed_at': datetime.now().isoformat()
                }
            )
    except Exception as e:
        print(f"Erro ao atualizar contexto: {e}")
    
    return {
        'success': True,
        'message': f'Contexto alterado para: {enem_subjects[new_subject]}',
        'previous_subject': agent.session_id or 'geral',
        'new_subject': new_subject
    }


def get_study_recommendations(agent: Agent, subject: Optional[str] = None) -> Dict[str, Any]:
    """
    Gera recomendações personalizadas de estudo.
    
    Args:
        agent: Instância do Agent
        subject: Matéria específica (opcional)
        
    Returns:
        Recomendações estruturadas de estudo
    """
    recommendations = {
        'daily_plan': {
            'morning': 'Revisão de conceitos fundamentais (30-45 min)',
            'afternoon': 'Resolução de exercícios práticos (60 min)',
            'evening': 'Leitura e interpretação de textos (30 min)'
        },
        'weekly_goals': [
            'Completar 3 simulados parciais',
            'Revisar 2 matérias em profundidade',
            'Praticar redação (1 tema por semana)',
            'Fazer resumos dos tópicos estudados'
        ],
        'study_techniques': [
            'Técnica Pomodoro (25 min foco + 5 min pausa)',
            'Mapas mentais para conexões entre conceitos',
            'Flashcards para memorização',
            'Resolução de questões passadas do ENEM'
        ],
        'priority_subjects': [],
        'improvement_areas': []
    }
    
    # Personaliza baseado no histórico do usuário
    try:
        if hasattr(agent, 'memory') and agent.memory:
            user_data = agent.memory.get_memories(user_id=agent.user_id)
            
            # Analisa padrões de estudo para personalizar
            if user_data:
                recent_subjects = []
                for memory in user_data[-10:]:  # Últimas 10 interações
                    content = memory.get('content', {})
                    if isinstance(content, dict):
                        subj = content.get('subject')
                        if subj and subj not in recent_subjects:
                            recent_subjects.append(subj)
                
                recommendations['recent_focus'] = recent_subjects
                
        # Se subject específico foi fornecido
        if subject:
            subject_name = get_enem_subjects().get(subject, subject)
            recommendations['subject_specific'] = {
                'focus': subject_name,
                'daily_time': '45-60 minutos',
                'weekly_goals': f'Dominar 3-4 tópicos principais de {subject_name}',
                'resources': f'Livros didáticos, videoaulas e questões específicas de {subject_name}'
            }
    
    except Exception as e:
        print(f"Erro ao personalizar recomendações: {e}")
    
    return recommendations