import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def generate_plan(payload: dict) -> dict:
    if payload.get("probability", 0) < 0.5:
        return {"retention_plan": []} # empty if no retention needed

    prompt = f"""
You are an HR expert.

Generate a SHORT retention plan for an employee at risk of leaving.
Rules:
- EXACTLY 4 bullet points
- Each bullet must be short (max 8 words)
- NO explanations
- OUTPUT JSON ONLY

FORMAT:
{{
  "RetentionPlan": [
    "Point 1",
    "Point 2",
    "Point 3",
    "Point 4"
  ]
}}

Employee data:
Age: {payload["Age"]}
Department: {payload["Department"]}
JobRole: {payload["JobRole"]}
MonthlyIncome: {payload["MonthlyIncome"]}
WorkLifeBalance: {payload["WorkLifeBalance"]}
"""

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        },
        timeout=30
    )
    data = response.json()

    try:
        # récupérer le texte de la réponse HF
        text = data["choices"][0]["message"]["content"]
        # parser le JSON renvoyé par le LLM
        plan_json = json.loads(text)
        return {"retention_plan": plan_json["RetentionPlan"]}
    except Exception as e:
        print("Error parsing HF response:", e)
        return {"retention_plan": []}  # fallback si erreur
