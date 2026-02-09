from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from core.models import CustomUser

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description", default="")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"

class Employee(models.Model):
    CONTRACT_CHOICES = [
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('stage', 'Stage'),
        ('freelance', 'Freelance'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    # Relations
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur", null=True, blank=True)
    
    # Informations personnelles - AVEC VALEURS PAR DÉFAUT CORRECTES
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Matricule")
    first_name = models.CharField(max_length=100, verbose_name="Prénom", default="")
    last_name = models.CharField(max_length=100, verbose_name="Nom", default="")
    cin = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="CIN",
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='Le CIN doit contenir 8 chiffres',
                code='invalid_cin'
            )
        ],
        default="00000000"
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Genre", default="M")
    birth_date = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    birth_place = models.CharField(max_length=100, verbose_name="Lieu de naissance", default="")
    
    # Adresse
    address = models.TextField(verbose_name="Adresse", default="")
    city = models.CharField(max_length=100, verbose_name="Ville", default="")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal", default="")
    country = models.CharField(max_length=100, default="Tunisie", verbose_name="Pays")
    personal_phone = models.CharField(max_length=20, verbose_name="Téléphone personnel", default="")
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone d'urgence", default="")
    
    # Informations professionnelles
    position = models.CharField(max_length=100, verbose_name="Poste")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Département")
    hire_date = models.DateField(verbose_name="Date d'embauche")
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, verbose_name="Type de contrat")
    contract_end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin de contrat")
    
    # Informations bancaires et salariales
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Salaire de base")
    bank_name = models.CharField(max_length=100, verbose_name="Nom de la banque", default="")
    bank_account = models.CharField(max_length=50, verbose_name="Numéro de compte", default="")
    rib = models.CharField(max_length=30, verbose_name="RIB", default="")
    
    # Avances sur salaire
    salary_advance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Avance sur salaire"
    )
    advance_date = models.DateField(null=True, blank=True, verbose_name="Date d'avance")
    advance_reason = models.TextField(blank=True, verbose_name="Motif de l'avance", default="")
    
    # Salaire net
    # net_salary = models.DecimalField(
    #     max_digits=10, 
    #     decimal_places=2, 
    #     default=0,
    #     verbose_name="Salaire net"
    # )
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # TEMPORAIREMENT - NE METTEZ PAS created_at et updated_at
    # Nous les ajouterons plus tard
    
    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour calculer le salaire net"""
         # self.net_salary = self.salary - self.salary_advance
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def net_salary(self):
        """Calcule le salaire net (propriété dynamique)"""
        return self.salary - self.salary_advance
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['last_name', 'first_name']