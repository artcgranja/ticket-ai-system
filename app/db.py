from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

from .models.base import Base


def _get_database_url() -> str:
    # Load environment variables from .env if present
    load_dotenv()
    return os.getenv(
        "DATABASE_URL",
        # Fallback to a sensible default used elsewhere in the app
        "postgresql://postgres:postgres@localhost:5432/ticket_ai?sslmode=disable",
    )


# Engine e Session global
engine = create_engine(
    _get_database_url(),
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global, thread-safe scoped session registry
# Usage across the app: from app.db import session
session = scoped_session(SessionLocal)


def init_db() -> None:
    """Create all tables from SQLAlchemy models."""
    from .models import ticket_model

    Base.metadata.create_all(bind=engine)


@contextmanager
def db_session() -> Iterator:
    session_instance = SessionLocal()
    try:
        yield session_instance
        session_instance.commit()
    except Exception:
        session_instance.rollback()
        raise
    finally:
        session_instance.close()


def remove_session() -> None:
    """Remove the current thread-local session.

    Call this on application shutdown or at the end of a request lifecycle
    when running in a web server to avoid connection leaks.
    """
    session.remove()


