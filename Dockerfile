# Utiliser l'image officielle de Python 3.12
FROM python:3.12

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer les migrations
RUN python manage.py migrate

# Copier le contenu du répertoire courant dans le répertoire de travail
COPY . .

# Exposer le port utilisé par l'app Django
EXPOSE 8000

# Commande pour lancer l'app Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TaskEqualizer.wsgi:application"]