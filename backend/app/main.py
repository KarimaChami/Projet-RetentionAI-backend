from fastapi import FastAPI
# import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base,get_db
from backend.app.schemas.user import UserCreate
from backend.app.schemas.token import Token 
from backend.app.models.user import User
from backend.app.utils.authentification import create_access_token, get_user_by_username,get_user_by_email, create_user, verify_password,get_current_user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from starlette import status
# from backend.app.schemas.employer import EmployeBase
# from backend.app.schemas.prediction import PredictionResponse
from backend.app.schemas.retention import RetentionPlan
# from backend.app.models.prediction_his import PredictionHistory
from backend.app.utils.ml import predict_churn
from backend.app.utils.ai import generate_plan
# from backend.app.schemas.employer import EmployeBase
# from backend.app.models.employer import Employee
from backend.app.schemas.employer import EmployeBase
from backend.app.utils.ml import pipeline as model

Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS - Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username )
    existing_email = get_user_by_email(db,user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    if existing_email:
        raise HTTPException(status_code=400, detail="this email already used")
    
    new_user = create_user(db, user)
    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token,"token_type": "bearer"}



@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)  
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/predict')
def predict(employe: EmployeBase, db: Session = Depends(get_db)):
    FEATURE_COLUMNS = [
    "Age",
    "BusinessTravel",
    "Department",
    "Education",
    "EducationField",
    "Gender",
    "JobInvolvement",
    "JobLevel",
    "JobRole",
    "MonthlyRate",
    "MaritalStatus",
    "MonthlyIncome",
    "MonthlyRate",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "OverTime",
    "PerformanceRating",
    "StockOptionLevel",
    "TotalWorkingYears",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsWithCurrManager"
    ]
    data_dict = employe.dict()
    X = pd.DataFrame([data_dict], columns=FEATURE_COLUMNS)

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }
    
    

# @app.post("/generate_retention_plan", response_model=RetentionPlan)
# def generate_retention_plan(request:RetentionPlan , db: Session = Depends(get_db)):
#     plan = generate_plan(request.dict())
#     return plan

@app.post("/generate-retention-plan", response_model=RetentionPlan)
def generate_retention_plan_endpoint(employee: EmployeBase, db: Session = Depends(get_db)):

    proba = predict_churn(employee.dict())
    payload = employee.dict()
    payload["probability"] = proba
    payload["prediction"] = 1 if proba > 0.5 else 0  # <-- ajouter ceci
    plan_dict = generate_plan(payload)

    return RetentionPlan(**plan_dict)










