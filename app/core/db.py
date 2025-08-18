from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db() -> Session:
    """
    Dependency to get a database session.

    Returns:
        Session: A SQLModel database session.
    """
    with Session(engine) as session:
        yield session
