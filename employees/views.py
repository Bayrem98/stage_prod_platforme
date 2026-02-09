from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from .models import Employee, Department
from .forms import EmployeeForm, AdvanceSalaryForm
from datetime import date, timedelta

@login_required
@permission_required('employees.can_view_employees', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.select_related('department', 'user').all()
    
    # Statistiques
    total_employees = employees.count()
    active_employees = employees.filter(is_active=True).count()
    total_salary = employees.aggregate(total=Sum('salary'))['total'] or 0
    total_advances = employees.aggregate(total=Sum('salary_advance'))['total'] or 0
    
    context = {
        'employees': employees,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_salary': total_salary,
        'total_advances': total_advances,
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
@permission_required('employees.can_manage_employees', raise_exception=True)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    context = {
        'employee': employee,
    }
    return render(request, 'employees/employee_detail.html', context)

@login_required
@permission_required('employees.can_manage_employees', raise_exception=True)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employé {employee.full_name} créé avec succès!")
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    
    context = {'form': form}
    return render(request, 'employees/employee_form.html', context)

@login_required
@permission_required('employees.can_manage_employees', raise_exception=True)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employé {employee.full_name} mis à jour avec succès!")
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'employees/employee_form.html', context)

@login_required
@permission_required('employees.can_manage_advances', raise_exception=True)
def add_advance(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = AdvanceSalaryForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            advance_date = form.cleaned_data['date']
            reason = form.cleaned_data['reason']
            
            # Mettre à jour l'avance
            employee.salary_advance = amount
            employee.advance_date = advance_date
            employee.advance_reason = reason
            employee.save()
            
            messages.success(request, f"Avance de {amount} DT ajoutée pour {employee.full_name}")
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = AdvanceSalaryForm()
    
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'employees/advance_form.html', context)

@login_required
def salary_report(request):
    # Récupérer tous les employés actifs
    employees = Employee.objects.filter(is_active=True)
    
    # Calcul des totaux (avec calcul côté Python)
    total_base_salary = employees.aggregate(total=Sum('salary'))['total'] or 0
    total_advances = employees.aggregate(total=Sum('salary_advance'))['total'] or 0
    
    # Calcul du total net côté Python
    total_net_salary = 0
    for employee in employees:
        total_net_salary += float(employee.net_salary)
    
    # Par département (avec annotate quand même pour les statistiques)
    by_department = employees.values('department__name').annotate(
        count=Count('id'),
        total_salary=Sum('salary'),
        total_advances=Sum('salary_advance'),
        avg_salary=Avg('salary')
    )
    
    context = {
        'employees': employees,
        'total_base_salary': total_base_salary,
        'total_advances': total_advances,
        'total_net_salary': total_net_salary,
        'by_department': by_department,
    }
    return render(request, 'employees/salary_report.html', context)