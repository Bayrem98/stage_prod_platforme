from django import forms
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'type': 'date'}),
            'advance_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'advance_reason': forms.Textarea(attrs={'rows': 3}),
        }

class AdvanceSalaryForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        label="Montant de l'avance",
        min_value=0
    )
    date = forms.DateField(
        label="Date de l'avance",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    reason = forms.CharField(
        label="Motif",
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )