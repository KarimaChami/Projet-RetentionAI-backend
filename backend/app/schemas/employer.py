from pydantic import BaseModel

class EmployeBase(BaseModel):
    Age : int
    BusinessTravel:str
    Department: str
    Education:int
    EducationField: str
    Gender:str
    JobInvolvement: int
    JobLevel:int
    JobRole:str
    MonthlyRate:int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate:int
    NumCompaniesWorked:int
    PercentSalaryHike:int
    OverTime:str
    PerformanceRating: int
    StockOptionLevel: int
    TotalWorkingYears: int
    WorkLifeBalance: int
    YearsAtCompany:int
    YearsInCurrentRole: int
    YearsWithCurrManager: int
    
