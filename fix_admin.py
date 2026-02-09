# fix_admin.py
import os

# Contenu du admin.py corrigé
admin_content = '''from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Liste des champs à afficher
    list_display = (
        "employee_id",
        "first_name", 
        "last_name",
        "cin",
        "position",
        "department",
        "salary",
        "salary_advance",
        "is_active",
    )
    
    # Filtres
    list_filter = ("department", "contract_type", "is_active")
    
    # Champs de recherche
    search_fields = ("employee_id", "first_name", "last_name", "cin")
    
    # Formulaire d'édition
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("employee_id", "first_name", "last_name", "cin", "address")
        }),
        ("Informations professionnelles", {
            "fields": ("position", "department", "hire_date", "contract_type")
        }),
        ("Salaire et avances", {
            "fields": ("salary", "salary_advance", "advance_date", "advance_reason")
        }),
        ("Statut", {
            "fields": ("is_active", "user")
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Nom complet"
'''

# Écrire le fichier
with open("employees/admin.py", "w", encoding="utf-8") as f:
    f.write(admin_content)

print("✓ employees/admin.py a été corrigé")
print("\nMaintenant rafraîchissez la page admin: http://127.0.0.1:8000/admin/employees/employee/")