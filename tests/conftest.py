import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock Agno Storage to prevent connection attempts at import time (e.g. in playground.py)
mock_storage_patch = patch("agno.storage.agent.postgres.PostgresAgentStorage")
mock_storage = mock_storage_patch.start()
mock_storage.return_value = MagicMock()

mock_memory_db_patch = patch("agno.memory.v2.db.postgres.PostgresMemoryDb")
mock_memory_db = mock_memory_db_patch.start()
mock_memory_db.return_value = MagicMock()

# Mock settings
mock_settings_patch = patch("app.core.config.settings")
mock_settings = mock_settings_patch.start()
mock_settings.GOOGLE_API_KEY = "test_key"
mock_settings.SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@localhost/db"
mock_settings.gemini_model = "gemini-2.5-flash"
mock_settings.API_V1_STR = "/api/v1"
mock_settings.PROJECT_NAME = "Test Project"

# Mock app.core.db
mock_db_module = MagicMock()
mock_db_module.engine = MagicMock()
mock_db_module.get_db = MagicMock()
sys.modules["app.core.db"] = mock_db_module

# Mock psycopg2
mock_psycopg2 = MagicMock()
class MockError(Exception):
    pass
mock_psycopg2.Error = MockError
sys.modules["psycopg2"] = mock_psycopg2

# Now we can safely import app modules
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def mock_settings():
    """Mock settings to avoid needing real env vars."""
    with patch("app.core.config.settings") as mock_settings:
        mock_settings.GOOGLE_API_KEY = "test_key"
        mock_settings.SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@localhost/db"
        mock_settings.gemini_model = "gemini-2.5-flash"
        yield mock_settings

@pytest.fixture
def mock_agent_dependencies():
    """Mock external dependencies for agents (DB, Qdrant, Gemini)."""
    with patch("app.agents.base_enem_agent.PostgresAgentStorage") as mock_storage, \
         patch("app.agents.base_enem_agent.PostgresMemoryDb") as mock_memory_db, \
         patch("app.agents.base_enem_agent.Gemini") as mock_gemini, \
         patch("app.agents.base_enem_agent.Memory") as mock_memory, \
         patch("app.agents.base_enem_agent.get_enem_knowledge_base") as mock_kb, \
         patch("app.core.db.engine") as mock_db_engine: # Also mock the engine instance in db.py
        
        # Configure mocks
        mock_storage.return_value = MagicMock()
        mock_memory_db.return_value = MagicMock()
        mock_gemini.return_value = MagicMock()
        mock_memory.return_value = MagicMock()
        mock_kb.return_value = None
        
        yield {
            "storage": mock_storage,
            "memory_db": mock_memory_db,
            "gemini": mock_gemini,
            "memory": mock_memory,
            "engine": mock_db_engine
        }

@pytest.fixture
def client(mock_settings, mock_agent_dependencies):
    """Test client for FastAPI."""
    return TestClient(app)

@pytest.fixture
def mock_orchestrator_response():
    """Mock the orchestrator's process_message method."""
    with patch("app.agents.orchestrator_agent.OrchestratorAgent.process_message") as mock_process:
        yield mock_process
