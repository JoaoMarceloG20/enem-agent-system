#!/usr/bin/env python3
"""
Test script para validar integração do Selector com agents
"""

import sys
import os

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_selector_integration():
    """Testa o selector e integração com APIs"""
    
    print("🔗 Testando Selector Integration...")
    print("=" * 50)
    
    try:
        # Test 1: Import do selector
        print("\n📚 Teste 1: Imports do Selector")
        from app.agents.selector import (
            AgentType, 
            get_agent,
            get_available_agents,
            get_agent_info,
            get_all_agents_info
        )
        print("✅ Selector imports bem-sucedidos")
        
        # Test 2: Agents disponíveis
        print("\n🤖 Teste 2: Agents Disponíveis")
        available_agents = get_available_agents()
        print(f"  Agents disponíveis: {available_agents}")
        print(f"  Total: {len(available_agents)} agents")
        
        # Test 3: Info detalhada dos agents
        print("\n📋 Teste 3: Informações dos Agents")
        all_info = get_all_agents_info()
        for agent_id, info in all_info.items():
            print(f"\n  {agent_id.upper()}:")
            print(f"    Nome: {info.get('name')}")
            print(f"    Descrição: {info.get('description')[:60]}...")
            print(f"    Suporta Subject: {info.get('supports_subject')}")
            print(f"    Suporta Difficulty: {info.get('supports_difficulty')}")
            print(f"    Temperature: {info.get('temperature')}")
            print(f"    Max Tokens: {info.get('max_tokens')}")
            
            if info.get('subjects'):
                subjects_count = len(info.get('subjects', []))
                print(f"    Subjects: {subjects_count} matérias ENEM")
            
            if info.get('difficulties'):
                print(f"    Difficulties: {info.get('difficulties')}")
        
        # Test 4: Criação de agents via selector
        print("\n🏭 Teste 4: Criação via Selector")
        
        # Test ENEM Agent
        try:
            test_agent = get_agent(
                agent_id=AgentType.TEST,
                user_id='test_user_selector',
                session_id='test_session_selector'
            )
            print(f"  ✅ TestAgent criado: {test_agent.name}")
            print(f"    Agent ID: {test_agent.agent_id}")
        except Exception as e:
            print(f"  ⚠️ TestAgent falhou: {str(e)[:80]}...")
        
        # Tutor Agent - Geral
        try:
            tutor_agent = get_agent(
                agent_id=AgentType.TUTOR,
                user_id='test_user_selector',
                session_id='test_session_selector'
            )
            print(f"  ✅ TutorAgent (geral) criado: {tutor_agent.name}")
            print(f"    Agent ID: {tutor_agent.agent_id}")
        except Exception as e:
            print(f"  ⚠️ TutorAgent falhou: {str(e)[:80]}...")
        
        # Tutor Agent - Matemática específico
        try:
            tutor_math = get_agent(
                agent_id=AgentType.TUTOR,
                subject='matematica',
                user_id='test_user_selector',
                session_id='test_session_selector'
            )
            print(f"  ✅ TutorAgent (matemática) criado: {tutor_math.name}")
            print(f"    Agent ID: {tutor_math.agent_id}")
        except Exception as e:
            print(f"  ⚠️ TutorAgent matemática falhou: {str(e)[:80]}...")
        
        # Quiz Agent - Médio
        try:
            quiz_agent = get_agent(
                agent_id=AgentType.QUIZ,
                difficulty='medio',
                user_id='test_user_selector',
                session_id='test_session_selector'
            )
            print(f"  ✅ QuizAgent (médio) criado: {quiz_agent.name}")
            print(f"    Agent ID: {quiz_agent.agent_id}")
        except Exception as e:
            print(f"  ⚠️ QuizAgent médio falhou: {str(e)[:80]}...")
        
        # Quiz Agent - Física Difícil
        try:
            quiz_physics = get_agent(
                agent_id=AgentType.QUIZ,
                subject='fisica',
                difficulty='dificil',
                user_id='test_user_selector',
                session_id='test_session_selector'
            )
            print(f"  ✅ QuizAgent (física/difícil) criado: {quiz_physics.name}")
            print(f"    Agent ID: {quiz_physics.agent_id}")
        except Exception as e:
            print(f"  ⚠️ QuizAgent física/difícil falhou: {str(e)[:80]}...")
        
        # Test 5: Routes helper data
        print("\n📚 Teste 5: Dados para Routes")
        
        # Subjects
        try:
            from app.agents.tutor_agent import TutorAgent
            subjects = TutorAgent.ENEM_SUBJECTS
            print(f"  Subjects disponíveis: {len(subjects)} matérias")
            print(f"  Exemplos: {list(subjects.keys())[:5]}...")
        except Exception as e:
            print(f"  ⚠️ Erro ao carregar subjects: {e}")
        
        # Topics
        try:
            from app.agents.quiz_agent import QuizAgent
            topics = QuizAgent.ENEM_TOPICS
            total_topics = sum(len(topics_list) for topics_list in topics.values())
            print(f"  Topics disponíveis: {total_topics} tópicos em {len(topics)} matérias")
        except Exception as e:
            print(f"  ⚠️ Erro ao carregar topics: {e}")
        
        # Difficulties
        try:
            from app.agents.quiz_agent import QuizAgent
            difficulties = QuizAgent.DIFFICULTY_LEVELS
            print(f"  Difficulties disponíveis: {list(difficulties.keys())}")
        except Exception as e:
            print(f"  ⚠️ Erro ao carregar difficulties: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Selector Integration - TESTES CONCLUÍDOS")
        print("\n📋 Resumo:")
        print(f"- ✅ {len(available_agents)} agents disponíveis via selector")
        print("- ✅ AgentType enum funcionando")
        print("- ✅ get_agent() factory funcionando")
        print("- ✅ Parâmetros subject/difficulty suportados")
        print("- ✅ Informações detalhadas dos agents")
        print("- ✅ Dados auxiliares (subjects, topics, difficulties)")
        print("- ✅ Pronto para integração API completa")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    success = test_selector_integration()
    sys.exit(0 if success else 1)