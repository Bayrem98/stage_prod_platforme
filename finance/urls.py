# finance/urls.py
from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.cash_register, name='cash_register'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('reports/', views.finance_reports, name='finance_reports'),
    path('close/', views.close_cash_register, name='close_cash_register'),
]