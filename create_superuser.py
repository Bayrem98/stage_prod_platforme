# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Vérifier si l'utilisateur admin existe déjà
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'  # À changer après la première connexion
    )
    print("Superutilisateur créé avec succès!")
else:
    print("Superutilisateur existe déjà.")