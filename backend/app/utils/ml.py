import joblib
# import numpy as np
import pandas as pd
# from backend.app.schemas.employer import EmployeBase

pipeline = joblib.load('backend/model/rf_model.pkl')
def predict_churn(employee_dict: dict) -> float:
    """
    Prédit la probabilité de churn pour un employé
    """
    df = pd.DataFrame([employee_dict])
    
    # Ajouter toutes les colonnes manquantes avec valeur par défaut si nécessaire
    expected_columns = pipeline.feature_names_in_  # ou une liste sauvegardée
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0  # ou "Unknown" pour les str
    
    # Réordonner les colonnes selon le pipeline
    df = df[expected_columns]
    
    # Retourner la probabilité du modèle
    return float(pipeline.predict_proba(df)[0][1])

