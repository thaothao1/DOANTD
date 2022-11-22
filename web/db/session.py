from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo = True
)
SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)