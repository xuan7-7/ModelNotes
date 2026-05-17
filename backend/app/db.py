from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost:3306/modelnotes')

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    """建表，开发阶段直接调用，生产用 Alembic"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI 依赖注入：每个请求一个 session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
