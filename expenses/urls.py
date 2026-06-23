from django.urls import path
from . import views

urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_category/', views.add_category, name='add_category'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('expense_summary/', views.expense_summary, name='expense_summary'),
]
