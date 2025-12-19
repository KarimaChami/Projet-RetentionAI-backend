from pydantic import BaseModel

# class RetentionBase(BaseModel):
#     employee_id: int

class RetentionPlan(BaseModel):
    retention_plan: list[str]