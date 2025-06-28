
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from qdrant_client import QdrantClient
import redis
from app.core.config import settings

# --- PostgreSQL (SQLAlchemy) ---
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Qdrant Client ---
qdrant_client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

# --- Redis Client ---
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
