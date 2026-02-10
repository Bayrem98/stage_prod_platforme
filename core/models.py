from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('manager', 'Manager'),
        ('employee', 'Employé'),
        ('accountant', 'Comptable'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name="Photo de profil (URL)"
    )
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"