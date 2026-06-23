from django.shortcuts import render, redirect
from .forms import ExpenseForm, CategoryForm
# from django.shortcuts import render
from .models import Expense, Category
# from django.shortcuts import render
from django.db.models import Sum
from django.contrib import messages
# from .models import Expense
import datetime

def expense_summary(request):
    # Monthly total
    today = datetime.date.today()
    monthly_total = Expense.objects.filter(
        date__month=today.month, date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Weekly total
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    weekly_total = Expense.objects.filter(
        date__range=[start_week, end_week]
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'expense_summary.html', {
        'monthly_total': monthly_total,
        'weekly_total': weekly_total
    })

def view_expenses(request):
    expenses = Expense.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        expenses = expenses.filter(category_id=category_id)

    # Filter by date
    date = request.GET.get('date')
    if date:
        expenses = expenses.filter(date=date)

    categories = Category.objects.all()
    return render(request, 'view_expenses.html', {
        'expenses': expenses,
        'categories': categories
    })



def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense added successfully!")
            return redirect('add_expense')
        else:
            messages.error(request, "Error adding expense. Please check form.")
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('add_category')
        else:
            messages.error(request, "Error adding category. Please check form.")
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

