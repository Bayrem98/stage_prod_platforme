from django.db import models
from django.core.validators import MinValueValidator
from core.models import CustomUser

class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=[('income', 'Recette'), ('expense', 'Dépense')])
    
    def __str__(self):
        return f"{self.name} ({self.get_transaction_type_display()})"
    
    class Meta:
        verbose_name = "Catégorie de Transaction"
        verbose_name_plural = "Catégories de Transaction"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Recette'),
        ('expense', 'Dépense'),
        ('salary', 'Salaire'),
        ('investment', 'Investissement'),
        ('other', 'Autre'),
    ]
    
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.TextField()
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True)
    receipt = models.FileField(upload_to='receipts/', blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.date.date()} - {self.get_transaction_type_display()}: {self.amount}€"
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

class CashRegister(models.Model):
    date = models.DateField(auto_now_add=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_cash_registers')
    
    def calculate_closing_balance(self):
        return self.opening_balance + self.total_income - self.total_expense
    
    def save(self, *args, **kwargs):
        if not self.closing_balance:
            self.closing_balance = self.calculate_closing_balance()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Caisse du {self.date} - Solde: {self.closing_balance}€"
    
    class Meta:
        verbose_name = "Registre de Caisse"
        verbose_name_plural = "Registres de Caisse"
        ordering = ['-date']