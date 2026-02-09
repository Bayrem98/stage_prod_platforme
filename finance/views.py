from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import date, timedelta
from .models import Transaction, TransactionCategory, CashRegister

@login_required
def cash_register(request):
    """Vue pour le registre de caisse"""
    # Récupérer le registre de caisse du jour
    today = date.today()
    
    try:
        cash_register = CashRegister.objects.get(date=today)
    except CashRegister.DoesNotExist:
        # Créer un nouveau registre pour aujourd'hui
        # Récupérer le solde de clôture d'hier
        yesterday = today - timedelta(days=1)
        try:
            yesterday_register = CashRegister.objects.get(date=yesterday)
            opening_balance = yesterday_register.closing_balance
        except CashRegister.DoesNotExist:
            opening_balance = 0
        
        cash_register = CashRegister.objects.create(
            date=today,
            opening_balance=opening_balance
        )
    
    # Transactions du jour
    transactions = Transaction.objects.filter(
        date__date=today
    ).select_related('category', 'created_by')
    
    # Calculer les totaux
    total_income = transactions.filter(
        transaction_type__in=['income', 'salary']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expense = transactions.filter(
        transaction_type__in=['expense', 'investment', 'other']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Mettre à jour le registre de caisse
    cash_register.total_income = total_income
    cash_register.total_expense = total_expense
    cash_register.save()
    
    context = {
        'cash_register': cash_register,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    
    return render(request, 'finance/cash_register.html', context)

@login_required
@permission_required('finance.add_transaction', raise_exception=True)
def add_transaction(request):
    """Vue pour ajouter une transaction"""
    from .forms import TransactionForm
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            
            messages.success(request, f"Transaction de {transaction.amount} DT ajoutée!")
            return redirect('finance:cash_register')
    else:
        # Gérer le pré-filtrage des catégories
        transaction_type = request.GET.get('type')
        initial = {}
        if transaction_type:
            initial = {'transaction_type': transaction_type}
        form = TransactionForm(initial=initial)
        
        # Filtrer les catégories si un type est spécifié
        if transaction_type and hasattr(form.fields['category'], 'queryset'):
            form.fields['category'].queryset = TransactionCategory.objects.filter(
                transaction_type=transaction_type
            )
    
    context = {'form': form}
    return render(request, 'finance/transaction_form.html', context)

@login_required
def transaction_list(request):
    """Liste de toutes les transactions"""
    transactions = Transaction.objects.all().select_related(
        'category', 'created_by'
    ).order_by('-date')
    
    # Filtres
    transaction_type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    if start_date:
        transactions = transactions.filter(date__date__gte=start_date)
    
    if end_date:
        transactions = transactions.filter(date__date__lte=end_date)
    
    # Totaux
    total_income = transactions.filter(
        transaction_type__in=['income', 'salary']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expense = transactions.filter(
        transaction_type__in=['expense', 'investment', 'other']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'transaction_types': Transaction.TRANSACTION_TYPES,
    }
    
    return render(request, 'finance/transaction_list.html', context)

@login_required
def finance_reports(request):
    """Rapports financiers"""
    # Statistiques mensuelles
    from django.db.models.functions import TruncMonth
    
    monthly_stats = Transaction.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_income=Sum('amount', filter=Q(transaction_type__in=['income', 'salary'])),
        total_expense=Sum('amount', filter=Q(transaction_type__in=['expense', 'investment', 'other'])),
        count=Count('id')
    ).order_by('-month')[:12]
    
    # Totaux par catégorie
    category_stats = Transaction.objects.values(
        'category__name', 'transaction_type'
    ).annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Balance générale
    total_income_all = Transaction.objects.filter(
        transaction_type__in=['income', 'salary']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expense_all = Transaction.objects.filter(
        transaction_type__in=['expense', 'investment', 'other']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_balance = total_income_all - total_expense_all
    
    context = {
        'monthly_stats': monthly_stats,
        'category_stats': category_stats,
        'total_income_all': total_income_all,
        'total_expense_all': total_expense_all,
        'net_balance': net_balance,
    }
    
    return render(request, 'finance/finance_reports.html', context)

@login_required
@permission_required('finance.change_cashregister', raise_exception=True)
def close_cash_register(request):
    """Fermer le registre de caisse du jour"""
    today = date.today()
    
    try:
        cash_register = CashRegister.objects.get(date=today)
        
        if cash_register.verified:
            messages.warning(request, "Le registre de caisse est déjà clôturé!")
        else:
            cash_register.verified = True
            cash_register.verified_by = request.user
            cash_register.save()
            messages.success(request, f"Registre de caisse du {today} clôturé avec succès!")
    
    except CashRegister.DoesNotExist:
        messages.error(request, "Aucun registre de caisse trouvé pour aujourd'hui!")
    
    return redirect('finance:cash_register')