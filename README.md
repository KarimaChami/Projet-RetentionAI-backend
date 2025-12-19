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