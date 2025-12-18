from backend.app.database import Base 
from sqlalchemy import Column, Integer, String, DateTime, func
 

class User(Base):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    gender = Column(String, nullable=False)
    
 



