#!/usr/bin/env python3
"""
Smoke tests de integração via TestClient (sem depender de serviços externos).
Executa os endpoints principais e valida respostas básicas.
"""

import os
import sys

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient

from app.main import app


def test_api_endpoints():
    client = TestClient(app)

    # Health endpoints
    resp = client.get("/api/v1/health/")
    assert resp.status_code == 200

    resp = client.get("/api/v1/health/detailed")
    assert resp.status_code == 200

    # Agents listing/info
    resp = client.get("/api/v1/agents")
    assert resp.status_code == 200
    agents_data = resp.json()
    assert "tutor" in agents_data.get("agents", [])

    resp = client.get("/api/v1/agents/info")
    assert resp.status_code == 200
    info_data = resp.json()
    assert "agents" in info_data
    assert "tutor" in info_data["agents"]

    # Subjects and quiz metadata
    resp = client.get("/api/v1/agents/subjects")
    assert resp.status_code == 200

    resp = client.get("/api/v1/agents/quiz/difficulties")
    assert resp.status_code == 200

    resp = client.get("/api/v1/agents/quiz/topics")
    assert resp.status_code == 200


if __name__ == "__main__":
    try:
        test_api_endpoints()
    except AssertionError:
        sys.exit(1)
    sys.exit(0)
