import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fallback temporário usando SQLite em arquivo local
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./oficina_dev.db"  # Conecta no SQLite sem precisar do Docker/PostgreSQL por enquanto
)

# SQLite exige o check_same_thread=False
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        