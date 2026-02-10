#!/usr/bin/env bash
set -o errexit

echo "=== Installation des dépendances ==="
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "=== Création des dossiers nécessaires ==="
mkdir -p static staticfiles media

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --no-input --clear

echo "=== Application des migrations ==="
python manage.py makemigrations --noinput || echo "Aucune nouvelle migration"
python manage.py migrate --noinput

echo "=== Création du superutilisateur ==="
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
try:
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('✓ Superutilisateur créé')
    else:
        print('✓ Superutilisateur existe déjà')
except Exception as e:
    print(f'⚠️ Erreur création admin: {e}')
"

echo "=== Build réussi ==="