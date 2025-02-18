# Utilise une image Python officielle
FROM python:3.10-slim

# Crée un répertoire pour l'application
WORKDIR /app

# Copie les fichiers de l'application dans le conteneur
COPY . /app

# Installe les dépendances requises
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port sur lequel l'application FastAPI fonctionne
EXPOSE 8000

# Commande pour exécuter l'application FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
