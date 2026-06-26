from pathlib import Path
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    DATABASE_PATH = BASE_DIR.parent.parent / "db" / "attendance.db"
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLITE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
