from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

CONNECTION_STRING = 'postgresql://postgres:postgres@localhost:5432/chat'

engine = create_engine(CONNECTION_STRING)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

sessions = {}


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
