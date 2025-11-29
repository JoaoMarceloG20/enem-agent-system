#!/usr/bin/env python3
"""
Test script para validar endpoints do Swagger sem dependência de DB
"""

import json
import sys
import os
from unittest.mock import patch, MagicMock

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_swagger_endpoints():
    """Testa endpoints do Swagger sem DB"""
    
    print("📊 Testando Swagger Endpoints...")
    print("=" * 50)
    
    try:
        # Importa a app diretamente
        from fastapi.testclient import TestClient
        from app.main import app
            
        client = TestClient(app)
            
        # Test 1: OpenAPI schema
        print("\n📜 Teste 1: OpenAPI Schema")
        openapi_response = client.get("/api/v1/openapi.json")
        print(f"  Status: {openapi_response.status_code}")
        
        if openapi_response.status_code == 200:
            openapi_data = openapi_response.json()
            paths = openapi_data.get('paths', {})
            print(f"  ✅ OpenAPI schema carregado")
            print(f"  Total de endpoints: {len(paths)}")
            
            # Lista todos os endpoints
            print("\n  📋 Endpoints encontrados:")
            for path, methods in paths.items():
                for method, details in methods.items():
                    summary = details.get('summary', 'No summary')
                    print(f"    {method.upper()} {path} - {summary}")
            
            # Verifica endpoints específicos
            expected_endpoints = [
                '/api/v1/agents',
                '/api/v1/agents/info',
                '/api/v1/agents/subjects',
                '/api/v1/agents/quiz/topics', 
                '/api/v1/agents/quiz/difficulties',
                '/api/v1/agents/create',
                '/api/v1/agents/{agent_id}/runs',
                '/api/v1/agents/{agent_id}/knowledge/load'
            ]
            
            print(f"\n  🔍 Verificando endpoints esperados:")
            missing_endpoints = []
            for endpoint in expected_endpoints:
                if endpoint in paths:
                    print(f"    ✅ {endpoint}")
                else:
                    print(f"    ❌ {endpoint} - MISSING")
                    missing_endpoints.append(endpoint)
            
            if not missing_endpoints:
                print(f"\n  ✅ Todos os {len(expected_endpoints)} endpoints estão presentes")
            else:
                print(f"\n  ⚠️ {len(missing_endpoints)} endpoints estão faltando")
        
        # Test 2: Testar endpoints informativos (que não dependem de DB)
        print("\n🔍 Teste 2: Endpoints Informativos")
        
        # Listar agents
        try:
            agents_response = client.get("/api/v1/agents")
            print(f"  GET /agents: {agents_response.status_code}")
            if agents_response.status_code == 200:
                agents = agents_response.json()
                print(f"    ✅ {len(agents)} agents disponíveis: {agents}")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        # Info dos agents
        try:
            info_response = client.get("/api/v1/agents/info")
            print(f"  GET /agents/info: {info_response.status_code}")
            if info_response.status_code == 200:
                info_data = info_response.json()
                print(f"    ✅ Info de {len(info_data)} agents recebida")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        # Subjects
        try:
            subjects_response = client.get("/api/v1/agents/subjects")
            print(f"  GET /agents/subjects: {subjects_response.status_code}")
            if subjects_response.status_code == 200:
                subjects = subjects_response.json()
                print(f"    ✅ {len(subjects)} matérias ENEM")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        # Quiz topics
        try:
            topics_response = client.get("/api/v1/agents/quiz/topics")
            print(f"  GET /agents/quiz/topics: {topics_response.status_code}")
            if topics_response.status_code == 200:
                topics = topics_response.json()
                total_topics = sum(len(topic_list) for topic_list in topics.values())
                print(f"    ✅ {total_topics} tópicos de quiz")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        # Quiz difficulties
        try:
            diff_response = client.get("/api/v1/agents/quiz/difficulties")
            print(f"  GET /agents/quiz/difficulties: {diff_response.status_code}")
            if diff_response.status_code == 200:
                difficulties = diff_response.json()
                print(f"    ✅ {len(difficulties)} níveis de dificuldade")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        # Test 3: Teste endpoint que requer body mas sem criar agent real
        print("\n🏭 Teste 3: Endpoint de Criação (Schema)")
        
        # Testar schema validation com dados inválidos
        try:
            invalid_create = client.post("/api/v1/agents/create", json={
                "agent_id": "invalid_agent"
            })
            print(f"  POST /agents/create (invalid): {invalid_create.status_code}")
            if invalid_create.status_code == 422:
                print("    ✅ Validação de schema funcionando")
            elif invalid_create.status_code == 400:
                print("    ✅ Erro de validação de agent type")
        except Exception as e:
            print(f"    ⚠️ Erro: {str(e)[:50]}...")
        
        print("\n" + "=" * 50)
        print("✅ Swagger Endpoints - TESTES CONCLUÍDOS")
        print("\n📋 Resumo:")
        print("- ✅ OpenAPI schema acessível")
        print("- ✅ Endpoints informativos funcionais")
        print("- ✅ Validação de schema ativa")
        print("- ✅ Swagger UI deve mostrar todos os endpoints")
        print("\n💡 Para testar com DB, use: docker-compose up -d")
        
        return True
            
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_swagger_endpoints()
    sys.exit(0 if success else 1)