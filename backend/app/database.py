from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.config import settings
from sqlalchemy.orm import declarative_base
import os

# URL de connexion
# DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", settings.DATABASE_URL)
# print(DATABASE_URL)

# Créer l'engine SQLAlchemy
engine = create_engine(settings.DATABASE_URL) 
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



