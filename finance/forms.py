from django import forms
from .models import Transaction, TransactionCategory, CashRegister

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'category', 'receipt']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les catégories selon le type
        if 'transaction_type' in self.data:
            try:
                transaction_type = self.data.get('transaction_type')
                self.fields['category'].queryset = TransactionCategory.objects.filter(
                    transaction_type=transaction_type
                )
            except (ValueError, TypeError):
                pass

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name', 'transaction_type']

class CashRegisterForm(forms.ModelForm):
    class Meta:
        model = CashRegister
        fields = ['opening_balance', 'verified']