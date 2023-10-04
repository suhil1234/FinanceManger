import json
import datetime
import locale

from userPreference.models import userPreference
from . import renderers
from django.http import Http404, JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from .models import Expense,Categories
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q,Sum
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
# Create your views here.
def index(request):
    expenses = Expense.objects.all().filter(owner=request.user)
    preference = userPreference.objects.get(user=request.user)
    paginator = Paginator(expenses, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'page_obj':page_obj,
        'currency':preference.currency
    }
    return render(request,'expenses/index.html',context)

def add_expense(request):
    categories = Categories.objects.filter(user=request.user)
    context ={
        'categories' : categories
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = Categories.objects.get(id=request.POST['category'])
        date = request.POST['date']
        context={'categories':categories,
                 'data': request.POST,
                 'cat':category}
        if not amount or not amount.isdigit():
            messages.error(request,'you should put an amount and should be numbers')
            return render(request,'expenses/add-expense.html',context)
        if not date:
            messages.error(request,'you should choose a date')
            return render(request,'expenses/add-expense.html',context)        
        expense = Expense.objects.create(owner = request.user,amount= amount,
                                         description=description, category=category,date=date)
        expense.save()
        return redirect('index')   
    if not categories:
        messages.info(request,'Please add some categories first')     
    return render(request,'expenses/add-expense.html',context)

def edit_expense(request,pk):
    categories = Categories.objects.filter(user=request.user)
    expense = Expense.objects.get(pk=pk)
    category = Categories.objects.get(id=expense.category_id)
    context ={
        'categories' : categories,
        'expense': expense,
        'pk':pk,
        'cat': category
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = Categories.objects.get(id=request.POST['category'])
        date = request.POST['date']
        context={'categories':categories,
                 'expense': request.POST,
                 'cat':category,
                 'pk':pk,
                 'data':expense}
        if not amount or not amount.isdigit():
            messages.error(request,'you should put an amount and should be numbers')
            return render(request,'expenses/edit-expense.html',context)
        if not date:
            messages.error(request,'you should choose a date')
            return render(request,'expenses/edit-expense.html',context)        
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date
        expense.save()
        return redirect('index')        
    return render(request,'expenses/edit-expense.html',context)

def expense_delete(request,pk):
    expense = Expense.objects.get(pk=pk)
    context ={'pk':expense.id}
    if request.method =='POST':
        expense.delete()
        return redirect('index') 
    return render(request,'expenses/delete-expense.html',context)

def search_expenses(request):
    if request.method =='POST':
        categories = Categories.objects.filter(user=request.user)
        query = json.loads(request.body).get('search')
        if query:
            results = Expense.objects.filter(
            Q(amount__icontains=query,owner=request.user) |
            Q(category__name__icontains=query,owner=request.user) |
            Q(date__icontains=query,owner=request.user) |
            Q(description__icontains=query,owner=request.user)
        )
            data=[]
            for expense in results:
                expense_data = {
                    'id': expense.id,
                    'amount': expense.amount,
                    'description': expense.description,
                    'date': expense.date,
                    'category': expense.category.name  # Include category name
                }
                data.append(expense_data)
            print (data)
        return JsonResponse(data,safe=False)

def category_expense_summary(request):
    category_expenses = Expense.objects.filter(owner=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    category_summary = {}
    for category_expense in category_expenses:
        category_name = category_expense['category__name']
        total_amount = category_expense['total_amount']
        category_summary[category_name] = total_amount

    print(category_summary)
    return JsonResponse(category_summary)

def category_expense_summary_page(request):
    return render(request,'expenses/expenses-summary.html')

def advanced_pdf_view(request):
    locale.setlocale(locale.LC_ALL, "")
    expenses = Expense.objects.filter(owner=request.user)
    context = {
       'expenses': expenses,
    }
    response = renderers.render_to_pdf("expenses/expenses_pdf.html", context)
    if response.status_code == 404:
        raise Http404("Invoice not found")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"Expenses_{current_date}.pdf"
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response
