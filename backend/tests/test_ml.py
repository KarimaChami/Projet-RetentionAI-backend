# tests/test_ml.py
import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.utils.ml import pipeline as model

def test_predict_output_shape():
    # Exemple de données d'entrée
    employee_dict = {
        "Age": 30,
        "BusinessTravel": "Travel_Rarely",
        "Department": "IT",
        "Education": 3,
        "EducationField": "Computer Science",
        "Gender": "Male",
        "JobInvolvement": 3,
        "JobLevel": 2,
        "JobRole": "Software Engineer",
        "MonthlyRate": 12000,
        "MaritalStatus": "Single",
        "MonthlyIncome": 5000,
        "NumCompaniesWorked": 2,
        "PercentSalaryHike": 15,
        "OverTime": "Yes",
        "PerformanceRating": 4,
        "StockOptionLevel": 1,
        "TotalWorkingYears": 8,
        "WorkLifeBalance": 3,
        "YearsAtCompany": 4,
        "YearsInCurrentRole": 2,
        "YearsWithCurrManager": 2
    }
    X = pd.DataFrame([employee_dict])
    probability = model.predict(X)

    # Assertions
    assert probability.shape[0] == 1  # 1 prédiction pour 1 employé
    assert 0 <= probability[0] <= 1   # Probabilité entre 0 et 1
