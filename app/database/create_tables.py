from app.database.connection import engine
from app.database.models import Base


def create_all_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all_tables()
    print("Database tables created.")