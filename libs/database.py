import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_db_path():
    project_root = Path.home() / "AppData" / "Local" / "DesktopAppMCC"
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / "app.db"


DATABASE_URL = f"sqlite:///{get_db_path()}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(engine)
    print(f"База данных создана: {get_db_path()}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()