# Plateforme-Fullstack-RetentionAI - Prédicteur de Départ & Assistant RH 


# Backend
### Objectif:

Industrialiser un modèle de prédiction via une API FastAPI sécurisée, accessible uniquement aux utilisateurs authentifiés, avec traçabilité des appels dans PostgreSQL

##  Architecture

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py  
│   │   └── employer.py             
│   │   └── prediction.py             # Routes d'authentification
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py  
│   │   └── employer.py      
│   │   └── token.py         
│   │   └── prediction.py   
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ai.py    
│   │   ├── ml.py        
│   │   └── authentificaton.py   
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Configuration et variables d'environnement  
│   └── database.py           
├── tests/
│   ├── __init__.py
│   ├── model_test.py
│   └── hf_test.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Installation

### Prérequis

- Python 
- PostgreSQL 
- Clés API : hugging Face 

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/KarimaChami/Projet-RetentionAI-backend.git
cd ./backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate   
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
```

5. **Initialiser la base de données**
```bash
python -m app.database init
```

6. **Lancer le serveur**
```bash
uvicorn backend.app.main:app --reload 
```

## 📡 API Endpoints

### Authentification

#### POST /register
Créer un nouveau compte utilisateur.

**Request:**
```json
{
  "email": "string@example.com",
  "username": "stringuser",
  "password": "SecureP@ssw0rd"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

#### POST /login
Se connecter et obtenir un token JWT.

**Request:**
```json
{
  "email": "string@example.com",
  "password": "SecureP@ssw0rd"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### prediction

#### POST /predict
<!-- Analyser un texte (requiert authentification JWT). -->

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "text": "Le marché boursier a connu une forte hausse aujourd'hui..."
}
```

**Response:**
```json
{
  "category": "Finance",
  "score": 0.92,
  "summary": "Analyse positive des marchés financiers montrant une tendance haussière avec des volumes d'échanges élevés.",
  "tone": "positif"
}
```

## 🔧 Configuration des Services IA

### Hugging Face

Le service utilise le modèle `facebook/bart-large-mnli` pour la classification Zero-Shot.

**Catégories supportées:**
- Finance
- Ressources Humaines
- Technologies de l'Information
- Opérations
- Marketing
- Juridique
- Sales
- Legal
- Support
- Logistique


### Gemini

Prompt Engineering pour une synthèse contextualisée :

```python
prompt = f"""
Tu dois OBLIGATOIREMENT répondre en JSON strict.
Aucun texte hors du JSON.
Même si le texte est court, donne un résumé et un ton.

Répond EXACTEMENT comme ceci :

{{
    "summary": "...",
    "tone": "positif" 
}}

Texte : {text}
"""
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest
```

### Tests spécifiques
```bash
pytest tests/hf_test.py -v
pytest tests/gemi_test.py -v
```

### Structure des tests

- **hf_test.py** : Tests de l'intégration HF
- **gemi_test.py** : Tests de l'intégration Gemini

## 📊 Logs

Les logs sont configurés dans `app/utils/logger.py` et incluent :

- **INFO** : Requêtes API, orchestration des services
- **WARNING** : Scores de classification faibles, timeouts
- **ERROR** : Erreurs critiques, échecs d'API
- **DEBUG** : Détails techniques (mode développement uniquement)


## 🔒 Sécurité

### JWT
- Token signé avec HS256
- Expiration configurable (défaut: 30 minutes)
- Validation sur tous les endpoints protégés

### Passwords
- Hashage avec argon2
- Validation de la complexité minimale
- Jamais stockés en clair

### API Keys
- Stockées dans variables d'environnement
- Jamais commitées dans le code
- Rotation régulière recommandée

## 🐳 Docker

### Build de l'image
```bash
docker build -t backend .
```

### Lancer avec Docker Compose
```bash
docker-compose up -d
```

## 🛠️ Dépendances principales

```
fastapi
uvicorn
pydantic
pytest
requests
passlib[bcrypt]
psycopg2-binary
python-jose
dotenv
sqlalchemy
alembic
python-multipart
httpx
argon2-cffi
pytest-mock
jwt
email-validator
imbalanced-learn==0.12.4
numpy==1.26.4
pandas==2.2.2
matplotlib==3.8.4
seaborn==0.13.2
scikit-learn==1.5.2
joblib==1.4.2
```

## 🚨 Gestion des erreurs

### Erreurs courantes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Non autorisé | Vérifier le token JWT |
| 422 | Validation échouée | Vérifier le format de la requête |
| 500 | Erreur serveur | Consulter les logs |
| 503 | Service indisponible | API externe down (HF/Gemini) |


## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request


## 👥 Auteurs

- Karima Chami - Dévloppeuse Fullstack & Ai

## 🔗 Liens utiles

- [Documentation Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [Documentation Gemini API](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)












# 🚀 RetentionAI - Documentation des Endpoints API

## Base URL
```
http://localhost:8000
```

---

## 📋 Table des Matières
1. [Authentification](#authentification)
2. [Prédictions ML](#prédictions-ml)
3. [IA Générative](#ia-générative)
4. [Historique](#historique)
5. [Statistiques](#statistiques)
6. [Health Check](#health-check)

---

## 🔐 Authentification

### 1. Créer un compte (Register)

**Endpoint:** `POST /register`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body (JSON):**
```json
{
  "username": "hr_manager@company.com",
  "password": "securepass123"
}
```

**Validation:**
- `username`: minimum 3 caractères, maximum 50
- `password`: minimum 6 caractères

**Réponse (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erreurs possibles:**
- `400` : Nom d'utilisateur déjà existant
- `422` : Validation échouée (mot de passe trop court, etc.)

**Exemple cURL:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hr_manager@company.com",
    "password": "securepass123"
  }'
```

---

### 2. Se connecter (Login)

**Endpoint:** `POST /login`

**Headers:**
```json
{
  "Content-Type": "application/x-www-form-urlencoded"
}
```

**Body (Form Data):**
```
username=hr_manager@company.com
password=securepass123
```

**Réponse (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erreurs possibles:**
- `401` : Identifiants incorrects

**Exemple cURL:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=hr_manager@company.com&password=securepass123"
```

**Exemple JavaScript (Frontend):**
```javascript
const formData = new URLSearchParams();
formData.append("username", "hr_manager@company.com");
formData.append("password", "securepass123");

const response = await fetch("http://localhost:8000/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: formData
});

const data = await response.json();
localStorage.setItem("token", data.access_token);
```

---

### 3. Obtenir l'utilisateur connecté

**Endpoint:** `GET /me`

**Headers:**
```json
{
  "Authorization": "Bearer {access_token}"
}
```

**Réponse (200 OK):**
```json
{
  "id": 1,
  "username": "hr_manager@company.com",
  "created_at": "2025-12-20T10:30:00"
}
```

**Erreurs possibles:**
- `401` : Token invalide ou expiré

**Exemple cURL:**
```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🤖 Prédictions ML

### 4. Prédire le risque de départ

**Endpoint:** `POST /predict`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {access_token}"
}
```

**Body (JSON):**
```json
{
  "age": 35,
  "department": "IT",
  "job_role": "Developer",
  "years_at_company": 5,
  "monthly_income": 5000.0,
  "job_satisfaction": 3,
  "work_life_balance": 2,
  "performance_rating": 4,
  "business_travel": "Travel_Rarely",
  "over_time": "Yes",
  "distance_from_home": 15,
  "employee_id": "EMP001"
}
```

**Paramètres obligatoires:**
| Paramètre | Type | Valeurs | Description |
|-----------|------|---------|-------------|
| `age` | integer | 18-100 | Âge de l'employé |
| `department` | string | IT, Sales, HR, Marketing, Finance, Operations, R&D | Département |
| `job_role` | string | Manager, Developer, Analyst, Specialist, Engineer, Consultant | Rôle |
| `years_at_company` | integer | ≥ 0 | Ancienneté |
| `monthly_income` | float | > 0 | Salaire mensuel |
| `job_satisfaction` | integer | 1-5 | Satisfaction (1=Très faible, 5=Très élevée) |
| `work_life_balance` | integer | 1-5 | Équilibre vie pro/perso |
| `performance_rating` | integer | 1-5 | Performance |
| `business_travel` | string | Non-Travel, Travel_Rarely, Travel_Frequently | Fréquence des voyages |
| `over_time` | string | Yes, No | Heures supplémentaires |
| `distance_from_home` | integer | ≥ 0 | Distance domicile-travail (km) |

**Paramètres optionnels:**
- `employee_id` (string) : Identifiant de l'employé

**Réponse (200 OK):**
```json
{
  "churn_probability": 0.7845,
  "risk_level": "HIGH",
  "timestamp": "2025-12-20T14:25:30.123456",
  "prediction_id": 42
}
```

**Niveaux de risque:**
- `LOW` : probabilité < 0.5 (< 50%)
- `MEDIUM` : 0.5 ≤ probabilité < 0.7 (50-70%)
- `HIGH` : probabilité ≥ 0.7 (≥ 70%)

**Erreurs possibles:**
- `401` : Non authentifié
- `422` : Validation échouée (âge invalide, etc.)
- `500` : Erreur de prédiction du modèle

**Exemple cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "department": "IT",
    "job_role": "Developer",
    "years_at_company": 5,
    "monthly_income": 5000.0,
    "job_satisfaction": 2,
    "work_life_balance": 2,
    "performance_rating": 4,
    "business_travel": "Travel_Frequently",
    "over_time": "Yes",
    "distance_from_home": 25
  }'
```

**Exemple JavaScript:**
```javascript
const employeeData = {
  age: 35,
  department: "IT",
  job_role: "Developer",
  years_at_company: 5,
  monthly_income: 5000.0,
  job_satisfaction: 2,
  work_life_balance: 2,
  performance_rating: 4,
  business_travel: "Travel_Frequently",
  over_time: "Yes",
  distance_from_home: 25
};

const response = await fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(employeeData)
});

const prediction = await response.json();
console.log(`Risque de départ: ${prediction.churn_probability * 100}%`);
```

---

## 🧠 IA Générative

### 5. Générer un plan de rétention

**Endpoint:** `POST /generate-retention-plan`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {access_token}"
}
```

**Body (JSON):**
```json
{
  "employee_data": {
    "age": 35,
    "department": "IT",
    "job_role": "Developer",
    "years_at_company": 5,
    "monthly_income": 5000.0,
    "job_satisfaction": 2,
    "work_life_balance": 2,
    "performance_rating": 4,
    "business_travel": "Travel_Frequently",
    "over_time": "Yes",
    "distance_from_home": 25
  },
  "churn_probability": 0.78
}
```

**Conditions:**
- `churn_probability` doit être **> 0.5** (50%)
- Si < 50%, l'endpoint retourne une erreur 400

**Réponse (200 OK):**
```json
{
  "retention_plan": [
    "Proposer 2 jours de télétravail par semaine pour améliorer l'équilibre vie professionnelle/personnelle et réduire la distance domicile-travail",
    "Organiser un entretien individuel pour comprendre les sources d'insatisfaction et proposer un plan de développement personnalisé",
    "Réduire immédiatement les heures supplémentaires et limiter les déplacements professionnels fréquents"
  ],
  "generated_at": "2025-12-20T14:30:45.789012"
}
```

**Erreurs possibles:**
- `400` : Probabilité < 50% (plan non nécessaire)
- `401` : Non authentifié
- `500` : Erreur de génération (API IA indisponible)

**Exemple cURL:**
```bash
curl -X POST "http://localhost:8000/generate-retention-plan" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_data": {
      "age": 35,
      "department": "IT",
      "job_role": "Developer",
      "years_at_company": 5,
      "monthly_income": 5000.0,
      "job_satisfaction": 2,
      "work_life_balance": 2,
      "performance_rating": 4,
      "business_travel": "Travel_Frequently",
      "over_time": "Yes",
      "distance_from_home": 25
    },
    "churn_probability": 0.78
  }'
```

**Workflow recommandé:**
```javascript
// 1. Prédiction
const predictionResponse = await fetch("/predict", {...});
const prediction = await predictionResponse.json();

// 2. Si risque élevé, générer plan
if (prediction.churn_probability > 0.5) {
  const planResponse = await fetch("/generate-retention-plan", {
    method: "POST",
    headers: {...},
    body: JSON.stringify({
      employee_data: employeeData,
      churn_probability: prediction.churn_probability
    })
  });
  
  const retentionPlan = await planResponse.json();
  console.log("Actions recommandées:", retentionPlan.retention_plan);
}
```

---

## 📊 Historique

### 6. Obtenir l'historique des prédictions

**Endpoint:** `GET /predictions/history`

**Headers:**
```json
{
  "Authorization": "Bearer {access_token}"
}
```

**Query Parameters:**
- `limit` (integer, optionnel) : Nombre maximum de résultats (défaut: 50)

**Exemple:**
```
GET /predictions/history?limit=20
```

**Réponse (200 OK):**
```json
[
  {
    "id": 42,
    "timestamp": "2025-12-20T14:25:30.123456",
    "user_id": 1,
    "employee_id": "EMP001",
    "probability": 0.7845,
    "age": 35,
    "department": "IT",
    "job_role": "Developer"
  },
  {
    "id": 41,
    "timestamp": "2025-12-20T14:20:15.654321",
    "user_id": 1,
    "employee_id": "EMP002",
    "probability": 0.3521,
    "age": 42,
    "department": "Sales",
    "job_role": "Manager"
  }
]
```

**Exemple cURL:**
```bash
curl -X GET "http://localhost:8000/predictions/history?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📈 Statistiques

### 7. Obtenir les statistiques utilisateur

**Endpoint:** `GET /stats`

**Headers:**
```json
{
  "Authorization": "Bearer {access_token}"
}
```

**Réponse (200 OK):**
```json
{
  "total_predictions": 125,
  "average_probability": 0.4523,
  "high_risk_count": 18,
  "medium_risk_count": 34,
  "low_risk_count": 73
}
```

**Détails:**
- `total_predictions` : Nombre total de prédictions effectuées
- `average_probability` : Probabilité moyenne de départ
- `high_risk_count` : Nombre d'employés à risque élevé (≥70%)
- `medium_risk_count` : Nombre d'employés à risque moyen (50-70%)
- `low_risk_count` : Nombre d'employés à risque faible (<50%)

**Exemple cURL:**
```bash
curl -X GET "http://localhost:8000/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🏥 Health Check

### 8. Vérifier l'état de l'API

**Endpoint:** `GET /`

**Aucune authentification requise**

**Réponse (200 OK):**
```json
{
  "message": "RetentionAI API",
  "version": "1.0.0",
  "status": "healthy",
  "author": "Karima Chami"
}
```

---

### 9. Health Check détaillé

**Endpoint:** `GET /health`

**Aucune authentification requise**

**Réponse (200 OK):**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-20T14:35:00.123456"
}
```

---

## 🔒 Sécurité

### Format du Token JWT

Le token JWT doit être envoyé dans le header `Authorization` :
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Durée de validité
- Par défaut : **30 minutes**
- Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` dans `.env`

### Rafraîchissement du token
Si vous recevez une erreur `401`, vous devez :
1. Rediriger l'utilisateur vers `/login`
2. Redemander une authentification

---

## 📋 Codes d'erreur HTTP

| Code | Signification |
|------|---------------|
| `200` | OK - Succès |
| `201` | Created - Ressource créée |
| `400` | Bad Request - Requête invalide |
| `401` | Unauthorized - Non authentifié |
| `422` | Unprocessable Entity - Validation échouée |
| `500` | Internal Server Error - Erreur serveur |

---

## 🧪 Collection Postman

### Import dans Postman

Créez une collection avec ces endpoints :

1. **Variables d'environnement :**
   - `base_url` : `http://localhost:8000`
   - `token` : (sera rempli après login)

2. **Script de test pour Login :**
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
}
```

3. **Headers globaux :**
```json
{
  "Authorization": "Bearer {{token}}"
}
```

---

## 💡 Exemples d'utilisation complète

### Workflow complet (JavaScript)

```javascript
// 1. Inscription
const registerResponse = await fetch("http://localhost:8000/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "hr_manager@company.com",
    password: "securepass123"
  })
});
const { access_token } = await registerResponse.json();

// 2. Prédiction
const predictionResponse = await fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${access_token}`
  },
  body: JSON.stringify({
    age: 35,
    department: "IT",
    job_role: "Developer",
    years_at_company: 5,
    monthly_income: 5000,
    job_satisfaction: 2,
    work_life_balance: 2,
    performance_rating: 4,
    business_travel: "Travel_Frequently",
    over_time: "Yes",
    distance_from_home: 25
  })
});
const prediction = await predictionResponse.json();

// 3. Plan de rétention si nécessaire
if (prediction.churn_probability > 0.5) {
  const planResponse = await fetch("http://localhost:8000/generate-retention-plan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${access_token}`
    },
    body: JSON.stringify({
      employee_data: employeeData,
      churn_probability: prediction.churn_probability
    })
  });
  const plan = await planResponse.json();
  console.log("Plan de rétention:", plan.retention_plan);
}

// 4. Consulter les statistiques
const statsResponse = await fetch("http://localhost:8000/stats", {
  headers: { "Authorization": `Bearer ${access_token}` }
});
const stats = await statsResponse.json();
console.log("Statistiques:", stats);
```

---

## 📝 Notes importantes

1. **Tous les endpoints sauf `/`, `/health`, `/register` et `/login` nécessitent une authentification JWT**

2. **Le modèle ML doit être présent dans `backend/models/best_model.pkl`**

3. **Pour l'IA générative, configurez soit `HUGGINGFACE_API_KEY` soit `GOOGLE_API_KEY` dans `.env`**

4. **Les prédictions sont automatiquement enregistrées dans la base de données**

5. **Le frontend appelle ces endpoints dans cet ordre :**
   - Login → `/login`
   - Analyse → `/predict`
   - Si risque > 50% → `/generate-retention-plan`

---

## 🔗 Liens utiles

- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc
- **Frontend** : http://localhost:3000

---

**Auteur :** Karima Chami  
**Projet :** RetentionAI - Prédicteur de Départ & Assistant RH  
**Date :** Décembre 2025