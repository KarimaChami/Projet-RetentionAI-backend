FROM python:3.11

WORKDIR /app

# Copier requirements
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier backend entier
COPY backend/ backend/
EXPOSE 8000

CMD ["uvicorn","backend.app.main:app","--host","0.0.0.0" , "--port", "8000"]