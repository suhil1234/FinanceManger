from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from expenses.models import Expense
from incomes.models import Income

# Create your views here.
def index(request):
    return render(request,'dashboard/main-index.html')

def summary(request):
    incomes_summary = Income.objects.filter(owner=request.user).aggregate(incomes=Sum('amount'))
    expenses_summary = Expense.objects.filter(owner=request.user).aggregate(expenses=Sum('amount'))
    summary = {}
    summary['incomes'] = incomes_summary['incomes']
    summary['expenses'] = expenses_summary['expenses']

    print(summary)
    return JsonResponse(summary)