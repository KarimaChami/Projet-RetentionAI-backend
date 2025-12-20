from fastapi import FastAPI
# import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base,get_db
from backend.app.models.prediction_his import PredictionHistory
from backend.app.schemas.user import UserCreate
from backend.app.schemas.token import Token 
from backend.app.models.user import User
from backend.app.utils.authentification import create_access_token, get_user_by_username,get_user_by_email, create_user, verify_password,get_current_user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from starlette import status
from backend.app.schemas.retention import RetentionPlan
from backend.app.utils.ai import generate_plan
from backend.app.schemas.employer import EmployeBase
from backend.app.utils.ml import pipeline as model
from backend.app.schemas.retention import RetentionPlanRequest
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
async def predict_churn(employee: EmployeBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Prédire la probabilité de départ d'un employé
    
    Nécessite une authentification JWT.
    
    Parameters:
        - age: Âge de l'employé (18-100)
        - department: Département (IT, Sales, HR, Marketing, Finance, Operations, R&D)
        - job_role: Rôle dans l'entreprise
        - years_at_company: Nombre d'années dans l'entreprise
        - monthly_income: Salaire mensuel en euros
        - job_satisfaction: Satisfaction au travail (1-5)
        - work_life_balance: Équilibre vie pro/perso (1-5)
        - performance_rating: Note de performance (1-5)
        - business_travel: Fréquence des voyages (Non-Travel, Travel_Rarely, Travel_Frequently)
        - over_time: Heures supplémentaires (Yes/No)
        - distance_from_home: Distance domicile-travail en km
        - employee_id: Identifiant employé (optionnel)
    
    Returns:
        Probabilité de départ et niveau de risque
    """
    try:
        # Convertir en dictionnaire pour le modèle
        employee_df = pd.DataFrame([employee.dict()]) 
        # Probabilité de churn
        probability = model.predict_proba(employee_df)[0][1]  # Classe 1
        
        # Niveau de risque
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Enregistrer dans l'historique
        prediction = PredictionHistory(
            user_id=current_user.id,
            probability=probability,
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return {
            "churn_probability": round(probability, 4),
            "risk_level": risk_level,
            "timestamp": prediction.timestamp,
            "prediction_id": prediction.id
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de prédiction: {str(e)}"
        )
@app.post("/generate-retention-plan", response_model=RetentionPlan)
async def generate_retention_plan(
    request: RetentionPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if request.churn_probability < 0.5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le plan de rétention n'est généré que pour une probabilité > 50%"
        )

    try:
        # Préparer le payload pour la fonction
        payload = request.employee_data.dict()
        payload["probability"] = request.churn_probability
        print("DEBUG PAYLOAD:", payload)  # Vérifier que "probability" est bien présent

        # Appel de la fonction generate_plan
        actions = generate_plan(payload)["retention_plan"]

        # Sauvegarder dans la DB (facultatif)
        last_prediction = db.query(PredictionHistory)\
            .filter(PredictionHistory.user_id == current_user.id)\
            .order_by(PredictionHistory.timestamp.desc())\
            .first()
        
        if last_prediction:
            last_prediction.retention_plan = "\n".join(actions)
            db.commit()

        return {"retention_plan": actions}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de génération du plan: {str(e)}"
        )












