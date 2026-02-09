# finance/create_default_categories.py
import os
import sys
import django

# Ajoutez le chemin de votre projet au sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Configure Django avec le bon chemin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    django.setup()
except Exception as e:
    print(f"Erreur lors du setup Django: {e}")
    print(f"Chemin actuel: {os.getcwd()}")
    print(f"Chemin projet: {project_path}")
    sys.exit(1)

from finance.models import TransactionCategory

# Catégories par défaut
DEFAULT_CATEGORIES = [
    # Recettes
    {'name': 'Ventes de produits', 'transaction_type': 'income'},
    {'name': 'Services clients', 'transaction_type': 'income'},
    {'name': 'Subventions', 'transaction_type': 'income'},
    {'name': 'Intérêts bancaires', 'transaction_type': 'income'},
    {'name': 'Autres recettes', 'transaction_type': 'income'},
    
    # Dépenses
    {'name': 'Achat matières premières', 'transaction_type': 'expense'},
    {'name': 'Frais de personnel', 'transaction_type': 'expense'},
    {'name': 'Salaire employés', 'transaction_type': 'salary'},
    {'name': 'Loyer', 'transaction_type': 'expense'},
    {'name': 'Électricité/Eau', 'transaction_type': 'expense'},
    {'name': 'Fournitures de bureau', 'transaction_type': 'expense'},
    {'name': 'Marketing/Publicité', 'transaction_type': 'expense'},
    {'name': 'Maintenance équipement', 'transaction_type': 'expense'},
    {'name': 'Investissement matériel', 'transaction_type': 'investment'},
    {'name': 'Investissement logiciel', 'transaction_type': 'investment'},
    {'name': 'Frais divers', 'transaction_type': 'other'},
]

def create_default_categories():
    """Crée les catégories de transaction par défaut"""
    created_count = 0
    
    for category_data in DEFAULT_CATEGORIES:
        category, created = TransactionCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={'transaction_type': category_data['transaction_type']}
        )
        
        if created:
            created_count += 1
            print(f"✓ Catégorie créée : {category.name} ({category.get_transaction_type_display()})")
        else:
            print(f"⏭ Catégorie existante : {category.name}")
    
    print(f"\n{created_count} nouvelles catégories créées sur {len(DEFAULT_CATEGORIES)}")
    return created_count

if __name__ == '__main__':
    create_default_categories()