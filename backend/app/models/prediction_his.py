from backend.app.database import Base 
from sqlalchemy import Column , Integer , ForeignKey  , DateTime , Float
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(Integer)
    probability = Column(Float)
    user = relationship("User", back_populates="predictions")
    employe = relationship("Employe", back_populates="predictions")