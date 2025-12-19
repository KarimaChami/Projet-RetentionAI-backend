from pydantic import BaseModel
from datetime import datetime

class PredictionBase(BaseModel):
    probability: float
    

class PredcitionCreate(PredictionBase):
    user_id: int
    employee_id: int
    

class PredictionResponse(PredictionBase):
    id: int
    createdAt: datetime

