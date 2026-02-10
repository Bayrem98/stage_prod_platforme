#!/usr/bin/env bash
set -o errexit

echo "=== Installation des dépendances ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --no-input

echo "=== Application des migrations ==="
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "=== Création du superutilisateur ==="
python -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('✓ Superutilisateur créé')
else:
    print('✓ Superutilisateur existe déjà')
"

echo "=== Build terminé avec succès ==="