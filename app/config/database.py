from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://zaki:mySql250250$@localhost/uvicorn"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Provides a database session for the duration of a request.

    Yields:
        SessionLocal: A SQLAlchemy database session.

    Ensures that the database session is properly closed after use.
    """
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
