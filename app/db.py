from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base


def _get_database_url() -> str:
    return os.getenv("DATABASE_URL")


# Engine e Session global
engine = create_engine(
    _get_database_url(),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables from SQLAlchemy models."""
    from .models import ticket_model

    Base.metadata.create_all(bind=engine)


@contextmanager
def db_session() -> Iterator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


