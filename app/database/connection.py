import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "news_db")
    safe_password = quote_plus(password)
    return f"postgresql://{user}:{safe_password}@{host}:{port}/{db}"


def _mask_value(value: str) -> str:
    if not value:
        return "<empty>"
    if len(value) <= 2:
        return "*" * len(value)
    return value[0] + ("*" * (len(value) - 2)) + value[-1]


def _build_db_error_message(exc: Exception) -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "news_db")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    return (
        "Database connection failed. Verify your credentials and that PostgreSQL is running.\n"
        f"User: {user}\n"
        f"Host: {host}\n"
        f"Port: {port}\n"
        f"Database: {db}\n"
        f"Password preview: {_mask_value(password)}\n"
        f"Original error: {exc}"
    )


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

try:
    with engine.connect():
        pass
except Exception as exc:
    if DATABASE_URL.startswith("postgresql://"):
        fallback_database_url = "sqlite:///./local_dev.db"
        print(
            "PostgreSQL connection failed. Falling back to SQLite at ./local_dev.db "
            "for local development."
        )
        engine = create_engine(fallback_database_url, pool_pre_ping=True)
    else:
        raise RuntimeError(_build_db_error_message(exc)) from exc

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    return SessionLocal()

