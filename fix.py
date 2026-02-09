# fix.py
import os
import sys

def create_urls_files():
    """Crée les fichiers urls.py manquants"""
    
    # employees/urls.py
    employees_urls = """from django.urls import path
from . import views

urlpatterns = [
    # URLs à ajouter plus tard
]
"""
    
    # finance/urls.py
    finance_urls = """from django.urls import path
from . import views

urlpatterns = [
    # URLs à ajouter plus tard
]
"""
    
    # Créer les fichiers
    with open('employees/urls.py', 'w') as f:
        f.write(employees_urls)
    
    with open('finance/urls.py', 'w') as f:
        f.write(finance_urls)
    
    print("✓ Fichiers urls.py créés")

def update_main_urls():
    """Met à jour myproject/urls.py"""
    
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.dashboard, name='dashboard'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', core_views.profile, name='profile'),
    
    # Commenté pour l'instant - décommentez quand vous aurez créé les vues
    # path('employees/', include('employees.urls')),
    # path('finance/', include('finance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
    
    with open('myproject/urls.py', 'w') as f:
        f.write(urls_content)
    
    print("✓ myproject/urls.py mis à jour")

if __name__ == '__main__':
    print("Correction des problèmes...")
    create_urls_files()
    update_main_urls()
    print("\nExécutez maintenant :")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")