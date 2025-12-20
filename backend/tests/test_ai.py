# tests/test_ai.py
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.utils.ai import generate_plan
import json

def test_generate_plan_high_churn(mocker):
    payload = {
        "Age": 30,
        "Department": "IT",
        "JobRole": "Engineer",
        "MonthlyIncome": 5000,
        "WorkLifeBalance": 3,
        "probability": 0.8
    }

    # On mocke requests.post pour simuler une réponse de Hugging Face
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "RetentionPlan": [
                            "Point 1",
                            "Point 2",
                            "Point 3",
                            "Point 4"
                        ]
                    })
                }
            }
        ]
    }
    
    mocker.patch("backend.app.utils.ai.requests.post", return_value=fake_response)

    plan = generate_plan(payload)
    assert "retention_plan" in plan
    assert len(plan["retention_plan"]) == 4
    assert plan["retention_plan"] == ["Point 1", "Point 2", "Point 3", "Point 4"]

def test_generate_plan_low_churn():
    payload = {
        "Age": 30,
        "Department": "IT",
        "JobRole": "Engineer",
        "MonthlyIncome": 5000,
        "WorkLifeBalance": 3,
        "probability": 0.3
    }
    
    plan = generate_plan(payload)
    # Pour churn < 0.5, le plan doit être vide
    assert plan["retention_plan"] == []
