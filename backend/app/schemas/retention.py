from pydantic import BaseModel
from .employer import EmployeBase
# class RetentionBase(BaseModel):
#     employee_id: int

class RetentionPlan(BaseModel):
    retention_plan: list[str]

class RetentionPlanRequest(BaseModel):
    employee_data: EmployeBase
    churn_probability: float