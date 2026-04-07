from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(url=settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, class_=Session)


def get_session():
    with SessionLocal() as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
